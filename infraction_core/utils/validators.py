import jsonschema
from jsonschema import validate
      
class Validator:
    
    
    @staticmethod
    def schema_validator(json_schema, data):
        try:
            validate(instance=data, schema=json_schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print(err)
            return False