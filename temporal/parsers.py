""" Short Desc.

Long Description

Example:
    Ex1
    Ex2

"""

from temporal.constants import DAY_NAMES, DAY_NAMES_LONG, MONTH_NAMES, MONTH_NAMES_LONG


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
    pass
