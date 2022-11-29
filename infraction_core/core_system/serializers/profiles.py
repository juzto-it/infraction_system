from rest_framework import serializers
from rest_framework.serializers import ValidationError
from includes.validator import IS_NUMBERVALIDATOR, IS_EMAIL
from django.core.validators import MinLengthValidator, EmailValidator

## MODELOS ##
from core_system.models import Comparendos, Sanciones, Personas, Infracciones


class BasicProfileSerializer(serializers.Serializer):
    '''
    Serializador profiles
    '''
    origin = serializers.CharField(
        label='Origen',
        max_length=20,
        allow_blank=False,
        allow_null=False
    )

    doc_number = serializers.CharField(
        label='Documento',
        max_length=20,
        allow_blank=False,
        allow_null=False
    )

    doc_type = serializers.CharField(
        label='Tipo documento',
        max_length=4,
        allow_blank=False,
        allow_null=False
    )

    person_type = serializers.CharField(
        label='Tipo persona',
        max_length=16,
        allow_blank=False,
        allow_null=False
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
        max_length=100,
        validators=[
            EmailValidator()
        ],
    )

    mobile = serializers.CharField(
        label='Movil',
        validators=[
            IS_NUMBERVALIDATOR,
            MinLengthValidator(7)
        ],
    )

    update = serializers.BooleanField(
        label='¿Actualizar informacion?',
    )

    def create(self, validated_data):
        Personas.objects.get_or_create(validated_data)
    
    def update(self, validated_data):
        update = self._kwargs['data'].get('update')
        if update == 1: 
            Personas.objects.update_or_create(validated_data)

