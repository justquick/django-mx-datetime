from .fields import DateField
from .widgets import AdminDateWidget


def date_format(attr):
    """
    Returns a classmethod for ModelAdmin classes to format mx DateFields to only show date information
    """
    def inner(cls, obj):
        return getattr(obj, attr).date
    inner.admin_order_field = attr
    inner.short_description = attr.replace('_', ' ').title()
    return inner


# For ModelAdmin.formfield_overrides
mx_overrides = {
    DateField: {'widget': AdminDateWidget},
}