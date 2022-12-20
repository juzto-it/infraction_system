from rest_framework import serializers
from rest_framework.serializers import ValidationError
from includes.validator import IS_NUMBERVALIDATOR, IS_EMAIL
from django.core.validators import MinLengthValidator, EmailValidator
from core_system.models import *


class BasicProfileSerializer(serializers.Serializer):
    '''
    Serializador profiles
    '''
    origin = serializers.ChoiceField(
        label='Origen',
        required = True,
        choices = ORIGEN
    )

    doc_number = serializers.CharField(
        label='Documento',
        max_length=20,
        required = True
    )

    doc_type = serializers.ChoiceField(
        label='Tipo documento',
        required = True,
        choices = TIPO_DOCUMENTO
    )

    person_type = serializers.ChoiceField(
        label='Tipo persona',
        choices = TIPO_PERSONA,
        allow_blank=True,
        allow_null=True,
    )

    first_name = serializers.CharField(
        label='Nombres',
        required=False,
        max_length=100,
        allow_blank=True,
        allow_null=True,
    )

    last_name = serializers.CharField(
        label='Apellidos',
        required=False,
        max_length=100,
        allow_blank=True,
        allow_null=True
    )

    email = serializers.CharField(
        label='Email',
        max_length=100,
        validators=[
            EmailValidator()
        ],
        allow_blank=True,
        allow_null=True
    )

    mobile = serializers.CharField(
        label='Movil',
        validators=[
            IS_NUMBERVALIDATOR,
            MinLengthValidator(7)
        ],
        allow_blank=True,
        allow_null=True
    )

    update = serializers.BooleanField(
        label='¿Actualizar informacion?',
        default=False,
        required=False
        
    )

    recurrent_query = serializers.BooleanField(
        label='¿Consulta recurrente?',
        required=False,
        default=False
    )