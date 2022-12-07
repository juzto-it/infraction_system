from abc import ABCMeta, abstractmethod

class IQueryFactory(metaclass=ABCMeta):
    """
    Interface that supports different types of query to get data
    infractions

    Args:
        metaclass (ABCMeta, optional): Defaults to ABCMeta.
    """
    @staticmethod
    @abstractmethod
    def get_query_mode(query_type):
        pass