import time
import json
import queue
import base64
import struct

from modi.module.input_module import (
    button, dial, env, gyro, ir, mic, ultrasonic
)
from modi.module.output_module import display, led, motor, speaker

from modi.module.module import Module


class ExecutorTask:
    """
    :param queue serial_write_q: Inter-process queue for writing serial
    message.
    :param queue json_recv_q: Inter-process queue for parsing json message.
    :param dict() module_ids: dict() of module_id : ['timestamp', 'uuid'].
    :param list() modules: list() of module instance.
    """

    # variables shared across all class instances
    __module_categories = ["network", "input", "output"]
    __module_types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"],
    }

    def __init__(self, serial_write_q, json_recv_q, module_ids, modules):
        super(ExecutorTask, self).__init__()
        self._serial_write_q = serial_write_q
        self._json_recv_q = json_recv_q
        self._module_ids = module_ids
        self._modules = modules

    def run(self):
        """ Run in ExecutorThread
        """

        try:
            message = json.loads(self._json_recv_q.get_nowait())
        except queue.Empty:
            pass
        else:
            self.__handler(message["c"])(message)
            time.sleep(0.004)

    def __handler(self, command):
        """ Excute task based on command message
        """

        return {
            0x00: self.__update_health,
            0x0A: self.__update_health,
            0x05: self.__update_modules,
            0x1F: self.__update_property,
        }.get(command, lambda _: None)

    def __update_health(self, message):
        """ Update information by health message
        """

        # Record current time and uuid, timestamp, battery information
        module_id = message["s"]
        curr_time_ms = int(time.time() * 1000)
        message_decoded = bytearray(base64.b64decode(message["b"]))

        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = curr_time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )
        self._module_ids[module_id]["battery"] = int(message_decoded[3])

        # Request uuid from network modules and other modules
        if not self._module_ids[module_id]["uuid"]:
            message_to_write = self.__request_uuid(
                module_id, is_network_module=False)
            self._serial_write_q.put(message_to_write)
            message_to_write = self.__request_uuid(
                module_id, is_network_module=True)
            self._serial_write_q.put(message_to_write)

        # Disconnect modules with no health message for more than 2 seconds
        for module_id, module_info in list(self._module_ids.items()):
            if curr_time_ms - module_info["timestamp"] > 1000:
                for module in self._modules:
                    if module.uuid == module_info["uuid"]:
                        module.set_connection_state(connection_state=False)

    def __update_modules(self, message):
        """ Update module information
        """

        # Set time variable for timestamp
        curr_time_ms = int(time.time() * 1000)

        # Record information by module id
        module_id = message["s"]
        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = curr_time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )

        # Extract uuid from message "b"
        message_decoded = bytearray(base64.b64decode(message["b"]))
        module_uuid_bytes = message_decoded[:4]
        module_info_bytes = message_decoded[-4:]

        module_info = (module_info_bytes[1] << 8) + module_info_bytes[0]

        module_category_idx = module_info >> 13
        module_type_idx = (module_info >> 4) & 0x1FF

        module_category = self.__module_categories[module_category_idx]
        module_type = self.__module_types[module_category][module_type_idx]
        module_uuid = self.__fit_module_uuid(
            module_info,
            (
                (module_uuid_bytes[3] << 24)
                + (module_uuid_bytes[2] << 16)
                + (module_uuid_bytes[1] << 8)
                + module_uuid_bytes[0]
            ),
        )

        self._module_ids[module_id]["uuid"] = module_uuid

        # Handle re-connected modules
        for module in self._modules:
            if module.uuid == module_uuid and not module.is_connected:
                module.set_connection_state(connection_state=True)
                # When reconnected, turn-off module pnp state
                pnp_off_message = self.__set_module_state(
                    0xFFF, Module.State.RUN, Module.State.PNP_OFF
                )
                self._serial_write_q.put(pnp_off_message)

        # Handle newly-connected modules
        if not next(
            (module for module in self._modules if module.uuid == module_uuid),
            None
        ):
            if module_category != "network":
                module_template = self.__init_module(module_type)
                module_instance = module_template(
                    module_id, module_uuid, self._serial_write_q
                )
                self.__set_pnp(
                    module_id=module_instance.id,
                    module_pnp_state=Module.State.PNP_OFF
                )
                self._modules.append(module_instance)
                # self._modules.sort(key=lambda module: module.uuid)

    def __init_module(self, module_type):
        """ Find module type for module initialize
        """

        module = {
            "button": button.Button,
            "dial": dial.Dial,
            "display": display.Display,
            "env": env.Env,
            "gyro": gyro.Gyro,
            "ir": ir.Ir,
            "led": led.Led,
            "mic": mic.Mic,
            "motor": motor.Motor,
            "speaker": speaker.Speaker,
            "ultrasonic": ultrasonic.Ultrasonic,
        }.get(module_type)
        return module

    def __update_property(self, message):
        """ Update module property
        """

        # Do not update reserved property
        property_number = message["d"]
        if property_number == 0 or property_number == 1:
            return

        # Decode message of module id and module property for update property
        for module in self._modules:
            if module.id == message["s"]:
                message_decoded = bytearray(base64.b64decode(message["b"]))
                property_type = module.PropertyType(property_number)
                module.update_property(
                    property_type,
                    round(struct.unpack("f", bytes(
                        message_decoded[:4]))[0], 2),
                )

    def __set_pnp(self, module_id, module_pnp_state):
        """ Generate module pnp on/off command
        """

        # If no module_id is specified, it will broadcast incoming pnp state
        if module_id is None:
            for curr_module_id in self._module_ids:
                pnp_message = self.__set_module_state(
                    curr_module_id, Module.State.RUN, module_pnp_state
                )
                self._serial_write_q.put(pnp_message)

        # Otherwise, it sets pnp state of the given module
        else:
            pnp_message = self.__set_module_state(
                module_id, Module.State.RUN, module_pnp_state
            )
            self._serial_write_q.put(pnp_message)

    def __fit_module_uuid(self, module_info, module_uuid):
        """ Generate uuid using bitwise operation
        """

        sizeof_module_uuid = 0
        while (module_uuid >> sizeof_module_uuid) > 0:
            sizeof_module_uuid += 1
        sizeof_module_uuid += sizeof_module_uuid % 4
        return (module_info << sizeof_module_uuid) | module_uuid

    def __set_module_state(self, destination_id, module_state, pnp_state):
        """ Generate message for set module state and pnp state
        """

        if type(module_state) is Module.State:
            message = dict()

            message["c"] = 0x09
            message["s"] = 0
            message["d"] = destination_id

            state_bytes = bytearray(2)
            state_bytes[0] = module_state.value
            state_bytes[1] = pnp_state.value

            message["b"] = base64.b64encode(bytes(state_bytes)).decode("utf-8")
            message["l"] = 2

            return json.dumps(message, separators=(",", ":"))
        else:
            raise RuntimeError("The type of state is not ModuleState")

    def init_modules(self):
        """ Initialize module on first run
        """

        BROADCAST_ID = 0xFFF

        # Reboot module
        reboot_message = self.__set_module_state(
            BROADCAST_ID, Module.State.REBOOT, Module.State.PNP_OFF
        )
        self._serial_write_q.put(reboot_message)
        self.__delay()

        # Command module pnp off
        pnp_off_message = self.__set_module_state(
            BROADCAST_ID, Module.State.RUN, Module.State.PNP_OFF
        )
        self._serial_write_q.put(pnp_off_message)
        self.__delay()

        # Command module uuid
        request_uuid_message = self.__request_uuid(BROADCAST_ID)
        self._serial_write_q.put(request_uuid_message)
        self.__delay()

    def __delay(self):
        """ Wait for delay
        """

        time.sleep(1)

    def __request_uuid(self, source_id, is_network_module=False):
        """ Generate broadcasting message for request uuid
        """

        BROADCAST_ID = 0xFFF

        message = dict()
        message["c"] = 0x28 if is_network_module else 0x08
        message["s"] = source_id
        message["d"] = BROADCAST_ID

        id_bytes = bytearray(8)
        id_bytes[0] = 0xFF
        id_bytes[1] = 0x0F

        message["b"] = base64.b64encode(bytes(id_bytes)).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))
