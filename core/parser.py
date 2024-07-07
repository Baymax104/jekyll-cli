# -*- coding: UTF-8 -*-
import argparse
import importlib
import os
import shutil

import argcomplete
from ruamel.yaml import YAML

from commands.build import BuildCommand
from commands.config import ConfigCommand
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
        self.parser = argparse.ArgumentParser(prog='blog', description='Jekyll blog CLI tool.')
        subparsers = self.parser.add_subparsers(dest='command', title='commands')

        # init config
        config, config_path = self.__init_config()

        # import basic commands
        self.__import_basic_commands(subparsers, root_dir, config, config_path)

    @staticmethod
    def __import_basic_commands(subparsers, root_dir, config, config_path):
        ServeCommand(subparsers, root_dir, config)
        ListCommand(subparsers, root_dir, config)
        OpenCommand(subparsers, root_dir, config)
        PostCommand(subparsers, root_dir, config)
        DraftCommand(subparsers, root_dir, config)
        PublishCommand(subparsers, root_dir, config)
        UnpublishCommand(subparsers, root_dir, config)
        RemoveCommand(subparsers, root_dir, config)
        ConfigCommand(subparsers, root_dir, config, config_path)
        BuildCommand(subparsers, root_dir, config)

    @staticmethod
    def __import_extra_commands(module_name, subparsers, root_dir, config):
        module = importlib.import_module(module_name)
        if hasattr(module, 'import_commands'):
            import_commands = getattr(module, 'import_commands')
            if callable(import_commands):
                import_commands(subparsers, root_dir, config)

    @staticmethod
    def __init_config():
        home = os.environ['USERPROFILE']
        power_jekyll_home = os.path.join(home, '.powerjekyll')
        config_path = os.path.join(power_jekyll_home, 'config.yml')

        # create app home
        if not os.path.exists(power_jekyll_home):
            os.mkdir(power_jekyll_home)

        if not os.path.exists(config_path):
            shutil.move('../config.yml.example', config_path)

        # read config
        with open(config_path, 'r') as f:
            yaml = YAML(typ='safe', pure=True)
            config = yaml.load(f)
        return config, config_path

    def parse(self):
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()
        if args.command is None:
            self.parser.print_help()
        else:
            args.execute(args)
