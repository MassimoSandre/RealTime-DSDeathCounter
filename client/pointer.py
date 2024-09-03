from pymem import Pymem
import sys

class Pointer:
    def __init__(self, pymemProcess:Pymem, pointed_address) -> None:
        """
        Initializes a Pointer object that encapsulates a memory address within a process.

        :param pymemProcess: An instance of Pymem representing the process whose memory is being accessed.
        :param pointed_address: The specific memory address to be pointed to.
        """
        self.__pymem = pymemProcess
        self.__curr_addr = pointed_address

    def read_pointed_value(self) -> int:
        """
        Reads the value at the pointed memory address.

        :return: The value at the pointed memory address, interpreted as an integer.
        """
        return int.from_bytes( self.__pymem.read_bytes(self.__curr_addr, length=4), byteorder=sys.byteorder)