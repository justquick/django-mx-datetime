from .fields import DateField
from .widgets import AdminDateWidget
from .utils import era_format


def date_format(attr):
    """
    Returns a classmethod for ModelAdmin classes to format mx DateFields to only show date information
    """
    def inner(cls, obj):
        date = getattr(obj, attr, None)
        if not date:
            return date
        return era_format(date)
    inner.admin_order_field = attr
    inner.short_description = attr.replace('_', ' ').title()
    return inner


# For ModelAdmin.formfield_overrides
mx_overrides = {
    DateField: {'widget': AdminDateWidget},
}