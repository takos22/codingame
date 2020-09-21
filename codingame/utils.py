from typing import get_type_hints
from functools import wraps


def validate_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)

        all_args = dict(zip(func.__code__.co_varnames, args))
        all_args.update(kwargs.copy())

        for arg, arg_type in ((i, type(j)) for i, j in all_args.items()):
            if arg in hints:
                if not issubclass(arg_type, hints[arg]):
                    raise TypeError(
                        "Argument {0!r} needs to be of type {1.__name__!r} "
                        "(got type {2.__name__!r})".format(arg, hints[arg], arg_type)
                    )

        result = func(*args, **kwargs)

        if "return" in hints:
            if type(result) != hints["return"]:
                raise TypeError(
                    "Return value needs to be of type {0.__name__!r} "
                    "(got type {1.__name__!r})".format(hints["return"], type(result))
                )

        return result

    return wrapper
