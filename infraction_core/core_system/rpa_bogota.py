from .ifc_rpa import IRPA


class RPABogota(IRPA):
    
    def __init__(self) -> None:
        self.origin = None
        self._endpoints = []
        self._infractions = list()
        
    def get_infractions(self, customer) -> list:
        return ['Infractions from the rpa Bogotá']
    
    def _save_infractions(self) -> bool:
        pass
    
    def _get_connection(self) -> str:
        pass