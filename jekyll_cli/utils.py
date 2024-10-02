# -*- coding: UTF-8 -*-
import os
from pathlib import Path
from typing import Any, Tuple, Dict

from InquirerPy import prompt
from rich.console import Console
from rich.progress import Progress as _Progress, SpinnerColumn, TextColumn
from rich.table import Table
from ruamel.yaml import YAML
from typer import Exit

__console = Console()
print = __console.print
rule = __console.rule


def check_root(root_dir: str) -> str:
    if root_dir is None:
        print('BLOG_ROOT environment variable is not set')
        raise Exit(1)
    elif not os.path.isdir(root_dir):
        print('BLOG_ROOT environment variable is not a directory')
        raise Exit(1)
    else:
        return root_dir


def print_table(items):
    if len(items) == 0:
        return

    table = Table(show_header=False)
    table.add_column()
    table.add_column()
    for i in range(0, len(items), 2):
        item1 = f"[bold][green][{i + 1}][/] {items[i]}"
        item2 = f"[bold][green][{i + 2}][/] {items[i + 1]}" if i + 1 < len(items) else ""
        table.add_row(item1, item2)
    print(table)


def print_info(item):
    table = Table(show_header=False)
    table.add_column()
    table.add_column()
    table.add_row('[bold green]Name', f'[bold]{item.name}')
    table.add_row('[bold #ffb300]Type', f'[bold]{item.type.name}')
    table.add_row('[bold #006eff]Item path', f'[bold]{item.path}')
    table.add_row('[bold #006eff]Markdown file path', f'[bold]{item.file_path}')
    print(table)


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


def select_item_matches(items):
    questions = [{
        'type': 'list',
        'name': 'select',
        'message': f'Found {len(items)} matches, select one to continue:',
        'choices': items
    }]
    return prompt(questions)['select']


def confirm_removed_items(items) -> bool:
    questions = [{
        'type': 'confirm',
        'name': 'confirm',
        'message': f'Found {len(items)} matches, remove {len(items)} items:',
        'default': False
    }]
    for i, item in enumerate(items):
        print(f'{i + 1}. {item}')
    return prompt(questions)['confirm']


class Progress:

    def __init__(self, description):
        self.progress = _Progress(SpinnerColumn(), TextColumn('{task.description}'))
        self.progress.add_task(description=description)

    def __enter__(self):
        self.progress.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()
