
from abc import ABCMeta, abstractmethod


class IVerifik(metaclass=ABCMeta):
    
    @staticmethod
    @abstractmethod
    def get_infractions(obj):
        pass