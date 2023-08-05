import json
import unittest
from unittest.mock import MagicMock, patch

from spuhllib.edgemessages import Publisher, HubManager, send_confirmation_callback


class PublisherTest(unittest.TestCase):

    @patch('spuhllib.edgemessages.publisher.HubManager')
    def setUp(self, hub_manager_mock):
        self.mod_name = "module name"
        self.output_name = "output name"
        self.publisher = Publisher(self.mod_name, self.output_name)
        self.hub_manager_mock = hub_manager_mock

    def test_init(self):
        self.assertIsNotNone(self.publisher.last_sent_values)
        self.assertIsNone(self.publisher.datetime_last_message)

    @patch('spuhllib.edgemessages.publisher.IoTHubMessage')
    @patch('spuhllib.edgemessages.publisher.datetime')
    def test_send_message(self, datetime_mock, iot_hub_message_mock):
        message_mock = MagicMock()
        iot_hub_message_mock.return_value = message_mock
        datetime_now = "2019-12-02 18:35:58.451694"
        datetime_mock.now.return_value = datetime_now
        message = {"temperature": 20}
        self.publisher.send_message(message)
        self.hub_manager_mock().forward_event_to_output.assert_called_with(self.output_name, message_mock, 0)
        self.assertEqual(message, self.publisher.last_sent_values)
        self.assertEqual(datetime_now, self.publisher.datetime_last_message)

    @patch('spuhllib.edgemessages.publisher.IoTHubMessage')
    @patch('spuhllib.edgemessages.publisher.uuid')
    def test_create_message_uuid(self, uuid_mock, iot_hub_message_mock):
        uuid4_str = "cf870b1e-6cae-41ca-b6a1-af118e319a11"
        uuid_mock.uuid4.return_value = uuid4_str
        message = self.publisher._create_message("temperatureModule", {"temperature": 20})
        iot_hub_message_mock.assert_called()
        uuid_mock.uuid4.assert_called_once()
        self.assertEqual(uuid4_str, message.message_id)

    @patch('spuhllib.edgemessages.publisher.datetime')
    def test_create_message_time(self, datetime_mock):
        datetime_now = "2019-12-02 18:35:58.451694"
        datetime_mock.now.return_value = datetime_now
        message = self.publisher._create_message("temperatureModule", {"temperature": 20})
        result = message.get_bytearray().decode('utf-8')
        expected = json.dumps({"temperature": 20, "moduleName": "temperatureModule", "time": datetime_now})
        self.assertEqual(expected, result)
        datetime_mock.now.assert_called_once()


class HubManagerTest(unittest.TestCase):

    @patch('spuhllib.edgemessages.publisher.IoTHubModuleClient')
    @patch('spuhllib.edgemessages.publisher.PROTOCOL', "MQTT")
    def setUp(self, client_mock):
        self.hub_manager = HubManager()
        self.client_mock = client_mock

    def test_init(self):
        message_timeout = 10000
        self.client_mock.assert_called_once()
        self.client_mock().create_from_environment.assert_called_with("MQTT")
        self.client_mock().set_option.assert_called_with("messageTimeout", message_timeout)

    @patch('spuhllib.edgemessages.publisher.send_confirmation_callback')
    def test_forward_event_to_output(self, send_confirmation_callback_mock):
        io_t_hub_message = MagicMock()
        self.hub_manager.forward_event_to_output("outputQueue", io_t_hub_message, 0)
        self.client_mock().send_event_async.assert_called_with("outputQueue", io_t_hub_message,
                                                               send_confirmation_callback_mock, 0)

    def test_send_confirmation_callback(self):
        iot_hub_message_mock = MagicMock()
        result_mock = MagicMock()
        user_context_mock = MagicMock()
        properties_mock = MagicMock()
        iot_hub_message_mock.properties.return_value = properties_mock
        send_confirmation_callback(iot_hub_message_mock, result_mock, user_context_mock)
        iot_hub_message_mock.properties.assert_called_once()
        properties_mock.get_internals.assert_called_once()
