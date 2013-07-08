from datetime import date
from mx.DateTime import DateTimeFromJDN, DateTimeType, DateFrom, today

from django.db import models, connection
from django.core.exceptions import ValidationError

from . import forms


class DateField(models.DateField):
    """
    Subclasses models.DateField to provide support for mx.DateTime.
    Data is stored as an integer in JDN notation.
    """
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'IntegerField'

    def to_python(self, value):
        if value is None or isinstance(value, DateTimeType):
            return value
        elif isinstance(value, (int, long)):
            value = DateTimeFromJDN(value)
        elif isinstance(value, date):
            value = DateFrom(value)
        elif isinstance(value, basestring):
            if not value.strip():
                return
            try:
                value = DateTimeFromJDN(int(value))
            except ValueError:
                try:
                    value = DateFrom(super(DateField, self).to_python(value))
                except ValidationError:
                    # TODO: if mx doesnt understand the input type it always returns today here
                    value = DateFrom(value)
        return value.rebuild(hour=12)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = today(hour=12)
            setattr(model_instance, self.attname, value)
            return value
        return super(DateField, self).pre_save(model_instance, add)

    def get_db_prep_value(self, value, connection=connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        if isinstance(value, DateTimeType):
            return int(value.rebuild(hour=12).jdn)

    def get_prep_value(self, value):
        return self.to_python(value)

    def get_prep_lookup(self, lookup_type, value):
        value = super(DateField, self).get_prep_lookup(lookup_type, value)
        if lookup_type in ('month', 'day', 'week_day', 'year'):
            raise ValueError('The __%s lookup is not supported' % lookup_type)
        return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        return '' if val is None else str(int(getattr(obj, self.attname).jdn))

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.DateField}
        defaults.update(kwargs)
        return super(DateField, self).formfield(**defaults)
