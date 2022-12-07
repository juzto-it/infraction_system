
from abc import ABCMeta, abstractmethod
from .formatters import Formatter
from .validators import Validator
from .logs import Log


class IUtility(Formatter, Validator, Log):
    """
    Interface to use all common tools used from the
    core system.

    Args:
        Formatter (Formatter):  Formatter instance.
        Validator (Validator):  Validator instance.
        Log (Log):              Log instance.
    """
    def __init__(self) -> None:
        super().__init__()
        
    @staticmethod
    def get_utility():
        pass
    
        
 
