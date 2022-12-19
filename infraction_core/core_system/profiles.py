from .models import Personas
from utils.tools import IUtility


class Profile:         
    """
    Class base of different request profiles. The minimun profile have
    a origin, doc number, doc type a person type. This attributes are
    neccesary to make any type of request to obtain infractions.
    
    Args:
        origin (str):       Request source system or client.
        doc_number (str):   Customer doc number.
        doc_type (str):     Customer doc type. Official doc types.

    Attributes:
        origin (str):       Request source system or client.
        doc_number (str):   Customer doc number.
        doc_type (str):     Customer doc type. Official doc types.
        person_type (str):  Customer person type (Natural, Jurídica).
        update (boolean):   Default False if update the Profile -> Persona
                            is not necessary.
        data_map (dict):    Data structure to transform a Profile in Persona
                            object.
    
    """
    def __init__(self, origin: str, doc_number: str, doc_type: str) -> None:
        
        self._origin = origin
        self._doc_number = doc_number
        self._doc_type = doc_type
        self._update = False
        self._data_map = dict()
        
    def __str__(self) -> str:
        return self._doc_type + ' ' + self._doc_number
    
    def save(self, validated_data: dict) -> Personas:
        """
        Function to save the Profile data to Persona 
        object in database.

        Args:
            validated_data (dict): a Profile dictionary with all data neccessary.

        Returns:
            Personas: A Personas object saved (created or updated).
        """
        person = None
        try:
            #validated_data.pop('origin')
            self.__map_object(validated_data)
        
            if validated_data.get('_update'):
                person = self.__update(self._data_map)
                return person
            else:
                person = self.__create(self._data_map)
                return person
            
        except Exception as err: 
            result = err
        return person    
        
    def __create(self, c_data: dict):
        """
        Function to get or create a persona in database.
        Args:
            c_data (dict): A profile maped in Persona data structure.

        Returns:
            Persona: A Persona object obtained or created.
        """
        person, _ = Personas.objects.get_or_create(
            documento=c_data.get('documento'), 
            tipo_documento=c_data.get('tipo_documento'),
            defaults=c_data)
        
        person.consulta_recurrente = c_data.get('consulta_recurrente')
        person.save()
        
        return person
    
    def __update(self, u_data: dict):
        """
        Function to update or create a persona in database.
        Args:
            u_data (dict): A profile maped in Persona data structure.

        Returns:
            Persona: A Persona object updated or created.
        """
        person, _ = Personas.objects.update_or_create(
            documento=u_data.get('documento'), 
            tipo_documento=u_data.get('tipo_documento'),
            defaults=u_data)
        return person
    
    def __map_object(self, validated_data: dict):
        """
        Function to map the profile data structure into a Persona object
        model structure. 

        Args:
            validated_data (dict):  Profile dictionary with all 
                                    data neccessary.

        Raises:
            Exception:              When de input data does not 
                                    a dicctionary.

        Returns:
            dict:                   With the profile data maped into a
                                    Persona structure.
        """
        
        try:
            
            if isinstance(validated_data, dict):
                self._data_map = {
                   'documento': validated_data.get('_doc_number'),
                   'tipo_documento': validated_data.get('_doc_type'),
                   'tipo_persona': validated_data.get('_person_type'),
                   'nombres': validated_data.get('_first_name'),
                   'apellidos': validated_data.get('_last_name'),
                   'email': validated_data.get('_email'),
                   'movil': validated_data.get('_mobile'),
                   'consulta_recurrente': validated_data.get('_recurring_query')
                   }
                return self._data_map

            raise Exception('Validated data does not a dict')
        
        except Exception as err:
            return err
            
            
class BasicProfile(Profile):
    """
    Basic profiles is inheritance from Profile. This profile type
    manage the basic data to make a request.
    
    Args:
        origin (str):       Request source system or client.
        doc_number (str):   Customer doc number.
        doc_type (str):     Customer doc type. Official doc types.
        person:type (str):  Customer person type (Natural, Jurídica).

    Attributes:
        first_name (str):           Customer first name.
        last_name (str):            Customer last name.
        email (str):                Customer email.
        mobile (str):               Customer mobile number.
        query_date (str):           Date time of last query.
        recurring_query (boolean):  If the customer needs recurrent queries
                                    to fetch infractions.

    """      
    def __init__(self, origin: str, doc_number: str, doc_type: str, person_type: str=None,
                 first_name: str=None, last_name: str=None, email: str=None, 
                 mobile: str=None, recurring_query: bool=False) -> None:
        
        super().__init__(origin=origin, doc_number=doc_number, doc_type=doc_type)
        self._person_type = person_type
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._mobile = mobile
        self._query_date = None
        self._recurring_query = recurring_query
        
 
class JuztoProfile(Profile):
    """
    Basic profiles is inheritance from Profile. This profile type
    manage the basic data to make a request.
    
    Args:
        origin (str):       Request source system or client.
        doc_number (str):   Customer doc number.
        doc_type (str):     Customer doc type. Official doc types.
        person:type (str):  Customer person type (Natural, Jurídica).
        first_name (str):   Customer first name.
        last_name (str):    Customer last name.
        email (str):        Customer email.
        mobile (str):       Customer mobile number.
        query_date (str):   Date time of last query.

    Attributes:
        first_name (str):           Customer first name.
        last_name (str):            Customer last name.
        email (str):                Customer email.
        mobile (str):               Customer mobile number.
        query_date (str):           Date time of last query.
        recurring_query (boolean):  If the customer needs recurrent queries
                                    to fetch infractions.

    """     
    def __init__(self, origin: str, doc_number: str, doc_type: str, person_type: str,
                 first_name: str, last_name: str, email: str, 
                 mobile: str, recurring_query: bool=False) -> None:
        
        super().__init__(origin=origin, doc_number=doc_number, doc_type=doc_type, 
                         person_type=person_type)
        self._person_type = person_type
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._mobile = mobile
        self._query_date = None
        self._recurring_query = recurring_query
        
    
    

        