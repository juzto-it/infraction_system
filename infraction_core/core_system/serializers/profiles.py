from rest_framework import serializers
from rest_framework.serializers import ValidationError

## MODELOS ##
from core_system.models import Comparendos, Sanciones, Personas, Infracciones


class BasicProfileSerializer(serializers.Serializer):
    '''
    Serializador profiles
    '''
    origin = serializers.CharField(
        label='Origen',
        max_length=20
    )

    doc_number = serializers.CharField(
        label='Documento',
        max_length=20
    )

    doc_type = serializers.CharField(
        label='Tipo documento',
        max_length=4
    )

    person_type = serializers.CharField(
        label='Tipo persona',
        max_length=16
    )

    first_name = serializers.CharField(
        label='Nombres',
        max_length=100
    )

    last_name = serializers.CharField(
        label='Apellidos',
        max_length=100
    )

    email = serializers.CharField(
        label='Email',
        max_length=100
    )

    mobile = serializers.CharField(
        label='Movil',
        max_length=13
    )

    update = serializers.BooleanField(
        label='¿Actualizar informacion?',
    )

    def create(self, validated_data):
        person = Personas.objects.filter(tipo_documento = validated_data['doc_type'], documento = validated_data['doc_number']).first()
        if person:
            raise serializers.ValidationError({'detail':'El usuario ya ha sido registrado'})
        return super().create(validated_data)


    def update(self, validated_data):
        update = self._kwargs['data'].get('update')
        if update == 1:
            instance = Personas.objects.filter(tipo_documento = validated_data['doc_type'], documento = validated_data['doc_number']).first()   
            return super().update(instance, validated_data)

