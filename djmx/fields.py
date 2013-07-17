from mx.DateTime import DateTimeType, today

from django.db import models


from . import forms
from . import utils


class DateField(models.DateField):
    """
    Subclasses models.DateField to provide support for mx.DateTime.
    Data is stored as an integer in JDN notation.
    """
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'IntegerField'

    def to_python(self, value):
        return utils.to_python(self, value)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = today(hour=12)
            setattr(model_instance, self.attname, value)
            return value
        return super(DateField, self).pre_save(model_instance, add)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        if isinstance(value, DateTimeType):
            return int(value.jdn)

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

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^djmx\.fields\.DateField'])
except:
    pass