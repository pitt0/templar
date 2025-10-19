from __future__ import annotations

import re
from typing import Mapping

from .evaluator import Convertible, Evaluable, Representable, evaluate_keywords
from .parser import parse_template


def replace_keyword(values: Mapping[str, Representable]):
    def _replace(m):
        k = m.group(1)
        return str(values.get(k, f"--{k}--"))

    return _replace


def resolve[T: Convertible](
    template: T,
    values: Mapping[str, Evaluable],
    fail: bool = False,
) -> T:
    t_type = type(template)
    template_str = str(template)
    keywords = parse_template(template_str)
    evaluated = evaluate_keywords(keywords, values, fail)
    replaced = re.sub(r"--(.*?)--", replace_keyword(evaluated), template_str)
    return t_type(replaced)
