# -*- coding: UTF-8 -*-
import ast
from pathlib import Path
from typing import Any, Tuple, Dict

from ruamel.yaml import YAML


def read_markdown(md_file: Path) -> Tuple[Dict[str, Any], str]:
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # split the content
    parts = content.split('---\n', maxsplit=2)
    yaml = YAML(pure=True)
    yaml_formatter = yaml.load(parts[1])
    article = parts[2]
    return yaml_formatter, article


def write_markdown(md_file: Path, yaml_formatter: Dict[str, Any], article: str):
    yaml = YAML(pure=True)
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(yaml_formatter, f)
        f.write('---\n')
        f.write(article)


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
