from mx.DateTime import DateFrom, DateTimeType

from django import forms

try:
    from django.core.validators import EMPTY_VALUES
except ImportError:
    from django.forms.fields import EMPTY_VALUES


class DateField(forms.DateField):
    """
    Subclasses forms.DateField to always return a mx.DateTime.DateTime instance
    """

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return
        if isinstance(value, DateTimeType):
            return value
        return super(DateField, self).to_python(value)

    def strptime(self, value, format):
        return DateFrom(value)
