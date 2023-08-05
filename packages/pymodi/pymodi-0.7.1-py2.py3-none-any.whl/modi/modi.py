"""Main MODI module."""

import time

from modi._serial_process import SerialProcess
from modi._parser_process import ParserProcess
from modi._executor_thread import ExecutorThread

from modi.module.setup_module import network
from modi.module.input_module import (
    button, dial, env, gyro, ir, mic, ultrasonic
)
from modi.module.output_module import display, led, motor, speaker

from modi.module.module import Module

import multiprocessing


class MODI:
    """
    Example:
    >>> import modi
    >>> bundle = modi.MODI()
    """

    def __init__(self, test=False):
        self._modules = list()
        self._module_ids = dict()

        self._serial_read_q = multiprocessing.Queue(100)
        self._serial_write_q = multiprocessing.Queue(100)
        self._json_recv_q = multiprocessing.Queue(100)

        self._ser_proc = None
        self._par_proc = None
        self._exe_thrd = None

        if not test:
            self._ser_proc = SerialProcess(
                self._serial_read_q, self._serial_write_q)
            self._ser_proc.daemon = True
            self._ser_proc.start()

            self._par_proc = ParserProcess(
                self._serial_read_q, self._json_recv_q)
            self._par_proc.daemon = True
            self._par_proc.start()

            self._exe_thrd = ExecutorThread(
                self._serial_write_q,
                self._json_recv_q,
                self._module_ids,
                self._modules
            )
            self._exe_thrd.daemon = True
            self._exe_thrd.start()

            # TODO: receive flag from executor thread
            time.sleep(5)

    def exit(self):
        """ Stop modi instance
        """

        self._ser_proc.stop()
        self._par_proc.stop()
        self._exe_thrd.stop()

    @property
    def modules(self):
        """Tuple of connected modules except network module.
        Example:
        >>> bundle = modi.MODI()
        >>> modules = bundle.modules
        """

        return tuple(self._modules)

    @property
    def buttons(self):
        """Tuple of connected :class:`~modi.module.button.Button` modules.
        """

        return tuple([module for module in self.modules if module.type == "button"])

    @property
    def dials(self):
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """

        return tuple([module for module in self.modules if module.type == "dial"])

    @property
    def displays(self):
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """

        return tuple([module for module in self.modules if module.type == "display"])

    @property
    def envs(self):
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """

        return tuple([module for module in self.modules if module.type == "env"])

    @property
    def gyros(self):
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """

        return tuple([module for module in self.modules if module.type == "gyro"])

    @property
    def irs(self):
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """

        return tuple([module for module in self.modules if module.type == "ir"])

    @property
    def leds(self):
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """

        return tuple([module for module in self.modules if module.type == "led"])

    @property
    def mics(self):
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """

        return tuple([module for module in self.modules if module.type == "mic"])

    @property
    def motors(self):
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """

        return tuple([module for module in self.modules if module.type == "motor"])

    @property
    def speakers(self):
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """

        return tuple([module for module in self.modules if module.type == "speaker"])

    @property
    def ultrasonics(self):
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic` modules.
        """

        return tuple([module for module in self.modules if module.type == "ultrasonic"])
