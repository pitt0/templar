from typing import Iterable
import re


def parse_keywords(obj: str) -> Iterable[str]:
    """Extract all unique keywords wrapped in double dashes from a string.

    A keyword is defined as any substring enclosed by `--`, for example
    `--foo--` or `--foo.bar123--`. The function returns all such keywords
    in the order they first appear. If a closing `--` is missing, the 
    substring up to the end of the string is still returned (best-effort).

    Parameters
    ----------
    obj : str
        The input string that may contain keywords wrapped in `--`.

    Returns
    -------
    Iterable[str]
        A set of unique keywords (without the surrounding `--`), preserving
        the order of first appearance.
    """
    return {m for m in re.findall(r"--(.*?)--", obj)}
