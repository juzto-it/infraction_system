from .schemas import *
from .models import Comparendos, Personas
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from utils.tools import IUtility
from .ifc_verifik import IVerifik
from .profiles import Profile
from .models import Tokens, Logs, Personas, Comparendos
import aiohttp
import asyncio

class ComparendoVerifik(IVerifik):
    
    def __init__(self) -> None:
        self.origin = None
        self.__endpoints = ['https://api.verifik.co/v2/co/simit/consultarComparendos', 
                           'https://api.verifik.co/v2/co/simit/consultarResoluciones']
        self._infractions = list()
        self.__customer = None
        self.__comparendos_obj = {'comparendos': list(), 'resoluciones': list()}
        
    async def get_infractions(self, customer: Profile) -> dict:
        
        verifik_resp = list()
        actions = list()
        self.__customer = customer
        try:
            token = await self.__get_connection()
            if token is not None:
                
                hds = {'Authorization': token, 'Content-Type': 'application/json'} 
                _data = {'documentNumber':self.__customer._doc_number, 
                         'documentType': self.__customer._doc_type}
                
                async with aiohttp.ClientSession(headers=hds) as session:
                    for endpoint in self.__endpoints:
                       actions.append(asyncio.ensure_future(
                           self.__get_data(session, endpoint, _data)))
                       
                    response_data = await asyncio.gather(*actions)
                    for data in response_data:
                        verifik_resp.append(data)
                        
                    self.__transform_data(verifik_resp)
                
                return self.__comparendos_obj, None    
        except Exception as _e:
            print(_e)
            log_data =  {
                'origen': self.__customer._origin,
                'destino': 'Verifik',  
                'resultado': 1,
                'fecha': IUtility.datetime_utc_now,
                'detalle': _e.args
            }
            Logs.objects.create(**log_data) 
            return self.__comparendos_obj, str(_e)
                
    def _save_infractions(self, customer: Personas) -> bool:
        try:
            saved = False
            if (isinstance(customer, Personas) and 
                isinstance(self.__comparendos_obj, dict)):
                
                data_api = (self.__comparendos_obj.get('comparendos') + 
                            self.__comparendos_obj.get('resoluciones'))
                
                ids_data_api = [id['id_comparendo'] for id in data_api]
                data_bd = Comparendos.objects.filter(id_persona=customer.pk) 
                
                if len(data_bd) > 0:
                    data_bd.exclude(id_comparendo__in=ids_data_api).update(estado='Inactivo')
                               
                for cmp in data_api:
                    cmp.update({'id_persona': customer})
                    Comparendos.objects.update_or_create(id_comparendo=cmp.get('id_comparendo'),
                                                            defaults=cmp)
                saved = True            
            else:
                raise Exception('Error saving infractions. Customer or comparendos object does not an instance.')
                           
        except Exception as _e:
            saved = False
            print(_e)
            # registrar en log la exepción
            log_data =  {
                'origen': self.__customer._origin,
                'destino': 'Verifik',  
                'resultado': 1,
                'fecha': IUtility.datetime_utc_now,
                'detalle': _e.args
            }
            return Logs.objects.create(**log_data) 
        return saved
    
    def __transform_data(self, infractions):
        
        self.__comparendos_obj = {'comparendos': list(), 'resoluciones': list()}

        try:
            for element in infractions:
                try:
                    if element['api'] == 'comparendos':
                        
                        val_schema = IUtility().schema_validator(
                            schema_comparendos, element['d'])
                        if val_schema:
                            if isinstance(element['d']['data']['comparendos'], list):
                                comparendos = element['d']['data']['comparendos']
                            else:
                                comparendos = [element['d']['data']['comparendos']]
                            
                            for cmp in comparendos:
                                
                                _map = {
   
                                     'id_comparendo': cmp['numeroComparendo'],
                                     'infraccion': cmp['codigoInfraccion'],
                                     'id_persona': None,
                                     'fotodeteccion': True if cmp['codigoInfraccion'] == 'S' else False,
                                     'estado': 'Comparendo',
                                     'fecha_imposicion': IUtility().format_date_verifik(cmp['fechaComparendo']),
                                     'fecha_resolucion': None,
                                     'fecha_cobro_coactivo': None,
                                     'numero_resolucion': None,
                                     'numero_cobro_coactivo': None,
                                     'placa': cmp['placaVehiculo'],
                                     'servicio_vehiculo': cmp['servicioVehiculo'],
                                     'tipo_vehiculo': cmp['tipoVehiculo'],
                                     'secretaria': cmp['secretariaComparendo'],
                                     'direccion': cmp['direccionComparendo'],
                                     'valor_neto': None,
                                     'valor_pago': cmp['total'],
                                }
                                self.__comparendos_obj['comparendos'].append(_map)
                        else:
                            log_data =  {
                                'origen': self.__customer._origin,
                                'destino': 'Verifik',  
                                'resultado': 8,
                                'fecha': IUtility.datetime_utc_now,
                                'detalle': 'incistencia en datos'
                            }
                            return Logs.objects.create(**log_data)    
                            
                    elif element['api'] == 'resoluciones':
                        
                        val_schema = IUtility().schema_validator(schema_resoluciones, element['d'])
                        if val_schema:
                            if isinstance(element['d']['data']['resoluciones'], list):
                                resoluciones = element['d']['data']['resoluciones']
                            else:
                                resoluciones = [element['d']['data']['resoluciones']]
                            
                            for res in resoluciones:
                                
                                _map = {
   
                                     'id_comparendo': res['numeroComparendo'],
                                     'infraccion': None,
                                     'id_persona': None,
                                     'fotodeteccion': None,
                                     'estado': 'Cobro' if res['estadosResoluciones'] == 'Cobro coactivo' else 'Resolución',
                                     'fecha_imposicion': IUtility().format_date_verifik(res['fechaComparendo']),
                                     'fecha_resolucion': IUtility().format_date_verifik(res['fechaResolucion']),
                                     'fecha_cobro_coactivo': None,
                                     'numero_resolucion': res['resoluciones'],
                                     'numero_cobro_coactivo': None,
                                     'placa': None,
                                     'servicio_vehiculo': None,
                                     'tipo_vehiculo': None,
                                     'secretaria': res['secretarias'],
                                     'direccion': None,
                                     'valor_neto': None,
                                     'valor_pago': res['total'],
                                }
                                self.__comparendos_obj['resoluciones'].append(_map)
                        else:
                            # report log de respuesta inconsistente
                            log_data =  {
                                'origen': self.__customer._origin,
                                'destino': 'Verifik',  
                                'resultado': 8,
                                'fecha': IUtility.datetime_utc_now,
                                'detalle': 'incistencia en datos'
                            }
                            return Logs.objects.create(**log_data)  
                          
                except Exception as _e:
                    # report log de excepción en transform data
                    log_data =  {
                        'origen': self.__customer._origin,
                        'destino': 'Verifik',
                        'resultado': 7,
                        'fecha': IUtility.datetime_utc_now,
                        'detalle': _e.args
                    }
                    return Logs.objects.create(**log_data)
       
        
        except Exception as _e:
            # report log de excepción loop response data from verifik
            log_data =  {
                'origen': self.__customer._origin,
                'destino': 'Verifik',
                'resultado': 6,
                'fecha': IUtility.datetime_utc_now,
                'detalle': _e.args
            }
            return Logs.objects.create(**log_data)
      
    async def __get_data(self, session: aiohttp.ClientSession, url: str, params: dict) -> dict:
        
        api = None
        async with session.get(url=url, params=params) as resp:
            data = await resp.json()
            
            if 'Comparendos' in url:
                api = 'comparendos'
            elif 'Resoluciones':
                api = 'resoluciones'
            
            return {'api': api, 'd': data}
        
    async def __get_connection(self) -> str:
        
        try:
            rs_token = await Tokens.objects.aget(id_token=1)    
            return rs_token.token_key
            
        except ObjectDoesNotExist as e:
            print(e)
            # Registar log de que el token no existe o no se puede recuperar
            log_data =  {
                'origen': self.__customer._origin,
                'destino': 'Verifik',
                'resultado': 4,
                'fecha': IUtility.datetime_utc_now,
                'detalle': e.args
            }
            return Logs.objects.create(**log_data)