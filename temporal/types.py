""" Short Desc.

Long Description

Example:
    Ex1
    Ex2

"""

import time
from temporal.algorithms import is_leap, from_ordinal, from_unix_time, from_iso, to_ordinal, date_to_days, days_to_date
from temporal.constants import DAY_NAMES, DAY_NAMES_LONG, MONTH_NAMES, MONTH_NAMES_LONG, DAYS_IN_MONTH
from temporal.parsers import strftime


class Date:
    __slots__ = ('year', 'month', 'day')
    __match_args__ = ('year', 'month', 'day')

    def __init__(self, year: int, month: int, day: int) -> None:
        for key, value in locals().items():
            if key in ('year', 'month', 'day') and not isinstance(value, int):
                raise TypeError(f'Expected {key} to be an int', f'{value!r}')
        if not 1 <= month <= 12:
            raise ValueError(f'month must be between 1 and 12')
        if is_leap(year) and month == 2:
            max_days = 29
        else:
            max_days = DAYS_IN_MONTH.get(month)
        if not 1 <= day <= max_days:
            raise ValueError(f'day must be between 1 and {max_days}')
        object.__setattr__(self, 'year', year)
        object.__setattr__(self, 'month', month)
        object.__setattr__(self, 'day', day)

    def __repr__(self):
        cls = type(self).__name__
        return f'{cls}(year={self.year!r}, month={self.month!r}, day={self.day!r})'

    def __str__(self) -> str:
        return self.as_iso_format()

    def __eq__(self, other):
        if not isinstance(other, Date):
            return NotImplemented
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    def __le__(self, other) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return (self.year, self.month, self.day) <= (other.year, other.month, other.day)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def __ge__(self, other) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return (self.year, self.month, self.day) >= (other.year, other.month, other.day)

    def __gt__(self, other) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return (self.year, self.month, self.day) > (other.year, other.month, other.day)

    def __hash__(self):
        return hash((self.year, self.month, self.day))

    def __setattr__(self, name, value):
        raise AttributeError(f"Can't set attribute {name!r}")

    def __delattr__(self, name):
        raise AttributeError(f"Can't delete attribute {name!r}")

    def __getstate__(self):
        return (self.year, self.month, self.day)

    def __setstate__(self, state):
        fields = ('year', 'month', 'day')
        for field, value in zip(fields, state):
            object.__setattr__(self, field, value)

    def __format__(self, fmt: str):
        if not isinstance(fmt, str):
            raise TypeError(f'must be str, not {type(fmt).__name__}')
        if len(fmt) != 0:
            return self.as_strftime(fmt)
        return str(self)

    def __reduce__(self):
        # Only necessary if Pickle is to be supported
        pass

    def __add__(self, other) -> bool:
        # Need the TimeDelta Object
        pass

    __radd__ = __add__

    def __sub__(self, other) -> bool:
        # Need the TimeDelta Object
        pass

    def __iter__(self):
        yield from (self.year, self.month, self.day)

    # Additional Constructors
    @classmethod
    def from_timestamp(cls, seconds: int) -> 'Date':
        "Construct a date from a POSIX timestamp."
        days = int(seconds // 86400)
        year, month, day, *_ = from_unix_time(days)
        return Date(year, month, day)
    
    @classmethod
    def today(cls) -> 'Date':
        "Construct a date from time.time()."
        seconds_since_epoch = time.time()
        return cls.from_timestamp(seconds_since_epoch)

    @classmethod
    def from_ordinal(cls, days: int) -> 'Date':
        """Construct a date from a proleptic Gregorian ordinal.
        0001-01-01 is day 1. Only the year, month and day are
        non-zero in the result.
        """
        year, month, day = from_ordinal(days)
        return cls(year, month, day)

    @classmethod
    def from_iso_format(cls, date: str) -> 'Date':
        # https://en.wikipedia.org/wiki/ISO_8601#Calendar_dates
        pass

    @classmethod
    def from_iso_calendar(cls, year: int, week: int, day: int) -> 'Date':
        days = (week - 1) * 7 + day
        days += date_to_days(year,1,1)
        year, month, day = days_to_date(days)
        return Date(year, month, day)

    @classmethod
    def from_iso_date(cls, days: int) -> 'Date':
        "Construct a date from days from ISO. 0000-01-01 is day 0."
        year, month, day = from_iso(days)
        return Date(year, month, day)

    # Format methods
    def as_iso_format(self) -> str:
        return f'{self.year:04}-{self.month:02}-{self.day:02}'

    def as_ordinal(self) -> int:
        """Return proleptic Gregorian ordinal for the year, month and day.
        January 1 of year 1 is day 1.  Only the year, month and day values
        contribute to the result.
        """
        return to_ordinal(*self)

    def as_ctime(self) -> str:
         "Return ctime style string."
         weekday = DAY_NAMES[self.iso_weekday() - 1]
         month = MONTH_NAMES[self.month - 1]
         return f'{weekday} {month} {self.day:02} 00:00:00 {self.year:04}'

    def as_strftime(self, text: str) -> str:
        return strftime(self, text)

    def as_time_tuple(self) -> time.struct_time:
        return time.struct_time(
            (*self, 0, 0, 0, self.weekday(), self.day_of_year(), -1))

    def as_iso_calendar(self):
        # original datetime returns a instance of IsoCalendarDate
        return (self.year, self.week(), self.iso_weekday())

    # Calculation methods
    def weekday(self) -> int:
        "Return day of the week, where Monday == 0 ... Sunday == 6."
        return (self.as_ordinal() + 6) % 7

    def iso_weekday(self) -> int:
        "Return day of the week, where Monday == 1 ... Sunday == 7."
        return self.as_ordinal() % 7 or 7

    def day_of_year(self) -> int:
        return date_to_days(*self) - date_to_days(self.year, 1, 1)

    def week(self) -> int:
        return self.day_of_year() // 7 + 1




# from dataclasses import dataclass


# @dataclass(frozen=True, slots=True)
# class TimeStruct:
#     year: int
#     month: int
#     day: int
#     hour: int
#     minute: int
#     second: int
#     def __iter__(self):
#         yield from (self.year, self.month, self.day)
