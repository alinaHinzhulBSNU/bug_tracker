from .enums import STATUS, SEVERITY


def get_choice_by_code(code, choices):
    for choice in choices:
        if choice[0] == code:
            return choice[1]


def get_choice_by_value(value, choices):
    for choice in choices:
        if choice[1] == value:
            return choice[0]


def get_status_by_code(code):
    return get_choice_by_code(code, STATUS)


def get_status_by_value(value):
    return get_choice_by_value(value, STATUS)


def get_severity_by_code(code):
    return get_choice_by_code(code, SEVERITY)


def get_severity_by_value(value):
    return get_choice_by_value(value, SEVERITY)
