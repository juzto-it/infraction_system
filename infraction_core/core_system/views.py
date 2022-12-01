from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .profiles import BasicProfile
from .controllers import InfractionController
from core_system.serializers.comparendos import ComparendosSerializer
from core_system.serializers.profiles import BasicProfileSerializer
from core_system.serializers.personas import PersonasSerializer
from core_system.models import Comparendos
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action


# Create your views here.

class Fotomultas(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        _data = request.data
        queryset = Comparendos.objects.all()
        serializer_class = BasicProfileSerializer(_data)
        try:
            customer = BasicProfile(_data['origin'], _data['doc_number'], _data['doc_type'], _data['person_type'])
            
            if _data['email']: customer._email = _data['email']
            if _data['mobile']: customer._mobile = _data['mobile']
            
            infractions = InfractionController(customer)
            infractions._fetch_data_infractions()
            print('here')
            
        except Exception as _customer_except:
            print(_customer_except)
               
        return Response(status=status.HTTP_200_OK, data={'hola': 'saludo'}) 

class Consultas(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = BasicProfileSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
   









