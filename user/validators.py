from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_mobile_number(value):
    if not (str(value[1:]).isnumeric and str(value).startswith("+")) :
        raise ValidationError(
            _('%(value)s is not an valid  number(eg:+91XXXXXXXX)'),
            params={'value': value},
        )