from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db import transaction

## MODELOS ##
from core_system.models import Logs, Comparendos, Sanciones, Personas, Infracciones


class LogsSerializer(serializers.ModelSerializer):
    '''
    Serializador para la creación de Logs
    '''

    origen = serializers.CharField(
        label='Origen',
        allow_blank=False,
        allow_null=False
    )

    destino = serializers.CharField(
        label='Destino',
        allow_blank=False,
        allow_null=False
    )

    fecha = serializers.DateTimeField(
        label='Fecha consulta comparendo',
        allow_null=True,
        required = False
    )

    usuario = serializers.PrimaryKeyRelatedField(
        label='Usuario', 
        queryset=Personas.objects.all(),
        allow_null=True,
        required=False
    )

    resultados = serializers.BooleanField(
        label='Resultados',
        allow_null=True,
        required = False
    )


    class Meta:
        model = Logs
        fields = ('origen' , 'destino', 'fecha', 'usuario', 'resultados')

    def create(self, validated_data):
        try:
            with transaction.atomic():                
                return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(e)
        