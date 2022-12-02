from rest_framework import serializers
from rest_framework.serializers import ValidationError

## MODELOS ##
from core_system.models import Personas


class PersonasSerializer(serializers.ModelSerializer):
    '''
    Serializador para la creación de Personas
    '''
 
    documento = serializers.CharField(
        label='Documento',
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
        max_length=100,
        allow_null=True
    )

    apellidos = serializers.CharField(
        label='Apellidos',
        max_length=100,
        allow_null=True
    )

    email = serializers.CharField(
        label='Email',
        max_length=100,
        allow_null=True
    )

    movil = serializers.CharField(
        label='Movil',
        max_length=13,
        allow_null=True
    )

    fecha_consulta_comp = serializers.DateTimeField(
        label='Fecha consulta comparendo',
        allow_null=True,
        required=False
    )

    consulta_recurrente = serializers.BooleanField(
        label='Consulta recurrente',
        allow_null=True
    )


    class Meta:
        model = Personas
        fields = ('documento' , 'tipo_documento', 'tipo_persona', 'nombres', 'apellidos', 'email', 'movil', 'fecha_consulta_comp', 
        'consulta_recurrente')
