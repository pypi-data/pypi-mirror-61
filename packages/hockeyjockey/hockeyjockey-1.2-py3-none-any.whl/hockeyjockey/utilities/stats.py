from functools import singledispatch


@singledispatch
def floatize(value: "unknown type") -> float:
    """
    Takes an input of unknown type and converts it to a float via single dispatch using the functions registered with
    @floatize.register(type). If the supplied type is not registered, this function is the default.

    :param value: A value of unknown type to be converted to a float.
    :return: value converted to a float.
    """
    return float(value)


@floatize.register(int)
def f2int(value: int) -> float:
    """
    Converts value of integer type to a float.

    :param value: An integer value to be converted to a float.
    :return: value converted to a float.
    """
    return float(value)


@floatize.register(str)
def f2str(value: str) -> float:
    """
    Converts value of string type to a float.

    :param value: A string value to be converted to a float.
    :return: value converted to a float.
    """
    return float(''.join(i for i in value if i.isdigit() or i == '.'))

# New statistic calculations can be added below:
def calc_pdo(shoot_pctg: float, save_pctg: float) -> float:
    """
    Calculates an advanced hockey statistic known as PDO or SPSV%.  Note: this is not a true PDO calculation
    because it is not calculated for teams at 'even strength'.

    :param shoot_pctg: A team's shooting percentage.
    :param save_pctg: A team's save percentage.
    :return: PDO (SPSV%) stat = (shoot_pctg + save_pctg * 100) * 10
    """
    return (shoot_pctg + save_pctg * 100) * 10
