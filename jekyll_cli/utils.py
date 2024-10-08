# -*- coding: UTF-8 -*-
import ast
from pathlib import Path
from typing import Any, Tuple, Dict

from ruamel.yaml import YAML


def read_markdown(md_file: Path) -> Tuple[Dict[str, Any], str]:
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---\n', maxsplit=2)
    formatter = YAML().load(parts[1]) if parts[1] else {}
    article = parts[2]
    return formatter, article


def write_markdown(md_file: Path, formatter: Dict[str, Any] = None, article: str = ''):
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        if formatter:
            YAML().dump(formatter, f)
        f.write(f'---\n{article}')


def convert_literal(value: str) -> Any:
    try:
        value = ast.literal_eval(value)
        return value
    except Exception:
        return value


def check_configuration(key: str, value: Any):
    match key:
        case 'mode':
            if not isinstance(value, str):
                raise TypeError('value must be a string.')
            if value not in ['single', 'item']:
                raise ValueError('Unexpected value of mode, it can only be "single" or "item".')
        case 'root':
            if not isinstance(value, str):
                raise TypeError('value must be a string.')
            if not Path(value).is_dir():
                raise ValueError('value must be a directory.')
        case _:
            pass
