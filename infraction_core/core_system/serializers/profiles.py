from rest_framework import serializers
from django.conf import settings
from rest_framework.serializers import ValidationError
from includes.validator import IS_NUMBERVALIDATOR, IS_EMAIL
from django.core.validators import MinLengthValidator, EmailValidator

## MODELOS ##
from core_system.models import Comparendos, Sanciones, Personas, Infracciones
from core_system.serializers.personas import PersonasSerializer


class BasicProfileSerializer(serializers.Serializer):
    '''
    Serializador profiles
    '''
    origin = serializers.CharField(
        label='Origen',
        allow_blank=False,
        allow_null=False
    )

    doc_number = serializers.CharField(
        label='Documento',
        max_length=13,
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
        max_length=17,
        allow_blank=False,
        allow_null=False
    )

    email = serializers.CharField(
        label='Email',
        allow_blank=True,
        allow_null=True,
        validators=[
            EmailValidator()
        ],
    )

    mobile = serializers.CharField(
        label='Movil',
        allow_blank=True,
        allow_null=True,
        max_length=17
    )

    update = serializers.BooleanField(
        label='¿Actualizar informacion?',
        allow_null=True,
        default=False
    )

    def create(self, validated_data):
        persona = validated_data
        data_persona = {
            'documento': persona['doc_number'],
            'tipo_documento': persona['doc_type'],
            'tipo_persona': persona['person_type'],
            'email': persona['email'],
            'movil': persona['mobile']
        }
        print(data_persona)
        persona_serializer = PersonasSerializer(data=data_persona)
        if persona_serializer.is_valid():
            persona_serializer.save()

    
    def update(self, validated_data):
        update = self._kwargs['data'].get('update')
        if update == False: 
            return Personas.objects.update_or_create(validated_data)
