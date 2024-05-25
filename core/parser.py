# -*- coding: UTF-8 -*-
import argparse
import importlib

import argcomplete
from ruamel import yaml

from commands.draft import DraftCommand
from commands.list import ListCommand
from commands.open import OpenCommand
from commands.post import PostCommand
from commands.publish import PublishCommand
from commands.remove import RemoveCommand
from commands.serve import ServeCommand
from commands.unpublish import UnpublishCommand


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
        ServeCommand(subparsers, root_dir, config)
        ListCommand(subparsers, root_dir, config)
        OpenCommand(subparsers, root_dir, config)
        PostCommand(subparsers, root_dir, config)
        DraftCommand(subparsers, root_dir, config)
        PublishCommand(subparsers, root_dir, config)
        UnpublishCommand(subparsers, root_dir, config)
        RemoveCommand(subparsers, root_dir, config)

    @staticmethod
    def __import_extra_commands(module_name, subparsers, root_dir, config):
        module = importlib.import_module(module_name)
        if hasattr(module, 'import_commands'):
            import_commands = getattr(module, 'import_commands')
            if callable(import_commands):
                import_commands(subparsers, root_dir, config)

    def parse(self):
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()
        if args.command is None:
            self.parser.print_help()
        else:
            args.execute(args)
