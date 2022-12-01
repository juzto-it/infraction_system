from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db import transaction

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
        max_length=100,
        allow_blank=True,
        allow_null=True,
        required = False
    )

    apellidos = serializers.CharField(
        label='Apellidos',
        max_length=100,
        allow_blank=True,
        allow_null=True,
        required = False
    )

    email = serializers.CharField(
        label='Email',
        max_length=100
    )

    movil = serializers.CharField(
        label='Movil',
        max_length=14
    )

    fecha_consulta_comp = serializers.DateTimeField(
        label='Fecha consulta comparendo',
        allow_null=True,
        required = False
    )

    consulta_recurrente = serializers.BooleanField(
        label='Consulta recurrente',
        allow_null=True,
        required = False
    )


    class Meta:
        model = Personas
        fields = ('documento' , 'tipo_documento', 'tipo_persona', 'nombres', 'apellidos', 'email', 'movil', 'fecha_consulta_comp', 
        'consulta_recurrente')

    def create(self, validated_data):
        try:
            with transaction.atomic():
                personas_instance = Personas.objects.filter(tipo_documento=validated_data['tipo_documento'], documento=validated_data['documento']).first()
                if personas_instance:
                    return super().update(personas_instance,validated_data)
                else:
                    return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(e)

        