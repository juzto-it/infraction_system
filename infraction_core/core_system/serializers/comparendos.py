from rest_framework import serializers
from rest_framework.serializers import ValidationError

## MODELOS ##
from core_system.models import Comparendos, Sanciones, Personas, Infracciones

class InfraccionesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Infracciones
        fields = ['codigo']
        

class ComparendosSerializer(serializers.ModelSerializer):
    '''
    Serializador para la creación de Comparendos
    '''

    infraccion = serializers.PrimaryKeyRelatedField(
        label='Codigo de infraccion', 
        queryset=Infracciones.objects.all()
    )

    id_persona = serializers.PrimaryKeyRelatedField(
        label='Persona', 
        queryset=Personas.objects.all()
    )

    fotodeteccion = serializers.BooleanField(
        label='¿fotodeteccion?',
        write_only= True
    )

    estado = serializers.CharField(
        label='Estado',
        max_length=11
    )

    fecha_imposicion = serializers.DateField(
        label='Fecha de observacion'
    )

    fecha_resolucion = serializers.DateField(
        label='Fecha de resolucion'
    )

    fecha_cobro_coactivo = serializers.DateField(
        label='Fecha de cobro coactivo'
    )

    numero_resolucion = serializers.CharField(
        label='Numero de resolucion',
        max_length=30
    )

    numero_cobro_coactivo = serializers.CharField(
        label='Numero de cobro coactivo',
        max_length=30
    )

    placa = serializers.CharField(
        label='Numero de placa',
        max_length=6
    )

    servicio_vehiculo = serializers.CharField(
        label='Tipo de servicio',
        
    )

    tipo_vehiculo = serializers.CharField(
        label='Tipo de vehiculo',
        
    )

    secretaria = serializers.CharField(
        label='Secretaria',
        max_length=100
    )

    direccion = serializers.CharField(
        label='Direccion',
        max_length=120
    )

    valor_neto = serializers.FloatField(
        label='Valor neto',
    )

    valor_pago = serializers.FloatField(
        label='Valor pago',
    )

    class Meta:
        model = Comparendos
        fields = ('infraccion' , 'id_persona', 'fotodeteccion', 'estado', 'fecha_imposicion', 'fecha_resolucion', 'fecha_cobro_coactivo', 'numero_resolucion', 
        'numero_cobro_coactivo', 'placa', 'servicio_vehiculo', 'tipo_vehiculo', 'secretaria', 'direccion', 'valor_neto', 'valor_pago')
 
            
class ComparendosObjectSerializer(serializers.ModelSerializer):
    '''
    Serializador para la creación de Comparendos
    '''

    infraccion = InfraccionesSerializer()
    
    class Meta:
        model = Comparendos
        fields = '__all__'



