from .rpa_bogota import RPABogota
from .rpa_medellin import RPAMedellin
from .rpa_simit import RPASimit


class RPAFactory:
    
    @staticmethod
    def get_data_rpa(rpa):
        
        try:
            if rpa == 'Bot SIMIT':
                return RPASimit()
            if rpa == 'Bot Bogotá':
                return RPABogota()
            if rpa == 'Bot Medellín':
                return RPAMedellin()
            raise Exception('RPA not found')
        except Exception as _api_backend:
            print(_api_backend)
        return None