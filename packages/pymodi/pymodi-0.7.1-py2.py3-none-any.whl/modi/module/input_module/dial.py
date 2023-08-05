"""Dial module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Dial(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class PropertyType(Enum):
        DEGREE = 2
        TURNSPEED = 3

    def __init__(self, id_, uuid, serial_write_q):
        super(Dial, self).__init__(id_, uuid, serial_write_q)
        self._type = "dial"

    def get_degree(self):
        """
        :return: The dial's angle.
        :rtype: float
        """
        return self._get_property(self.PropertyType.DEGREE)

    def get_turnspeed(self):
        """
        :return: The dial's turn speed.
        :rtype: float
        """
        return self._get_property(self.PropertyType.TURNSPEED)
