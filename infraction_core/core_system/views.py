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

            Logs.objects.create(**log_data)

        return Response(status=status.HTTP_200_OK, data=object_response)
