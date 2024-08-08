import os


def get_environ(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)


def parse_comma_str_to_list(comma_sep_str):
    if not comma_sep_str or not isinstance(comma_sep_str, str):
        return []
    return [str.strip() for str in comma_sep_str.split(',') if str]
