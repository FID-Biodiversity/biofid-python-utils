from typing import Callable, Any

from django.http import QueryDict

ERROR_MESSAGE_INPUT_PARAMETER_HAS_WRONG_FORMAT = (
    'The parameter "{name}" is expected to be of type {parameter_type}!'
)


def get_from_data(
    data: QueryDict,
    name: str,
    parameter_type: Callable = None,
    is_list: bool = False,
    optional: bool = False,
    default: Any = None,
    escape_function: Callable = None
) -> Any:
    """Accesses the parameter with `name` in the `data` and returns its value.
    If the given `name` is NOT present in `data` and `optional` is True, the `default` is returned.
    :raises UserInputException: If a required parameter is not given or if a given parameter value is not of
    the required type.
    If `is_list` is True, a list of all parameters of the given `name` will be converted to `parameter_type` (if given)
    and returned in a list.
    This method does NO sanitizing, except for making sure that the requested type is given!
    """
    is_name_in_data = name in data

    if not optional and not is_name_in_data:
        raise UserInputException(f"The parameter '{name}' is missing in the request!")

    parameter_value = (
        data.get(name, default) if not is_list else data.getlist(name, default)
    )

    if parameter_value is not None and parameter_type is not None:
        try:
            if isinstance(parameter_value, list):
                parameter_value = [parameter_type(value) for value in parameter_value]
            elif parameter_type == bool:
                parameter_value = str(parameter_value).lower() in {'true', 't', '1', 'yes'}
            else:
                parameter_value = parameter_type(parameter_value)
        except ValueError:
            raise UserInputException(
                ERROR_MESSAGE_INPUT_PARAMETER_HAS_WRONG_FORMAT.format(
                    name=name, parameter_type=parameter_type.__name__
                )
            )

    if escape_function is not None:
        parameter_value = escape_function(parameter_value)

    return parameter_value


class UserInputException(Exception):
    """A dedicated exception class for errors that should be returned to the user."""

    pass
