

class Customer:
    
    
    def __init__(self, origin: str, doc_number: str, doc_type: str, person_type: str, 
                 email: str='', mobile: str='', recurring_query: bool=False) -> None:
        self._origin = origin
        self._doc_number = doc_number
        self._doc_type = doc_type
        self._person_type = person_type
        self._email = email
        self._mobile = mobile
        self._query_date = None
        self._recurring_query = recurring_query
        
    
    def _fetch_data_infractions():
        pass
    
    def _fetch_another_data():
        pass