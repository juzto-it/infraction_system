from .ifc_query_factory import IQueryFactory
from .api_factory import APIFactory
from .rpa_factory import RPAFactory


class QueryFactory(IQueryFactory):
    """
    Concrete class that implements the interface for query modes
    (IQueryFactory) 

    Args:
        IQueryFactory (Interface):  Class as interface with abstract methods
                                    to call different factory types.

    Raises:
        Exception: When the factory is not found.

    Returns:
        Class object: APIFactory or RPAFactory class.
    """
    @staticmethod
    def get_query_mode(query_type):
        """
        Function to get the fetch infractions factory.

        Args:
            query_type (str):   Type of rpa or api backend to get the
                                data.

        Raises:
            Exception: When the factory is not found.

        Returns:
            Class object: APIFactory or RPAFactory class.
        """
        rpa_backends = ['Bot SIMIT', 'Bot Bogotá', 'Bot Medellín']
        api_backends = ['Verifik']
        
        try:
            if query_type in api_backends:
                return APIFactory().get_data_api(query_type)
            if query_type in rpa_backends:
                return RPAFactory().get_data_rpa(query_type)
            raise Exception('Query factory type not found')
        
        except Exception as _query_backends:
            print(_query_backends)
        return None