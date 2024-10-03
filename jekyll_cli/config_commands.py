# -*- coding: UTF-8 -*-
from typing import Annotated, Any

from rich import print_json
from typer import Typer, Argument

from .blog import Blog
from .config import Config
from .utils import print, convert_literal, check_configuration

app = Typer(
    name='config',
    no_args_is_help=True,
    help='Configuration Subcommands.',
    rich_markup_mode='rich',
)


@app.command(name='list')
def list_config():
    """List all configurations."""
    print_json(Config.json)


@app.command(name='set')
def set_config(
    key: Annotated[str, Argument(help='Configuration key using dot-notation.')],
    value: Annotated[Any, Argument(help='Configuration value.', parser=convert_literal)],
):
    """Set a configuration."""
    check_configuration(key, value)
    Config.update(key, value)
    Blog.refresh()
    print(f'[bold green]Configuration modified successfully.')
