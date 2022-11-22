from abc import ABCMeta, abstractmethod

class IQueryFactory(metaclass=ABCMeta):
    
    @staticmethod
    @abstractmethod
    def get_query_mode(query_type):
        pass