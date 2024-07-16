def is_positive_number(value):
    try:
        number_string: float = float(value)

    # except Exception as e
        # print(e.__class__.__name__)
    except ValueError:
        return False

    return number_string > 0
