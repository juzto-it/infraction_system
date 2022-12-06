import os
import jsonschema
from jsonschema import validate
from datetime import datetime, timezone, timedelta, date
from core_system.models import Sanciones, Infracciones, Parametrizaciones
import yaml
from yaml.loader import SafeLoader

class Validator:
    
    
    @staticmethod
    def schema_validator(json_schema: dict, data: dict):
        try:
            validate(instance=data, schema=json_schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            return False
        
    @staticmethod
    def get_infraction(inf_type: str, inf_date: str):
        
        invm = None
        invm_value = 0
        try:
            if isinstance(inf_type, str) and isinstance(inf_date, str):
                
                _path = os.path.dirname(os.path.abspath(__file__)) + '/inmv_data.yaml'
                _class = inf_type[0]
                _year = inf_date[0:4]
                
                sancion, created = Sanciones.objects.get_or_create(infraccion=_class, 
                                                                   anio=_year)
                if created:
                    sancion_base = Sanciones.objects.filter(infraccion=_class).first()
                    sancion.smldv = sancion_base.smldv
                    sancion.save()
                
                with open(_path) as yaml_file: 
                    invm = yaml.load(yaml_file, Loader=SafeLoader)
                
                invm_value = invm.get(inf_type)    
                infraccion, created = Infracciones.objects.get_or_create(codigo=inf_type, 
                                                                         id_sancion=sancion,
                                                                         inmovilizacion=invm_value)

                    
                return infraccion
            raise Exception('Infraction type or date are incorrect data type.')    
        except Exception as err:
            # Escribir log de que ocurrio una excepción (guardar el err)
            return None
    
    @staticmethod
    def validate_query_time(query_date: datetime, date_time_now: str):
        
        default_days = 0
        try:
            if isinstance(query_date, datetime) and isinstance(date_time_now, str):
                
                current_datetime = datetime.strptime(date_time_now, '%Y-%m-%d %H:%M:%S')
                person_datetime =  datetime.strptime(query_date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                default_days = Parametrizaciones.objects.filter(clave='next_query_days').first()
                
                if (person_datetime + timedelta(days=int(default_days.valor))) > current_datetime:
                    return False
                else:
                    return True
            else:
                return True
        except Exception as err:
            print(err)
            return True