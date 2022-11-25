from .profiles import Profile
from .query_factory import QueryFactory
import asyncio



class InfractionController:
        
    def __init__(self, profile: Profile) -> None:
        self._profile = profile
        
    
    def _fetch_data_infractions(self) -> dict: 
        
        try:
            if isinstance(self._profile, Profile):
                
                query = QueryFactory.get_query_mode('Verifik')

                print(f"{query.__class__} : {asyncio.run(query.get_infractions(self._profile))}")
            raise
        except:
            pass
        
    
    def _fetch_another_data():
        pass