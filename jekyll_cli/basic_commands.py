# -*- coding: UTF-8 -*-
from typing import Annotated, List

from typer import Typer, Option, Argument

from .blog import Blog
from .config_commands import app as config_app
from .global_config import Config
from .item import Item, BlogType
from .utils import *

app = Typer(
    no_args_is_help=True,
    help='[bold green]Jekyll Blog CLI Tool.',
    rich_markup_mode='rich'
)

app.add_typer(config_app, rich_help_panel='Configuration')


@app.command(rich_help_panel='Deployment')
def serve(
    draft: Annotated[bool, Option('--draft', '-d', help='Start blog server with drafts.')] = False,
    port: Annotated[int, Option(help='Listen on the given port.')] = Config.port
):
    """Start blog server locally through jekyll."""
    os.chdir(Config.root)
    command = 'bundle exec jekyll serve'
    # draft option
    if draft:
        command += ' --drafts'
    command += f' --port {port}'
    os.system(command)


@app.command(rich_help_panel='Deployment')
def build(draft: Annotated[bool, Option('--draft', '-d', help='Build including drafts.')] = False):
    """Build jekyll site."""
    os.chdir(Config.root)
    command = 'bundle exec jekyll build'
    if draft:
        command += ' --drafts'
    os.system(command)


@app.command(rich_help_panel='Operation')
def info(pattern: Annotated[str, Argument(help='Pattern of post or draft name.')]):
    """Show info about post or draft."""
    items = Blog.find(pattern)
    if len(items) == 0:
        print('[bold red]No such item.')
        return

    item = items[0] if len(items) == 1 else select_item_matches(items)
    rule('[bold green]Info')
    print_info(item)


@app.command(name='list', rich_help_panel='Operation')
def list_items(
    draft: Annotated[bool, Option('--draft', '-d', help='List only all drafts.')] = False,
    post: Annotated[bool, Option('--post', '-p', help='List only all posts.')] = False,
):
    """List all posts and drafts."""
    if post or (not post and not draft):
        rule('[bold green]Posts')
        print_table(Blog.posts)

    if draft or (not post and not draft):
        rule('[bold green]Drafts')
        print_table(Blog.drafts)


@app.command(name='open', rich_help_panel='Operation')
def open_item(pattern: Annotated[str, Argument(help='Pattern of post or draft name.')]):
    """Open post or draft in editor."""
    items = Blog.find(pattern)
    if len(items) == 0:
        print(f'[bold red]No such item.')
        return

    item = items[0] if len(items) == 1 else select_item_matches(items)
    with Progress(f'Opening {item.file_path}'):
        item.open()


@app.command(rich_help_panel='Operation')
def draft(
    name: Annotated[str, Argument(help='Name of draft item.')],
    title: Annotated[str, Option('--title', '-t', help='Title of draft.')] = None,
    class_: Annotated[List[str], Option('--class', '-c', help='Categories of draft.')] = None,
    tag: Annotated[List[str], Option('--tag', '-g', help='Tags of draft.')] = None,
    open_: Annotated[bool, Option('--open', '-o', help='Open draft after creation.')] = False
):
    """Create a draft."""
    item = Item(name, BlogType.Draft)
    item.create(title, class_, tag)
    Blog.add(item)
    print(f'[bold]{item.file_path} [green]created as draft successfully.')
    if open_:
        with Progress('Opening draft...'):
            item.open()


@app.command(rich_help_panel='Operation')
def post(
    name: Annotated[str, Argument(help='Name of post item.')],
    title: Annotated[str, Option('--title', '-t', help='Title of post.')] = None,
    class_: Annotated[List[str], Option('--class', '-c', help='Categories of post.')] = None,
    tag: Annotated[List[str], Option('--tag', '-g', help='Tags of post.')] = None,
    open_: Annotated[bool, Option('--open', '-o', help='Open post after creation.')] = False
):
    """Create a post."""
    item = Item(name, BlogType.Post)
    item.create(title, class_, tag)
    Blog.add(item)
    print(f'[bold]{item.file_path} [green]created as post successfully.')
    if open_:
        with Progress('Opening post...'):
            item.open()


@app.command(rich_help_panel='Operation')
def remove(pattern: Annotated[str, Argument(help='Pattern of post or draft name.')]):
    """Remove a post or draft."""
    items = Blog.find(pattern)
    if len(items) == 0:
        print(f'[bold red]No such item: {pattern}')
        return

    if confirm_removed_items(items):
        for item in items:
            item.remove()
            Blog.remove(item)
        print('[bold green]Remove successfully.')


@app.command(rich_help_panel='Operation')
def publish(pattern: Annotated[str, Argument(help='Pattern of draft name.')]):
    """Publish a draft."""
    items = Blog.find(pattern, BlogType.Draft)

    if len(items) == 0:
        rule('[bold green]Drafts')
        print_table(Blog.drafts)
        print('[bold red]No such item in _drafts.')
        return

    item = items[0] if len(items) == 1 else select_item_matches(items)
    item.publish()
    print(f'[bold green]Draft [#ffb300]"{item.name}"[/] published as [#ffb300]"{item.file_path}"[/]')


@app.command(rich_help_panel='Operation')
def unpublish(pattern: Annotated[str, Argument(help='Pattern of post name.')]):
    """Unpublish a post."""
    items = Blog.find(pattern, BlogType.Post)

    if len(items) == 0:
        rule('[bold green]Posts')
        print_table(Blog.posts)
        print('[bold red]No such item in _posts.')
        return

    item = items[0] if len(items) == 1 else select_item_matches(items)
    item.unpublish()
    print(f'[bold green]Post [#ffb300]"{item.name}"[/] unpublished as [#ffb300]"{item.file_path}"[/]')
