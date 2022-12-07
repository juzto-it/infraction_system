from .rpa_bogota import RPABogota
from .rpa_medellin import RPAMedellin
from .rpa_simit import RPASimit


class RPAFactory:
    """
    Concrete class that return the access to business logic
    when the app needs fech data infractions via RPA.

    Raises:
        Exception: RPA not found.

    Returns:
        Concrete class: Returns a RPA class instance (RPASimit, 
                        RPABogota or RPAMedellin).
    """
    @staticmethod
    def get_data_rpa(rpa):
        """
        Function to generate a RPA instance when the RPA to
        fetch infractions is RPASimit, RPABogota or RPAMedellin.

        Args:
            api (str): RPA type.

        Raises:
            Exception: RPA not found.

        Returns:
            Concrete class: Returns a RPA instance.
        """
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