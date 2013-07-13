from mx.DateTime import DateFrom

from django import forms

from . import utils


class DateField(forms.DateField):
    """
    Subclasses forms.DateField to always return a mx.DateTime.DateTime instance
    """

    def to_python(self, value):
        return utils.to_python(self, value)

    def strptime(self, value, frmt):
        try:
            value = DateFrom(super(DateField, self).strptime(value, frmt))
        except ValueError:
            value = utils.strpdatetime(value)
        return value.rebuild(hour=12)
