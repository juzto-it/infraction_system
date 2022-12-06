from .profiles import Profile
from .query_factory import QueryFactory
import asyncio
from .models import Personas, Comparendos
from utils.tools import IUtility
from core_system.serializers.comparendos import ComparendosObjectSerializer


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
            # Log con la excepción presentada
            return self.__results_api, str(err)
    
    def get_infractions_from_db(self, person: Personas):
        
        try:
            if isinstance(person, Personas):
                comparendos_db = Comparendos.objects.filter(
                    id_persona=person.pk).select_related('infraccion')
                comparendos_db.exclude(estado='Inactivo')
                
                comparendos_db = ComparendosObjectSerializer(instance=comparendos_db, many=True).data
                
                for cmp in comparendos_db:
                    if cmp.get('infraccion'): cmp['infraccion'] = cmp.get('infraccion').get('codigo')
                    cmp['fotodeteccion'] = bool(cmp['fotodeteccion'])
                    cmp['id_persona'] = None
                return comparendos_db, None
            
            raise Exception('Profile does not an object')
        
        except Exception as err:
            # Log con la excepción presentada
            return self.__results_api, str(err)
        
    def _save_infractions(self, customer: Personas):
        
        result_api = None
        result_rpa = None
        try:
            if isinstance(customer, Personas):
                
                if self._query_api:
                    result_api = self._query_api._save_infractions(customer)
                    
                if self._query_rpa:
                    pass
            else:
                raise Exception('Param customer does not a person')
            return result_api, result_rpa, None
        except Exception as err:
            # Log con la excepción presentada
            return result_api, result_rpa, str(err)
    
    def _is_allowed_by_date(self, customer: Personas):
        
        is_allowed = True
        try:
            if isinstance(customer, Personas):
                
                datetime_now = IUtility().datetime_utc_now()
                is_allowed = IUtility().validate_query_time(customer.fecha_consulta_comp, datetime_now)
            else:
                raise Exception('Customer does not an Personas object')      
        except Exception as err:
            print(err)
            
        return is_allowed
    