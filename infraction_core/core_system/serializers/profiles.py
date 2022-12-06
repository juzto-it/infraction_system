from rest_framework import serializers
from rest_framework.serializers import ValidationError
from includes.validator import IS_NUMBERVALIDATOR, IS_EMAIL
from django.core.validators import MinLengthValidator, EmailValidator


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