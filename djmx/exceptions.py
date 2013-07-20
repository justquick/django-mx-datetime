from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

INVALID = _("'%s' value has an invalid date format.")


class InvalidDateError(ValidationError):
    def __init__(self, input_value, exc=None, **kwargs):
        if exc:
            super(InvalidDateError, self).__init__(exc.args[0])
        else:
            super(InvalidDateError, self).__init__(INVALID % input_value, **kwargs)
