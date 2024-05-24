# -*- coding: UTF-8 -*-

import os

from argcomplete import completers
from ruamel import yaml


def check_root(root_dir: str) -> str:
    if root_dir is None:
        print('BLOG_ROOT environment variable is not set')
        exit(-1)
    elif not os.path.isdir(root_dir):
        print('BLOG_ROOT environment variable is not a directory')
        exit(-1)
    else:
        return root_dir


def format_print(files):
    max_len = max(len(f"[{i + 1}] {file}") for i, file in enumerate(files))
    format_str = f"{{:<{max_len}}} \t\t {{}}"

    for i in range(0, len(files), 2):
        if i + 1 < len(files):
            file1 = f"[{i + 1}] {files[i]}"
            file2 = f"[{i + 2}] {files[i + 1]}"
            print(format_str.format(file1, file2))
        else:
            file1 = f"[{i + 1}] {files[i]}"
            print(file1)


def read_markdown(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # split the content
    parts = content.split('---\n', maxsplit=2)
    yaml_formatter = yaml.safe_load(parts[1])
    article = parts[2]
    return yaml_formatter, article


def write_markdown(file, yaml_formatter, article):
    yaml_formatter = yaml.dump(yaml_formatter, default_flow_style=False,
                               Dumper=yaml.RoundTripDumper, allow_unicode=True)
    with open(file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(yaml_formatter)
        f.write('---\n')
        f.write(article)


def get_file_completer(root_dir, option):
    if option == 'post':
        return completers.ChoicesCompleter(
            [file for file in os.listdir(os.path.join(root_dir, '_posts')) if file.endswith('.md')])
    elif option == 'draft':
        return completers.ChoicesCompleter(
            [file for file in os.listdir(os.path.join(root_dir, '_drafts')) if file.endswith('.md')])
    elif option == 'both':
        posts = [file for file in os.listdir(os.path.join(root_dir, '_posts')) if file.endswith('.md')]
        drafts = [file for file in os.listdir(os.path.join(root_dir, '_drafts')) if file.endswith('.md')]
        posts.extend(drafts)
        return completers.ChoicesCompleter(posts)
    return None
