from .profiles import Profile
from .query_factory import QueryFactory
import asyncio



class InfractionController:
        
    def __init__(self, profile: Profile) -> None:
        self._profile = profile
        self._query_api = None
        self._query_rpa = None
        self.__results_api = list()
        self.__results_rpa = list()
        
    def _fetch_data_infractions(self) -> dict: 
        
        try:
            if isinstance(self._profile, Profile):
                
                self._query_api = QueryFactory.get_query_mode('Verifik')
                results, err = asyncio.run(self._query_api.get_infractions(self._profile))
                self.__results_api = results['comparendos'] + results['resoluciones']
                
                return self.__results_api, err
            
            raise Exception('Profile does not an object')
        
        except Exception as err:
            return self.__results_api, str(err)
        
    
    def _save_infractions(self, customer: object):
        
        try:
            if self._query_api:
                pass
            if self._query_rpa:
                pass
            
        except Exception as _e:
            print(_e)