from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .profiles import BasicProfile
from .controllers import InfractionController


# Create your views here.

class Fotomultas(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        
        _data = request.data
        
        # Aquí va un serializador
        try:
            customer = BasicProfile(_data['origin'], _data['doc_number'], _data['doc_type'], _data['person_type'])
            
            if _data['email']: customer._email = _data['email']
            if _data['mobile']: customer._mobile = _data['mobile']
            
            infractions = InfractionController(customer)
            infractions._fetch_data_infractions()
            
        except Exception as _customer_except:
            print(_customer_except)
        
        

        
        return Response(status=status.HTTP_200_OK, data={'hola': 'saludo'}) 
