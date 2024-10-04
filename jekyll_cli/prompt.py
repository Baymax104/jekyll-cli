# -*- coding: UTF-8 -*-
from pathlib import Path
from typing import List, Any, Dict

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
from rich.console import Console
from rich.progress import Progress as _Progress, SpinnerColumn, TextColumn
from rich.table import Table

__console = Console()
print = __console.print
rule = __console.rule


def print_table(items: List[Any]):
    if not items:
        return
    table = Table(show_header=False)
    table.add_column()
    table.add_column()
    for i in range(0, len(items), 2):
        item1 = f"[bold][green][{i + 1}][/] {items[i]}"
        item2 = f"[bold][green][{i + 2}][/] {items[i + 1]}" if i + 1 < len(items) else ""
        table.add_row(item1, item2)
    print(table)


def print_info(info: Dict[str, Any]):
    table = Table(show_header=False)
    table.add_column()
    table.add_column()
    for key, value in info.items():
        table.add_row(f'[bold green]{key.capitalize()}', f'[bold]{value}')
    print(table)


class Progress:

    def __init__(self, description):
        self.progress = _Progress(SpinnerColumn(), TextColumn('{task.description}'))
        self.progress.add_task(description=description)

    def __enter__(self):
        self.progress.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()


def select_item_matches(items):
    return inquirer.select(
        message=f'Found {len(items)} matches, select one to continue:',
        choices=[Choice(value=item, name=f'[{item.type.name}] {item.name}') for item in items],
        vi_mode=True
    ).execute()


def select_mode() -> str:
    return inquirer.select(
        message='Please choose the management mode (single or item):',
        choices=[
            Choice('single', 'single (A single markdown file denotes a blog item.)'),
            Choice('item', 'item (A directory containing a markdown file and an assets directory denotes a blog item.)')
        ],
        vi_mode=True
    ).execute()


def confirm(message, default=False) -> bool:
    return inquirer.confirm(message, default=default).execute()


def input_directory_path(message) -> Path:
    return inquirer.filepath(
        message=message,
        vi_mode=True,
        only_directories=True,
        multicolumn_complete=True,
        validate=PathValidator(is_dir=True, message='Input is not a directory.'),
        filter=lambda path: Path(path).resolve()
    ).execute()
