from datetime import date

from mx.DateTime import DateFrom, DateTimeFrom, DateTimeType, DateTimeFromJDN, today, RangeError

from django.core.exceptions import ValidationError
try:
    from django.core.validators import EMPTY_VALUES
except ImportError:
    from django.forms.fields import EMPTY_VALUES

from .exceptions import InvalidDateError
from .settings import BC, AD


def era_format(datetime):
    """
    Formats an mx.DateTime.DateTime instance to include BC/AD indicators.
    Accounts for JDN offset by subtracting a year from BC dates.
    """
    bce = False
    if datetime.year < 0:
        datetime = datetime.rebuild(year=abs(datetime.year - 1))
        bce = True
    return u'%s %s' % (datetime.date, BC if bce else AD)


def to_python(instance, value, frmt='date'):
    """
    Given a db/form field instance and a value, return a mx.DateTime.DateTime instance.
    Handles strptime operations as well.
    """
    if frmt == 'date':
        from_func = DateFrom
    else:
        from_func = DateTimeFrom
    if value in EMPTY_VALUES:
        return value
    elif isinstance(value, DateTimeType):
        pass
    elif isinstance(value, (int, long)):
        value = DateTimeFromJDN(value)
    elif isinstance(value, date):
        value = from_func(value)
    elif isinstance(value, basestring):
        if not value.strip():
            return
        try:
            value = DateTimeFromJDN(int(value))
        except ValueError:
            try:
                value = from_func(super(instance.__class__, instance).to_python(value))
            except ValidationError:
                value = strpdatetime(value)
    return value.rebuild(hour=12)


def strpdatetime(value, frmt='date'):
    """
    Parse the given input text value as a particular format (date/datetime).
    If the value is identical to today, then InvalidDateError is raised.
    This is supposed to be used as a last resort after all other validation efforts have failed.
    """
    if frmt == 'date':
        from_func = DateFrom
    else:
        from_func = DateTimeFrom
    input_value = value
    try:
        value = from_func(value)
    except RangeError, exc:
        raise InvalidDateError(input_value, exc)
    except ValueError:
        raise InvalidDateError(input_value)
    try:
        assert value == today()
    except AssertionError:
        pass
    else:
        raise InvalidDateError(input_value)
    return value
