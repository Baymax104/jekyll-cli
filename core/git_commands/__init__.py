# -*- coding: UTF-8 -*-
import importlib
import inspect
import os

from command import Command


def init(subparsers, root_dir, config):
    parser = subparsers.add_parser('git', help='use git commands')
    git_subparsers = parser.add_subparsers(dest='git_commands', title='git commands')

    for script in os.listdir('git_commands'):
        if script.endswith('.py') and script != '__init__.py':
            module = importlib.import_module(f'{__name__}.{script[:-3]}')
            for name, cls in inspect.getmembers(module):
                if name != 'Command' and inspect.isclass(cls) and issubclass(cls, Command):
                    cls(git_subparsers, root_dir, config)
