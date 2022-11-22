from .comparendo_verifik import ComparendoVerifik

class APIFactory:
    
    @staticmethod
    def get_data_api(api):
        
        try:
            if api == 'Verifik':
                return ComparendoVerifik()
            raise Exception('API not found')
        except Exception as _api_backend:
            print(_api_backend)
        return None