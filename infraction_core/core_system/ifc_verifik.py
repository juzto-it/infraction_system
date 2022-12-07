
from abc import ABCMeta, abstractmethod


class IVerifik(metaclass=ABCMeta):
    """
    Interface that supports a specific 
    infractions

    Args:
        metaclass (ABCMeta, optional): Defaults to ABCMeta.
    """
    @staticmethod
    @abstractmethod
    def get_infractions(obj):
        pass