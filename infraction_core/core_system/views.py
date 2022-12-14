from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .profiles import BasicProfile
from utils.tools import IUtility
from .controllers import InfractionController
from core_system.serializers.profiles import BasicProfileSerializer
from core_system.serializers.personas import PersonasSerializer
from core_system.models import *
import pandas as pd
import json
import requests

# Create your views here.

class Fotomultas(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        API function to fetch comparendos data from Verifik API and RPA projects.
        This API works as core system to collect all the data from different sources.

        Args:
            request (POST): Json request has 

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        _data = request.data
        
        object_response = {
            'data': list(),
            'status': None,
            'error': None,
        }
        err = None
        
        try:
            # A basic profile not demand all the data structure to fetch comparendos data
            profile_serializer = BasicProfileSerializer(data=_data)
            
            # Validating if the imput data is correct
            if profile_serializer.is_valid():
                
                customer = BasicProfile(_data['origin'], _data['doc_number'], 
                                        _data['doc_type'], _data['person_type'])
                
                if _data['first_name']: customer._first_name = _data['first_name']
                if _data['last_name']: customer._last_name = _data['last_name']
                if _data['email']: customer._email = _data['email']
                if _data['mobile']: customer._mobile = _data['mobile']
                if _data['recurrent_query']: customer._recurring_query = _data['recurrent_query']
                if _data['update']: customer._update = _data['update']
                
                person = customer.save(customer.__dict__)
                
                infractions = InfractionController(customer)
                
                # Validating the cuote to renew comparendos data from the las datetime query 
                refresh_query = infractions._is_allowed_by_date(person)
                 
                if refresh_query:
                    # Fetching to the external API 
                    data_infractions, err = infractions._fetch_data_infractions()
                    _, _, err = infractions._save_infractions(person)
                    person.fecha_consulta_comp = IUtility().datetime_utc_now()
                    person.save()
                    if err:
                        raise Exception(err)
                else:
                    # Fetching to the own data base
                    data_infractions, err = infractions.get_infractions_from_db(person)
                    
                object_response['data'] = data_infractions
                object_response['status'] = 'success'
            else:
                raise Exception (profile_serializer.errors)
        
        except Exception as _except:

            object_response['status'] = 'error'
            object_response['error'] = err if err else _except.args
            # log con la excepción presentada
            print(_except)
            log_data =  {
                'origen': _data['origin'],
                'destino': 'Verifik',
                'resultado': 1,
                'fecha': IUtility.datetime_utc_now,
                'detalle': err if err else _except.args
            }

            return Logs.objects.create(**log_data)

        return Response(status=status.HTTP_200_OK, data=object_response)

class MultasTuio(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        get_data = False
        fs_object = FileSystemStorage()
        cols = ['fecha_consulta',
                'comparendo',
                'placa',
                'nit',
                'estado_comparendo',
                'comparendo_electronico',
                'fecha_comparendo',
                'tipo_infraccion',
                'ciudad_infraccion',
                'tiene_resolucion',
                'fecha_resolucion',
                'tiene_cobro_coactivo',
                'fecha_cobro_coactivo',
                'valor_infraccion',
                'fecha_notificacion',
                'valor_notificacion',
                'dias_notificacion',
                'fecha_descuento_50',
                'valor_descuento_50',
                'dias_descuento_50',
                'fecha_descuento_25',
                'valor_descuento_25',
                'dias_descuento_25',
                'fecha_sin_intereses',
                'valor_sin_intereses',
                'dias_sin_intereses',
                

                ]
        df_multas = pd.DataFrame(columns=cols)
        file_path_p = fs_object.base_location + '/Base de Datos JUZTO.xlsx'
        df_placas = pd.read_excel(file_path_p, sheet_name='Hoja1', 
                                  usecols=['Placa'])
        hds = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRJZCI6IjYxNjlmMmE3ZmU0ZjY2M2MyZmZkMDZmNCIsImRvY3VtZW50VHlwZSI6Ik5JVCIsImRvY3VtZW50TnVtYmVyIjoiOTAxMzUwNjI4LTQiLCJ2IjoxLCJyb2xlIjoiY2xpZW50Iiwic3Vic2NyaXB0aW9uUGxhbiI6IjYxNjlmMmE4NDhmOGI5N2QzZDliZGIxZCIsIkpXVFBocmFzZSI6ImFwcjI1IiwiaWF0IjoxNjU4MTcxMTA5fQ.hLzhjs_dtwR8o2J6CVHyvat9c1gqZfkgK7NqRkRmJXU' , 
               'Content-Type': 'application/json'}
        
        IUtility.format_date('04/11/2022')
        print(df_placas)
        for index, rec in df_placas.iterrows():

            num_placa = rec['Placa']
  
            
            body = dict(documentType='CC', documentNumber=num_placa)
            url = 'https://api.verifik.co/v2/co/simit/consultar'
            try:
                response = json.loads(requests.get(url=url, headers=hds, data=json.dumps(body).encode('utf8')).text)
                LogMultas.objects.create(placa=num_placa, fecha_consulta=IUtility.datetime_utc_now(), resultado='exitoso')
            except Exception as err:
                LogMultas.objects.create(placa=num_placa, fecha_consulta=IUtility.datetime_utc_now(), resultado='fallido')
                continue
            if response.get('data').get('multas'):
                multas = response.get('data').get('multas')
                for multa in multas:
                    try:
                        data_multa = {
                        'fecha_consulta': IUtility.datetime_utc_now(),
                            'id_comparendo': multa.get('numeroComparendo'),
                            'placa': num_placa,
                            'documento': multa.get('infractor').get('numeroDocumento'),
                            'estado_comparendo': multa.get('estadoComparendo'),
                            'comparendo_electronico': multa.get('comparendoElectronico'),
                            'fecha_comparendo': IUtility.format_date(multa.get('fechaComparendo')),
                            'tipo_infraccion':multa.get('infracciones')[0].get('codigoInfraccion'),
                            'ciudad_infraccion': multa.get('organismoTransito'),
                            'tiene_resolucion': multa.get('numeroResolucion'),
                            'fecha_resolucion': IUtility.format_date(multa.get('fechaResolucion')),
                            'tiene_cobro_coactivo': multa.get('nroCoactivo'),
                            'fecha_cobro_coactivo': IUtility.format_date(multa.get('fechaCoactivo')),
                            'valor_infraccion': multa.get('valorPagar'),
                            'fecha_notificacion': IUtility.format_date(multa.get('proyeccion')[0].get('fecha')) if len(multa.get('proyeccion')) > 0 else None,
                            'valor_notificacion': multa.get('proyeccion')[0].get('valor') if len(multa.get('proyeccion')) > 0 else None,
                            'dias_notificacion': multa.get('proyeccion')[0].get('dias') if len(multa.get('proyeccion')) > 0 else None,
                            'fecha_descuento_50': IUtility.format_date(multa.get('proyeccion')[1].get('fecha')) if len(multa.get('proyeccion')) > 1 else None,
                            'valor_descuento_50': multa.get('proyeccion')[1].get('valor') if len(multa.get('proyeccion')) > 1 else None,
                            'dias_descuento_50':  multa.get('proyeccion')[1].get('dias') if len(multa.get('proyeccion')) > 1 else None,
                            'fecha_descuento_25': IUtility.format_date(multa.get('proyeccion')[2].get('fecha')) if len(multa.get('proyeccion')) > 2 else None,
                            'valor_descuento_25': multa.get('proyeccion')[2].get('valor') if len(multa.get('proyeccion')) > 2 else None,
                            'dias_descuento_25': multa.get('proyeccion')[2].get('dias') if len(multa.get('proyeccion')) > 2 else None,
                            'fecha_sin_intereses': IUtility.format_date(multa.get('proyeccion')[3].get('fecha')) if len(multa.get('proyeccion')) > 3 else None,
                            'valor_sin_intereses': multa.get('proyeccion')[3].get('valor')if len(multa.get('proyeccion')) > 3 else None,
                            'dias_sin_intereses':multa.get('proyeccion')[3].get('dias') if len(multa.get('proyeccion')) > 3 else None,
                            
                        }
                        Multas.objects.update_or_create(id_comparendo=data_multa.get('id_comparendo'), defaults=data_multa)
                    except Exception as e:
                        print(e)
                    #df_multas = df_multas.append(data_multa, ignore_index=True)

        df_multas.to_csv('resultados_consulta.csv')
        print(df_multas)
        return Response(status=status.HTTP_200_OK, data={'object': 'finalizado'}) 
        