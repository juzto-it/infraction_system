from abc import ABCMeta, abstractmethod

class IRPA(metaclass=ABCMeta):
    
    @staticmethod
    @abstractmethod
    def get_infractions(obj):
        pass
