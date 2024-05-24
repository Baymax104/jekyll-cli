# -*- coding: UTF-8 -*-
import argparse
import importlib
import inspect
import os

import argcomplete
from ruamel import yaml

from command import Command


class BlogParser(object):

    def __init__(self, root_dir):
        # init parser
        self.parser = argparse.ArgumentParser(prog='blog', description='jekyll blog CLI tool.')
        subparsers = self.parser.add_subparsers(dest='command', title='commands')

        # read config
        with open('../config.yml', 'r') as f:
            config = yaml.safe_load(f)

        # import basic commands
        self.__import_basic_commands(subparsers, root_dir, config)

        # import git commands
        self.__import_extra_commands('git_commands', subparsers, root_dir, config)

    @staticmethod
    def __import_basic_commands(subparsers, root_dir, config):
        for script in os.listdir('commands'):
            if script.endswith('.py'):
                module = importlib.import_module(f'commands.{script[:-3]}')
                for name, cls in inspect.getmembers(module):
                    if name != 'Command' and inspect.isclass(cls) and issubclass(cls, Command):
                        cls(subparsers, root_dir, config)

    @staticmethod
    def __import_extra_commands(module_name, subparsers, root_dir, config):
        module = importlib.import_module(module_name)
        if hasattr(module, 'init'):
            init = getattr(module, 'init')
            if callable(init):
                init(subparsers, root_dir, config)

    def parse(self):
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()
        if args.command is None:
            self.parser.print_help()
        else:
            args.execute(args)
