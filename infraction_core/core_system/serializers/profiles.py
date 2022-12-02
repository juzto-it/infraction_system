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
        query = Personas.objects.filter(tipo_documento=validated_data['doc_type'],documento=validated_data['doc_number']).first()
        return query

