from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core_system.profiles import BasicProfile
from utils.tools import IUtility
from core_system.controllers import InfractionController
from django.core.files.storage import default_storage
from core_system.serializers.profiles import BasicProfileSerializer
from core_system.serializers.personas import PersonasSerializer
import datetime
from datetime import date
from core_system.models import *
import pandas as pd
import json
import requests

class MultasTuio(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        get_data = False    
        csv_file = request.FILES.get('file')
        try:
            csv_file.content_type
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid parameters.'})  
        
        if 'text/csv' in csv_file.content_type:
            
            fs_object = FileSystemStorage()
            file_dest = fs_object.base_location + '/' + csv_file.name
            with default_storage.open(file_dest, 'wb') as dest:
                for chunk in csv_file.chunks():
                    dest.write(chunk)
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
            # df_multas = pd.DataFrame(columns=cols)
            df_placas = pd.read_csv(file_dest, usecols=['Placa'])
            token = Tokens.objects.get(id_token=1)
            hds = {'Authorization': token.token_key, 'Content-Type': 'application/json'}

            for index, rec in df_placas.iterrows():

                num_placa = rec['Placa']
                fecha_consulta = IUtility.datetime_utc_now()
                
                body = dict(documentType='CC', documentNumber=num_placa)
                url = 'https://api.verifik.co/v2/co/simit/consultar'
                try:
                    response = json.loads(requests.get(url=url, headers=hds, data=json.dumps(body).encode('utf8')).text)
                    LogMultas.objects.create(placa=num_placa, fecha_consulta=fecha_consulta, resultado='exitoso')
                except Exception as err:
                    LogMultas.objects.create(placa=num_placa, fecha_consulta=fecha_consulta, resultado='fallido')
                    continue
                if response.get('data').get('multas'):
                    multas = response.get('data').get('multas')
                    for multa in multas:
                        try:
                            data_multa = {
                                'fecha_consulta': fecha_consulta,
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
        else:
            return  Response(status=status.HTTP_200_OK, data={'error': 'Invalid type file.'}) 

        return Response(status=status.HTTP_200_OK, data={'object': 'finalizado'}) 

class CronMultasTuio(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            today = date.today()
            logsmultas = LogMultas.objects.filter(fecha_consulta__year=today.year,fecha_consulta__month=today.month,fecha_consulta__day=today.day,resultado='fallido')
            print(logsmultas)
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid query.'})  

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
        # df_multas = pd.DataFrame(columns=cols)
        token = Tokens.objects.get(id_token=1)
        hds = {'Authorization': token.token_key, 'Content-Type': 'application/json'}
        for rec in logsmultas:
            num_placa = rec.placa
            fecha_consulta = IUtility.datetime_utc_now()
            
            body = dict(documentType='CC', documentNumber=num_placa)
            url = 'https://api.verifik.co/v2/co/simit/consultar'
            try:
                response = json.loads(requests.get(url=url, headers=hds, data=json.dumps(body).encode('utf8')).text)
                print(response)
                LogMultas.objects.create(placa=num_placa, fecha_consulta=fecha_consulta, resultado='exitoso')
            except Exception as err:
                LogMultas.objects.create(placa=num_placa, fecha_consulta=fecha_consulta, resultado='fallido')
                continue
            if response.get('data').get('multas'):
                multas = response.get('data').get('multas')
                for multa in multas:
                    try:
                        data_multa = {
                            'fecha_consulta': fecha_consulta,
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

        return Response(status=status.HTTP_200_OK, data={'object': 'finalizado'}) 