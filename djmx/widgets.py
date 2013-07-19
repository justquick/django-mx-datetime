from mx.DateTime import DateTimeType

from django.forms import widgets
from django.contrib.admin import widgets as admin_widgets
from django.utils.encoding import force_unicode

from .utils import era_format, strpdatetime


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

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        if value:
            # Only add the 'value' attribute if a value is non-empty.
            attrs['value'] = force_unicode(self._format_value(value))

            # Add formatted value to attrs for display.
            attrs['placeholder'] = era_format(strpdatetime(value))
        return super(DateInput, self).render(name, value, attrs)


class AdminDateWidget(DateInput, admin_widgets.AdminDateWidget):
    """
    Rebuild of the AdminDateWidget to use mx.DateTime DateInput
    """
