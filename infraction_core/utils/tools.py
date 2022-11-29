
from abc import ABCMeta, abstractmethod
from .formatters import Formatter
from .validators import Validator
from .logs import Log


class IUtility(Formatter, Validator, Log):
    
    def __init__(self) -> None:
        super().__init__()
        
    @staticmethod
    def get_utility():
        pass
    
        
 
