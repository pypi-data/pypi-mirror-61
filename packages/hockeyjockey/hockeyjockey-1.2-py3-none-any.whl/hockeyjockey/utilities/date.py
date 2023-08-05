"""
Constants and utility functions for working with datetimes.
"""
from datetime import datetime, timedelta
from hockeyjockey import config as cfg

DATE_FMT = cfg.date.date_fmt
DATE_STR = cfg.date.date_str


def valid_date(date_str: str) -> str:
    """
    Returns a string-formatted datetime if the date_str parameter is vaild, otherwise issues a warning message to the
    user and returns None.

    :param date_str: String-formatted date.
    :return: String-formatted date if supplied date_str is valid, else None.
    """
    try:
        date_obj = datetime.strptime(date_str, DATE_FMT)
        return date_obj.strftime(DATE_FMT)
    except ValueError:
        print('Incorrect date format, should be: %s' % DATE_FMT)
        return None

def yesterday() -> str:
    """
    Calculates yesterday's date and returns it as a string-formatted date.

    :return: A date string representing yesterday's date
    """
    d = datetime.today()
    y = d - timedelta(1)
    return datetime.strftime(y, DATE_FMT)

def today() -> str:
    """
    Calculates today's date and returns it as a string-formatted date.

    :return: A date string representing today's date
    """
    d = datetime.today()
    return datetime.strftime(d, DATE_FMT)

def closest_fri_sat() -> tuple:
    """
    Calculates next Friday and Saturday's dates and returns them in a string-formatted tuple. If today is a Friday or a
    Saturday, returns the current Friday/Saturday pair.

    :return: A tuple containing this (or closest next) Friday and Saturday's dates in string format.
    """
    d = datetime.today()
    d1, d2 = None, None

    if d.weekday() == 4:
        d1, d2 = (d, d + timedelta(1))
    elif d.weekday() == 5:
        d1, d2 = (d - timedelta(1), d)
    else:
        while d.weekday() != 4:
            d += timedelta(1)
            d1, d2 = d, d + timedelta(1)
    return datetime.strftime(d1, DATE_FMT), datetime.strftime(d2, DATE_FMT)
