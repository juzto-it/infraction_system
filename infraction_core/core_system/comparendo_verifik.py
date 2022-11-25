from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from .ifc_verifik import IVerifik
from .profiles import Profile
from .models import Tokens
import aiohttp
import asyncio

class ComparendoVerifik(IVerifik):
    
    def __init__(self) -> None:
        self.origin = None
        self.__endpoints = ['https://api.verifik.co/v2/co/simit/consultarComparendos', 
                           'https://api.verifik.co/v2/co/simit/consultarResoluciones']
        self._infractions = list()
        
    async def get_infractions(self, customer: Profile) -> list:
        
        verifik_resp = list()
        actions = list()
        
        try:
            token = await self.__get_connection()
            if token is not None:
                
                hds = {'Authorization': token, 'Content-Type': 'application/json'} 
                _data = {'documentNumber':customer._doc_number, 'documentType': customer._doc_type}
                
                async with aiohttp.ClientSession(headers=hds) as session:
                    for endpoint in self.__endpoints:
                       actions.append(asyncio.ensure_future(self.__get_data(session, endpoint, _data)))
                       
                    response_data = await asyncio.gather(*actions)
                    for data in response_data:
                        verifik_resp.append(data)

                
        except Exception as _e:
            print(_e)
            pass
            
        return ['Infractions from the comparendo verifik']
    
    def _save_infractions(self) -> bool:
        pass
    
    def __transform_data(self, infractions):
        try:
            pass
        except:
            pass
            
    async def __get_data(self, session: aiohttp.ClientSession, url: str, params: dict):
        
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            return data
        
    async def __get_connection(self) -> str:
        
        try:
            rs_token = await Tokens.objects.aget(id_token=1)    
            return rs_token.token_key 
            
        except ObjectDoesNotExist as e:
            print(e)
            return None
                