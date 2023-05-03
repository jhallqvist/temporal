""" Short Desc.

Long Description

Example:
    Ex1
    Ex2

"""

from temporal.constants import DAY_NAMES, DAY_NAMES_LONG, MONTH_NAMES, MONTH_NAMES_LONG
from temporal.algorithms import days_to_date

def strftime(object, text: str) -> str:
        directives = {
        '%a', '%A', '%w', '%d', '%-d', '%b', '%B', '%m', '%-m', '%y', '%-y',
        '%Y', '%H', '%-H', '%I', '%-I', '%p', '%M', '%-M', '%S', '%-S', '%f',
        '%z', '%Z', '%j', '%-j', '%U', '%W', '%c', '%x', '%X', '%%'}
        for directive in directives:
            if directive in text:
                if directive == '%a':
                    data = DAY_NAMES[object.weekday()]
                elif directive == '%A':
                    data = DAY_NAMES_LONG[object.weekday()]
                elif directive == '%w':
                    data = f'{object.weekday()}'
                elif directive == '%d':
                    data = f'{object.day:02}'
                elif directive == '%-d':
                    data = f'{object.day}'
                elif directive == '%b':
                    data = MONTH_NAMES[object.month]
                elif directive == '%B':
                    data = MONTH_NAMES_LONG[object.month]
                elif directive == '%m':
                    data = f'{object.month:02}'
                elif directive == '%-m':
                    data = f'{object.month}'
                elif directive == '%y':
                    data = f'{object.year % 100:02}'
                elif directive == '%-y':
                    data = f'{object.year % 100}'
                elif directive == '%Y':
                    data = f'{object.year}'

                text = text.replace(directive, data)
        return text

def iso_format(text: str) -> str:
    # Standard formats that can be translated directy to a Date object:
    # Shortest allowed: 7
    # Longeset allowed: 10
    # Calendar
        # YYYY-MM-DD
        # YYYY-MM
        # YYYYMMDD
    # Week:
        # YYYY-Www
        # YYYYWww
        # YYYY-Www-D
        # YYYYWwwD
    # Ordinal:
        # YYYY-DDD
        # YYYYDDD
    # First four must be year,
    # If next is hyphen calendar or week must have a hyphen befor the optional day part
    # 
    year = int(text[0:4])
    has_sep = text[4] == '-'
    pos = 4 + has_sep
    if text[pos] == 'W':
        pos += 1
        week = int(text[pos:pos+2])
        pos += 2
        if has_sep:
            if text[pos] != '-':
                raise ValueError('Inconsistent usage of separator')
            pos += 1
        day = int(text[pos:pos+2])
        pos += 2
        if pos < len(text):
            raise ValueError(f'trailing garbage in string: {text[pos:]}')
        return year, week, day
    elif has_sep:
        if text[pos:pos+3].isdecimal():
            day_of_year = text[pos:pos+3]
            pos += 3
            if pos < len(text):
                raise ValueError(f'trailing garbage in string: {text[pos:]}')
            return year, day_of_year
        else:
            month = int(text[pos:pos+2])
            pos += 2
            if has_sep and text[pos] != '-':
                raise ValueError('Inconsistent usage of separator')
            pos += 1
            day = int(text[pos:pos+2])
            pos += 2
            if pos < len(text):
                raise ValueError(f'trailing garbage in string: {text[pos:]}')
            return year, month, day

def iso_calendar(text: str):
    try:
        year = int(text[0:4])
    except ValueError:
        raise ValueError('year must be four digits') from None
    has_sep = text[4] == '-'
    pos = 4 + has_sep
    if has_sep:
        month = int(text[pos:pos+2])
        pos += 2
        if pos >= len(text):
            return year, month
        if has_sep and text[pos] != '-':
            raise ValueError(f'Expected separator but got:', f'{text[pos]}')
        pos += 1
        day = int(text[pos:pos+2])
        pos += 2
        if pos < len(text):
            raise ValueError(f'trailing garbage in string:', f'{text[pos:]}')
    else:
        month = int(text[pos:pos+2])
        pos += 2
        if pos >= len(text):
            raise SyntaxError('missing days')
        day = int(text[pos:pos+2])
        pos += 2
        if pos < len(text):
            raise ValueError(f'trailing garbage in string:', f'{text[pos:]}')
    return year, month, day

def iso_week(text: str):
    try:
        year = int(text[0:4])
    except ValueError:
        raise ValueError('year must be four digits') from None
    has_sep = text[4] == '-'
    pos = 4 + has_sep
    if text[pos] != 'W':
        raise SyntaxError('Expected week indicator')
    pos += 1
    if has_sep:
        week = int(text[pos:pos+2])
        pos += 2
        if pos >= len(text):
            return year, week
        if has_sep and text[pos] != '-':
            raise ValueError(f'Expected separator but got:', f'{text[pos]}')
        pos += 1
    else:
        week = int(text[pos:pos+2])
        pos += 2
        if pos >= len(text):
            return year, week
    day = int(text[pos:pos+2])
    pos += 2
    if pos < len(text):
        raise ValueError(f'trailing garbage in string:', f'{text[pos:]}')
    return year, week, day


def iso_ordinal(text: str):
    if not len(text) in (6,7):
        raise SyntaxError('wrong format')
    try:
        year = int(text[0:4])
    except ValueError:
        raise ValueError('year must be four digits') from None
    has_sep = text[4] == '-'
    pos = 4 + has_sep
    try:
        day_of_year = int(text[pos:pos+3])
        pos += 3
    except ValueError:
        raise ValueError('ordinal must be three digits') from None
    if pos < len(text):
        raise ValueError(f'trailing garbage in string:', f'{text[pos:]}')
    return year, day_of_year



def parse_iso_duration(cls, data: str):
    if data[0] not in 'Pp':
        raise ValueError('A valid duration starts with P')

    if 'T' in data:
        period, sep, time = data[1:].partition('T')
    else:
        period, sep, time = data[1:].partition('t')

    unit_found = False
    result = {}

    period_dict = (('Y', 'year'), ('M', 'month'), ('W', 'week'), ('D', 'day'))
    time_dict = (('H', 'hour'), ('M', 'min'), ('S', 'sec'))
    for unit, name in period_dict.items():
        try:
            unit_pos = next(index for index, char in enumerate(period) if char.upper() == unit)
            unit_value = int(period[:unit_pos])
            result[name] = unit_value
            period = period[unit_pos + 1:]
            unit_found = True
        except StopIteration:
            result[name] = 0
        except ValueError:
            raise ValueError(
                f'{unit_value} contains non-numeric characters') from None

    if period:
        raise ValueError(f'Trailing garbage in period: {period}')

    for unit, name in time_dict.items():
        try:
            unit_pos = next(index for index, char in enumerate(time) if char.upper() == unit)
            unit_value = int(time[:unit_pos])
            result[name] = unit_value
            time = time[unit_pos + 1:]
            unit_found = True
        except StopIteration:
            result[name] = 0
        except ValueError:
            raise ValueError(
                f'{unit_value} contains non-numeric characters') from None

    if time:
        raise ValueError(f'Trailing garbage in time: {time}')

    if 'week' in result.keys(): # Insufficient test. Need to check presence of week earlier instead
        temp_dict = {key: value \
                    for key, value in result.items() if key != 'week'}
        if sum(temp_dict.values()) > 0:
            raise ValueError('Week is not allowed with other units')

    if not unit_found:
        raise ValueError('At least one unit needs to be provided')

    # if sum(result.values()) == 0: # This method does not allow valid formats such as PT0S
    #     raise ValueError('At least one unit needs to be provided')

    return data, result