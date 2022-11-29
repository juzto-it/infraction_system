# pylint: disable=C0111
'''
Django custom validations
'''
from django.core.validators import RegexValidator


IS_ALPHANUMERICVALIDATOR = RegexValidator(r'^[a-zA-Z0-9 ]*$',
                                          message='Este campo debe ser alfanumérico.',
                                          code='Inválido')

IS_NUMBERVALIDATOR = RegexValidator(r'^[0-9]*$',
                                    message='Este campo debe ser numérico.',
                                    code='Inválido')

IS_NUMBER0VALIDATOR = RegexValidator(r'^[1-9][0-9]*$',
                                    message='Este campo debe ser numérico.',
                                    code='Inválido')

IS_LOWERVALIDATOR = RegexValidator(r'^[a-z]*$',
                                   message='Este campo solo permite letras minúsculas.',
                                   code='Inválido')

IS_NODIACRITICVALIDATOR = RegexValidator(r'^[a-zA-Z]*$',
                                         message='Este campo no permite letras tildadas.',
                                         code='Inválido')

IS_ALPHAVALIDATOR = RegexValidator(r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$',
                                   message='Este campo sólo permite letras.',
                                   code='Inválido')

IS_LENGTH = RegexValidator(r'^[0-9]{1,3}$',
                                   message='Este campo solo permite 3 dígitos',
                                   code='Inválido')

IS_USER_TWITTER = RegexValidator(
                regex='^@?(?!.*admin|.*twitter)(\w){1,15}$',
                flags=2,
                message='Introduzca un usuario de Twitter válido',
            )

IS_USER_INSTAGRAM = RegexValidator(
                regex='^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$',
                flags=2,
                message='Introduzca un usuario de Instagram válido',
            )

IS_USER_FACEBOOK = RegexValidator(
                regex='^[a-z\d.]{5,}$',
                flags=2,
                message='Introduzca un usuario de Facebook válido',
            )


IS_EMAIL = RegexValidator(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",
                                   message='Este campo debe de ser un email',
                                   code='Inválido')
