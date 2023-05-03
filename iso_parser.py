from temporal.algorithms import date_to_days, days_to_date, from_ordinal

def week_to_days(year, days):
    days += date_to_days(year,1,1)
    return days_to_date(days)

def iso_format(text):
    year = int(text[0:4])
    week = None
    day_of_year = None
    has_sep = text[4] == '-'
    pos = 4 + has_sep
    if len(text[pos:]) == 5:
        if text[pos] == 'W':
            pos += 1
            week = int(text[pos:pos+2])
            pos += 2
            if text[pos] != '-':
                raise SyntaxError('missing hyphen')
            pos += 1
            day = int(text[pos:pos+1])
            pos += 1
        else:
            month = int(text[pos:pos+2])
            pos += 2
            if text[pos] != '-':
                raise SyntaxError('missing hyphen')
            pos += 1
            day = int(text[pos:pos+2])
            pos += 2
    elif len(text[pos:]) == 4:
        if text[pos] == 'W':
            pos += 1
            week = int(text[pos:pos+2])
            pos += 2
            day = int(text[pos:pos+1])
            pos += 1
        elif not has_sep:
            month = int(text[pos:pos+2])
            pos += 2
            day = int(text[pos:pos+2])
            pos += 2
        else:
            if text[pos] == 'W':
                pos += 1
                week = int(text[pos:pos+2])
                pos += 2
            else:
                day_of_year = int(text[pos:pos+3])
                pos += 3
    elif len(text[pos:]) == 3:
        if text[pos] == 'W':
            pos += 1
            week = int(text[pos:pos+2])
            pos += 2
        else:
            day_of_year = int(text[pos:pos+3])
            pos += 3
    elif len(text[pos:]) == 2 and has_sep:
        month = int(text[pos:pos+2])
        pos += 2
        day = None
    else:
        raise SyntaxError("can't possibly be an is format")
    if pos < len(text):
        raise SyntaxError('trailing garbage:', f'{text[pos:]}')
    if week:
        _, month, days = week_to_days(year, week*7)
        day += days
    if day_of_year:
        _, month, day = from_ordinal(day_of_year)
    return year, month, day


# YYYY-MM-DD
# YYYY-Www-D

# YYYYWwwD
# YYYYMMDD
# YYYY-DDD
# YYYY-Www

# YYYYWww
# YYYYDDD

# YYYY-MM
