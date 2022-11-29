
class Profile:
      
    def __init__(self, origin: str, doc_number: str, doc_type: str, person_type: str) -> None:
        
        self._origin = origin
        self._doc_number = doc_number
        self._doc_type = doc_type
        self._person_type = person_type
        
    def __str__(self) -> str:
        return self._doc_type + ' ' + self._doc_number


class BasicProfile(Profile):
      
    def __init__(self, origin: str, doc_number: str, doc_type: str, person_type: str,
                 first_name: str=None, last_name: str=None, email: str=None, 
                 mobile: str=None, recurring_query: bool=False) -> None:
        
        super().__init__(origin=origin, doc_number=doc_number, doc_type=doc_type, 
                         person_type=person_type)
        
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._mobile = mobile
        self._query_date = None
        self._recurring_query = recurring_query
        
 
class JuztoProfile(Profile):
      
    def __init__(self, origin: str, doc_number: str, doc_type: str, person_type: str,
                 first_name: str, last_name: str, email: str, 
                 mobile: str, recurring_query: bool=False) -> None:
        
        super().__init__(origin=origin, doc_number=doc_number, doc_type=doc_type, 
                         person_type=person_type)

        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._mobile = mobile
        self._query_date = None
        self._recurring_query = recurring_query
        
    
    

        