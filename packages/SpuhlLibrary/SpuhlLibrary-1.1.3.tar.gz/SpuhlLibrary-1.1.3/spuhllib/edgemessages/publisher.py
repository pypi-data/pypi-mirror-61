import json
import logging
import uuid
from datetime import datetime

# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubTransportProvider, IoTHubMessage, IoTHubError

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# global counters
SEND_CALLBACKS = 0

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT


def send_confirmation_callback(message, result, user_context):
    """
    Callback received when the forwarded message has been processed.
    """
    global SEND_CALLBACKS
    SEND_CALLBACKS += 1
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    logging.log(logging.INFO, "Confirmation[%d] received for message with result = %s\n"
                              "    Properties: %s\n"
                              "   Total calls confirmed: %d"
                % (user_context, result, key_value_pair, SEND_CALLBACKS))


class HubManager:
    """
    The HubManager forwardes messages to other modules or the iot-hub itself.
    """
    def __init__(self):
        self.client_protocol = PROTOCOL
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(PROTOCOL)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)

    def forward_event_to_output(self, output_queue_name, event, send_context):
        """
        Forwards the message received onto the next stage in the process.
        """
        self.client.send_event_async(output_queue_name, event, send_confirmation_callback, send_context)


class Publisher:
    """
    The publisher can dump dictionaries to a json-string and send this string as a message to the specified
    target module
    """

    def __init__(self, module_name, output_queue_name):
        """
        Create a new publisher to send values to the iot hub
        :param module_name: Name of the module as str
        :param output_queue_name: The name of the output queue as str
        """
        self.module_name = module_name
        self.output_queue_name = output_queue_name
        self.hub_manager = HubManager()
        self.last_sent_values = dict()
        self.datetime_last_message = None
        logging.log(logging.DEBUG, "Setup publisher for module " + module_name + " using protocol %s..."
                    % self.hub_manager.client_protocol)

    def _create_message(self, module_name, values) -> IoTHubMessage:
        """
        Creates the message with the values to forward to the routing.
        """
        values["moduleName"] = module_name
        values["time"] = str(datetime.now())
        message = IoTHubMessage(bytearray(json.dumps(values), 'utf-8'))
        message.message_id = str(uuid.uuid4())
        return message

    def send_message(self, values):
        """
        Forwards the message to the output.
        """
        try:
            logging.log(logging.DEBUG, "Sending values: " + json.dumps(values))
            message = self._create_message(self.module_name, values)
            self.hub_manager.forward_event_to_output(self.output_queue_name, message, 0)
            self.last_sent_values = values
            self.datetime_last_message = datetime.now()

        except IoTHubError as iothub_error:
            logging.log(logging.ERROR, "Unexpected error %s from IoTHub" % iothub_error)
            return
        except KeyboardInterrupt:
            logging.log(logging.ERROR, "IoTHubModuleClient stopped by Keyboard Interrupt")
