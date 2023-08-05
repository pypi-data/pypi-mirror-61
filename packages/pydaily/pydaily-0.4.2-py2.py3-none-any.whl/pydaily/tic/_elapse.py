# -*- coding: utf-8 -*-

from datetime import datetime

__all__ = ["time_to_str",
           "current_time"]


def current_time():
    """ Provide current time as YYYY-MM-DD_HH-MM-SS

    Parameters
    --------
    None

    Returns
    --------
    time_str: str
        current time string

    """

    time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    return time_str


def time_to_str(delta_t, mode="min"):
    """Convert elapsed time to string representation

    Parameters
    --------
    delta_t: time difference
        Elapsed time
    mode: str
        Time representation manner, by "minitues" or "seconds".

    Returns
    --------
    delta_str: str
        Elapsed time string representation

    Examples
    --------
    >>> from timeit import default_timer as timer
    >>> start = timer()
    >>> end = timer()
    >>> elapsed_time_str = time_to_str(end - start, "min")

    """
    if mode == "min":
        t = int(delta_t) / 60
        hrs = int(t // 60)
        mins = int(t % 60)
        delta_str = "{:2d} hr {:2d} min".format(hrs, mins)
    elif mode == "sec":
        t = int(delta_t)
        mins = int(t // 60)
        sec = int(t % 60)
        delta_str = "{:2d} min {:2d} sec".format(mins, sec)
    else:
        raise NotImplementedError()

    return delta_str
