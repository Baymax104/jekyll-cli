# -*- coding: UTF-8 -*-
from typing import Annotated

from rich import print_json
from typer import Typer, Option

from blog import Blog
from global_config import Config
from utils import print

app = Typer(
    name='config',
    no_args_is_help=True,
    help='Configuration Subcommands.',
    rich_markup_mode='rich',
)


@app.command(name='list')
def list_config():
    """List all configurations."""
    print_json(data=Config.content)


@app.command(name='set')
def set_config(
    mode: Annotated[str, Option(help='Management mode.', )] = None,
    port: Annotated[int, Option(help='Listen on the given port.')] = 4000
):
    """Set configurations."""
    if mode is not None:
        Config.mode = mode
    if port is not None:
        Config.port = port
    Blog.refresh()
    print(f'[bold green]Configuration modified successfully.')
