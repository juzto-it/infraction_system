from rest_framework import serializers
from rest_framework.serializers import ValidationError

## MODELOS ##
from core_system.models import Comparendos, Sanciones, Personas, Infracciones


class PersonasSerializer(serializers.ModelSerializer):
    '''
    Serializador para la creación de Personas
    '''
 
    documento = serializers.CharField(
        label='Direccion',
        max_length=20
    )

    tipo_documento = serializers.CharField(
        label='Tipo documento',
        max_length=4
    )

    tipo_persona = serializers.CharField(
        label='Tipo persona',
        max_length=16
    )

    nombres = serializers.CharField(
        label='Nombres',
        max_length=100
    )

    apellidos = serializers.CharField(
        label='Apellidos',
        max_length=100
    )

    email = serializers.CharField(
        label='Email',
        max_length=100
    )

    movil = serializers.CharField(
        label='Movil',
        max_length=13
    )

    fecha_consulta_comp = serializers.DateTimeField(
        label='Fecha consulta comparendo'
    )

    consulta_recurrente = serializers.BooleanField(
        label='Consulta recurrente',
    )


    class Meta:
        model = Comparendos

