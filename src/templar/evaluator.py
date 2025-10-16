from typing import Iterable, Mapping, Sequence

type Convertible = str | dict | list
type Evaluable = dict | list
type Representable = str | int | float


def evaluate_keyords(keywords: Iterable[str], values: Mapping[str, Convertible], fail: bool) -> Mapping[str, Representable]:
    """Evaluate and resolve keyword-value mappings according to provided evaluation rules.

    This function iterates over a list of keyword identifiers, attempts to evaluate 
    the corresponding objects from the `values` mapping, and returns a new mapping 
    of evaluated results. Keywords may include dotted paths (e.g., "config.option") 
    to indicate nested evaluation through `_evaluate_object`.

    Parameters
    ----------
    keywords : Iterable[str]
        A collection of keyword names to evaluate.
    values : Mapping[str, Convertible]
        A mapping of keyword names to convertible objects or values to be evaluated.
    fail : bool
        If True, raises a `ValueError` when encountering a non-representable value. 
        If False, substitutes `"N\\A"` instead.

    Returns
    -------
    Mapping[str, Representable]
        A dictionary mapping evaluated keywords to `Representable` objects or placeholder values.

    Raises
    ------
    ValueError
        If `fail` is True and a keyword value is not `Representable`.

    Notes
    -----
    - If a keyword contains a dot (e.g., `"a.b"`), the base key before the dot is used 
      to evaluate a sub-object via `_evaluate_object`.
    - Assumes the existence of `_evaluate_object` for nested path evaluation.
    """
    evaluated = {}

    for keyword in keywords:
        if keyword in values:
            val = values[keyword]
            if not isinstance(val, Representable):
                if fail:
                    raise ValueError()
                else:
                    val = r"N\A"

            evaluated[keyword] = val

        if '.' not in keyword:
            # Runs both if the keyword is in values and if it isn't
            continue

        kw, path = keyword.split('.', maxsplit=1)
        if kw not in values:
            continue

        evaluated[keyword] = _evaluate_object(values[kw], path)

    return evaluated


def _evaluate_object(obj: Evaluable, path: str, fail: bool) -> Representable:
    """Recursively resolve a dotted attribute or sequence path on an object.

    This function takes an object and a dot-delimited path (e.g., `"a.b.c"`),
    then navigates through the object's attributes or sequence indices to
    return the final resolved value. If the path cannot be fully resolved,
    it either raises an `AttributeError` or returns `"N\\A"` depending on
    the `fail` parameter.

    Parameters
    ----------
    obj : Evaluable
        The root object from which to start the attribute or sequence lookup.
    path : str
        The dot-delimited path specifying which attributes or indices to resolve.
        Example: `"data.items.0.value"`.
    fail : bool
        If `True`, raises an `AttributeError` when the path cannot be resolved.
        If `False`, returns `"N\\A"` instead.

    Returns
    -------
    Representable
        The final resolved value obtained by following the attribute or
        sequence path.

    Raises
    ------
    AttributeError
        If an attribute in the path cannot be resolved and `fail` is `True`.

    Examples
    --------
    >>> class Foo:
    ...     def __init__(self):
    ...         self.bar = {'baz': [10, 20, 30]}
    >>> f = Foo()
    >>> _evaluate_object(f, 'bar.baz.1', fail=True)
    20

    >>> _evaluate_object(f, 'bar.missing', fail=False)
    'N\\A'
    """
    for attr in path.split('.'):
        if hasattr(obj, attr):
            obj = getattr(obj, attr)
        elif attr.isnumeric() and isintance(obj, Sequence):
            obj = obj[int(attr)]

        else:
            if fail:
                raise AttributeError(f"Cannot resolve '{attr}' on {type(obj).__name__}")
            else:
                return r"N\A"

    return obj

