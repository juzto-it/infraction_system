from .ifc_query_factory import IQueryFactory
from .api_factory import APIFactory
from .rpa_factory import RPAFactory


class QueryFactory(IQueryFactory):
    
    @staticmethod
    def get_query_mode(query_type):
        
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