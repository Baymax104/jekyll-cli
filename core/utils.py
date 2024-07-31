# -*- coding: UTF-8 -*-
import os

from ruamel.yaml import YAML


def check_root(root_dir: str) -> str:
    if root_dir is None:
        print('BLOG_ROOT environment variable is not set')
        exit(-1)
    elif not os.path.isdir(root_dir):
        print('BLOG_ROOT environment variable is not a directory')
        exit(-1)
    else:
        return root_dir


def format_print(items):
    if len(items) == 0:
        return

    max_len = max(len(f"[{i + 1}] {file}") for i, file in enumerate(items))
    format_str = f"{{:<{max_len}}} \t\t {{}}"

    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            item1 = f"[{i + 1}] {items[i]}"
            item2 = f"[{i + 2}] {items[i + 1]}"
            print(format_str.format(item1, item2))
        else:
            item1 = f"[{i + 1}] {items[i]}"
            print(item1)


def read_markdown(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # split the content
    parts = content.split('---\n', maxsplit=2)
    yaml = YAML(pure=True)
    yaml_formatter = yaml.load(parts[1])
    article = parts[2]
    return yaml_formatter, article


def write_markdown(md_file, yaml_formatter, article):
    yaml = YAML(pure=True)
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(yaml_formatter, f)
        f.write('---\n')
        f.write(article)


