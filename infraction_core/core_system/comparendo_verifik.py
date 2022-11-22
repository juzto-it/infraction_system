from .ifc_verifik import IVerifik

class ComparendoVerifik(IVerifik):
    
    def __init__(self) -> None:
        self.origin = None
        self._endpoints = ['https://api.verifik.co/v2/co/simit/consultarComparendos', 
                           'https://api.verifik.co/v2/co/simit/consultarResoluciones']
        self._infractions = list()
        
    def get_infractions(self, customer) -> list:
        
        return ['Infractions from the comparendo verifik']
    
    def _save_infractions(self) -> bool:
        pass
    
    def _get_connection(self) -> str:
        pass