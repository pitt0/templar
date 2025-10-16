from __future__ import annotations

import re

from .evaluator import Convertible, Evaluable, evaluate_keywords
from .parser import parse_template


def replace_keyword(values: Mapping[str, Evaluable]):
    def _replace(m):
        k = m.group(1)
        return values.get(k, f"--{k}--")
    return _replace

def resolve[T: Convertible](template: T, values: Mapping[str, Evaluable]) -> T:
    template_str = str(template)
    keywords = parse_template(template_str)
    values = evaluate_keywords(keywords, values)
    return re.sub(r"--(.*?)--", replace_keyword(values), template_str)
