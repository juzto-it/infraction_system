from .comparendo_verifik import ComparendoVerifik

class APIFactory:
    """
    Concrete class that return the access to business logic
    when the app needs fech data infractions via API.

    Raises:
        Exception: API not found.

    Returns:
        Concrete class: Returns a ComparendoVerifik instance.
    """
    @staticmethod
    def get_data_api(api):
        """
        Function to generate a ComparendoVerifik when the API to
        fetch infractions is verifik.

        Args:
            api (str): API type.

        Raises:
            Exception: API not found.

        Returns:
            Concrete class: Returns a ComparendoVerifik instance.
        """
        try:
            if api == 'Verifik':
                return ComparendoVerifik()
            raise Exception('API not found')
        except Exception as _api_backend:
            print(_api_backend)
        return None