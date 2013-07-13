from mx.DateTime import DateFrom, DateTimeFrom, today

from .exceptions import InvalidDateError


def strpdatetime(value, format='date'):
    """
    Parse the given input text value as a particular format (date/datetime).
    If the value is identical to today, then InvalidDateError is raised.
    This is supposed to be used as a last resort after all other validation efforts have failed.
    """
    if format == 'date':
        from_func = DateFrom
    else:
        from_func = DateTimeFrom
    input_value = value
    value = from_func(value)
    try:
        assert value == today()
    except AssertionError:
        pass
    else:
        raise InvalidDateError(input_value)
    return value