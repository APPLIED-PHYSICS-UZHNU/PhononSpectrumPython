import os
from datetime import datetime

from IPython.display import display, Markdown

LOG_LEVEL = 'LOG_LEVEL'
LOG_LEVEL_HIGH = '3'
LOG_LEVEL_MEDIUM = '2'
LOG_LEVEL_LOW = '1'
LOG_LEVEL_NONE = '0'


def produce_measure_high(title_start=None):
    return produce_measure(title_start, LOG_LEVEL_HIGH)


def produce_measure_medium(title_start=None):
    return produce_measure(title_start, LOG_LEVEL_MEDIUM)


def produce_measure_low(title_start=None):
    return produce_measure(title_start, LOG_LEVEL_LOW)


def produce_measure(title_start=None, log_level=LOG_LEVEL_NONE):
    return _produce_measure(print_on, title_start, log_level)


def produce_measure_md_high(title_start=None):
    return produce_measure_md(title_start, LOG_LEVEL_HIGH)


def produce_measure_md_medium(title_start=None):
    return produce_measure_md(title_start, LOG_LEVEL_MEDIUM)


def produce_measure_md_low(title_start=None):
    return produce_measure_md(title_start, LOG_LEVEL_LOW)


def produce_measure_md(title_start=None, log_level=LOG_LEVEL_MEDIUM):
    return _produce_measure(printmd_on, title_start, log_level)


def _produce_measure(print_on_func, title_start=None, log_level=LOG_LEVEL_MEDIUM):

    start_time = datetime.now()

    def measure(title_end=None, print_out=True):
        end_time = datetime.now()

        time_diff = end_time - start_time

        if title_start is None and title_end is None:
            if print_out:
                print_on_func(f'duration = {time_diff}', log_level)

            return time_diff

        if title_start is None:
            if print_out:
                print_on_func(f'{title_end} || duration = {time_diff}', log_level)

            return time_diff

        if title_end is None:
            if print_out:
                print_on_func(f'{title_start} || duration = {time_diff}', log_level)

            return time_diff

        if print_out:
            print_on_func(f'{title_start} || {title_end} || duration = {time_diff}', log_level)

        return time_diff

    return measure


def is_log_level(log_level):
    is_level = (LOG_LEVEL in os.environ and int(os.environ[LOG_LEVEL]) >= int(log_level)) or log_level == LOG_LEVEL_NONE

    return is_level


def is_high_log_level():
    is_high = is_log_level(LOG_LEVEL_HIGH)

    return is_high


def is_medium_log_level():
    is_medium = is_log_level(LOG_LEVEL_MEDIUM)

    return is_medium


def is_low_log_level():
    is_low = is_log_level(LOG_LEVEL_LOW)

    return is_low


def is_none_log_level():
    is_none = is_log_level(LOG_LEVEL_NONE)

    return is_none


def run_on(_lambda, _lambda_else=None, log_level=LOG_LEVEL_HIGH):
    if is_log_level(log_level):
        _lambda()
    else:
        if _lambda_else is not None:
            _lambda_else()


def run_high(_lambda, _lambda_else=None):
    run_on(_lambda, _lambda_else, LOG_LEVEL_HIGH)


def run_medium(_lambda, _lambda_else=None):
    run_on(_lambda, _lambda_else, LOG_LEVEL_MEDIUM)


def run_low(_lambda, _lambda_else=None):
    run_on(_lambda, _lambda_else, LOG_LEVEL_LOW)


def printmd(string):
    display(Markdown(string))


def printmd_on(string, log_level):
    if is_log_level(log_level):
        printmd(string)


def printmd_high(string):
    if is_high_log_level():
        printmd(string)


def printmd_medium(string):
    if is_medium_log_level():
        printmd(string)


def printmd_low(string):
    if is_low_log_level():
        printmd(string)


def print_on(text, log_level):
    if is_log_level(log_level):
        print(text)


def print_high(text):
    if is_high_log_level():
        print(text)


def print_medium(text):
    if is_medium_log_level():
        print(text)


def print_low(text):
    if is_low_log_level():
        print(text)


def get_log_level():
    return os.environ[LOG_LEVEL]


def set_log_level(log_level):
    os.environ[LOG_LEVEL] = log_level


def set_log_level_NONE():
    os.environ[LOG_LEVEL] = LOG_LEVEL_NONE
    printmd(f'Log level: **NONE**')


def set_log_level_LOW():
    os.environ[LOG_LEVEL] = LOG_LEVEL_LOW
    printmd(f'Log level: **LOW**')


def set_log_level_MEDIUM():
    os.environ[LOG_LEVEL] = LOG_LEVEL_MEDIUM
    printmd(f'Log level: **MEDIUM**')


def set_log_level_HIGH():
    os.environ[LOG_LEVEL] = LOG_LEVEL_HIGH
    printmd(f'Log level: **HIGH**')


def print_action_title_description__low(title, description=""):
    run_on(lambda: print_action_title_description(title, description), log_level=LOG_LEVEL_LOW)


def print_action_title_description__medium(title, description=""):
    run_on(lambda: print_action_title_description(title, description), log_level=LOG_LEVEL_MEDIUM)


def print_action_title_description__high(title, description=""):
    run_on(lambda: print_action_title_description(title, description), log_level=LOG_LEVEL_HIGH)


def print_action_title_description(title, description=""):
    title = f'**{title}**'
    if description == "":
        printmd_low(f"{title}")
    else:
        description = f"`{description}`"
        printmd_low(f"{title}\r\n\r\n{description}")


def measure_print_action_title_description(title, description=""):
    print_action_title_description(title, description)

    return produce_measure(title)


def measure_print_action_title_description__low(title, description=""):
    print_action_title_description__low(title, description)

    return produce_measure_low(title)


def measure_print_action_title_description__medium(title, description=""):
    print_action_title_description__medium(title, description)

    return produce_measure_medium(title)


def measure_print_action_title_description__high(title, description=""):
    print_action_title_description__high(title, description)

    return produce_measure_high(title)