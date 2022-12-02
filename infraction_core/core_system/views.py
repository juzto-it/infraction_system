from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .profiles import BasicProfile
from .controllers import InfractionController
from core_system.serializers.comparendos import ComparendosSerializer
from core_system.serializers.personas import PersonasSerializer
from core_system.serializers.profiles import BasicProfileSerializer
from core_system.models import Comparendos
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action


# Create your views here.

class Fotomultas(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        _data = request.data
        
        object_response = {
            'data': list(),
            'status': None,
            'error': None,
        }
        err = None
        
        try:
            
            profile_serializer = BasicProfileSerializer(data=_data)
            
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
                data_infractions, err = infractions._fetch_data_infractions()
                _, _, err = infractions._save_infractions(person)
                if err:
                    raise Exception(err)
                    
                object_response['data'] = data_infractions
                object_response['status'] = 'success'
            else:
                raise Exception (profile_serializer.errors)
        except Exception as _except:

            object_response['status'] = 'error'
            object_response['error'] = err if err else _except.args
            print(_except)

        return Response(status=status.HTTP_200_OK, data=object_response)
