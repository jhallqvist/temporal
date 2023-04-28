""" Short Desc.

Long Description
    Algorithms used come from:
    https://stackoverflow.com/a/12863278
    https://web.archive.org/web/20170507133619/https://alcor.concordia.ca/~gpkatch/gdate-algorithm.html

Example:
    Ex1
    Ex2

"""

from typing import Tuple


def is_leap(year: int) -> bool:
    """Determines if the given year is a leap year.

    Args:
        year: year to classify as leap.

    Returns:
        A boolean that determines if the supplied year is a leap year.
        False means no and True means yes

    Raises:
        ValueError: Supplied year is not an integer.
    """

    if not isinstance(year, int):
        raise ValueError('Supplied year is not an integer')

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_to_date(days: int):
    """Converts days to date (Year, Month, Day).

    Args:
        days: days since 0000-03-01.

    Returns:
        A tuple where year is the first entry, month the second and
        day the third.

    Raises:
        ValueError: Supplied days is not an integer.
    """

    if not isinstance(days, int):
        raise ValueError('Supplied days is not an integer')

    year = (10000 * days + 14780) // 3652425
    ddd = days - (365 * year + year // 4 - year // 100 + year // 400)
    if (ddd < 0):
        year = year - 1
        ddd = days - (365 * year + year // 4 - year // 100 + year // 400)
    mi = (100 * ddd + 52) // 3060
    month = (mi + 2) % 12 + 1
    year = year + (mi + 2) // 12
    day = ddd - (mi * 306 + 5) // 10 + 1
    return year, month, day


def date_to_days(year: int, month: int, day: int):
    """Converts date (Year, Month, Day) to days.

    Args:
        year: The year of the date.
        month: The month of the date.
        day: The day of the date.

    Returns:
        An integer representing the amount of days that has passed since
        0000-03-01.

    Raises:
        ValueError: (Expected {parameter} to be an int, {parameter_value})
    """

    for key, value in locals().items():
        if key in ('year', 'month', 'day') and not isinstance(value, int):
            raise TypeError(f'Expected {key} to be an int', f'{value!r}')

    month = (month + 9) % 12
    year = year - month // 10
    return  365 * year + year // 4 - year // 100 + year // 400 \
            + (month * 306 + 5) // 10 + (day - 1)


def from_ordinal(ordinal: int):
    """Converts a gregorian ordinal to the corresponding date (Year, Month, Day).

    Args:
        ordinal: A integer value other than 0.

    Returns:
        A tuple where year is the first entry, month the second and
        day the third.

    Raises:
        ValueError: Supplied days is not an integer.
    """

    if not isinstance(ordinal, int):
        raise ValueError('Supplied days is not an integer')

    if ordinal == 0:
        raise ValueError('Ordinal can be any number except zero')
    ordinal -= ordinal >= 0
    ordinal += 306
    year, month, day = days_to_date(ordinal)
    year -= year <= 0
    return year, month, day


def to_ordinal(year: int, month: int, day: int):
    """Converts date (Year, Month, Day) to a gregorian ordinal.

    Args:
        year: The year of the date.
        month: The month of the date.
        day: The day of the date.

    Returns:
        An integer representing the amount of days that has passed since
        0001-01-01.

    Raises:
        ValueError: (Expected {parameter} to be an int, {parameter_value})
    """

    for key, value in locals().items():
        if key in ('year', 'month', 'day') and not isinstance(value, int):
            raise TypeError(f'Expected {key} to be an int', f'{value!r}')

    days = date_to_days(year, month, day)
    days -= 306
    days += 1
    return days


def from_unix_time(days: int):
    """Converts days to the corresponding date (Year, Month, Day).

    Args:
        days: A integer value other than 0.

    Returns:
        A tuple where year is the first entry, month the second and
        day the third.

    Raises:
        ValueError: Supplied days is not an integer.
    """

    if not isinstance(days, int):
        raise ValueError('Supplied days is not an integer')

    days += 719468
    return days_to_date(days)


def to_unix_time(year: int, month: int, day: int):
    """Converts date (Year, Month, Day) to days.

    Args:
        year: The year of the date.
        month: The month of the date.
        day: The day of the date.

    Returns:
        An integer representing the amount of days that has passed since
        1970-01-01.

    Raises:
        ValueError: (Expected {parameter} to be an int, {parameter_value})
    """

    for key, value in locals().items():
        if key in ('year', 'month', 'day') and not isinstance(value, int):
            raise TypeError(f'Expected {key} to be an int', f'{value!r}')

    days = date_to_days(year, month, day)
    days -= 719468
    return days


def from_iso(days: int):
    """Converts days to the corresponding date (Year, Month, Day).

    Args:
        days: A integer value other than 0.

    Returns:
        A tuple where year is the first entry, month the second and
        day the third.

    Raises:
        ValueError: Supplied days is not an integer.
    """

    if not isinstance(days, int):
        raise ValueError('Supplied days is not an integer')

    days -= 60
    return days_to_date(days)


def to_iso(year: int, month: int, day: int):
    """Converts date (Year, Month, Day) to days.

    Args:
        year: The year of the date.
        month: The month of the date.
        day: The day of the date.

    Returns:
        An integer representing the amount of days that has passed since
        0000-01-01.

    Raises:
        ValueError: (Expected {parameter} to be an int, {parameter_value})
    """

    for key, value in locals().items():
        if key in ('year', 'month', 'day') and not isinstance(value, int):
            raise TypeError(f'Expected {key} to be an int', f'{value!r}')

    days = date_to_days(year, month, day)
    days += 60
    return days
