from mx.DateTime import DateTimeType

from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets


class DateInput(widgets.DateInput):
    """
    DateInput that returns the date from a mx.DateTime.DateTime instance to hide time information.
    Also gives a bigger input size by default since it can parse larger strings (eg January 1 2000)
    """
    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = {'size': '25'}
        elif not 'size' in attrs:
            attrs['size'] = '25'
        super(DateInput, self).__init__(attrs, format)

    def _format_value(self, value):
        if isinstance(value, DateTimeType):
            return value.date
        return value


class AdminDateWidget(DateInput, admin_widgets.AdminDateWidget):
    """
    Rebuild of the AdminDateWidget to use mx.DateTime DateInput
    """
