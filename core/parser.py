# -*- coding: UTF-8 -*-
import argparse
import importlib
import os

import argcomplete
from ruamel import yaml


class BlogParser(object):

    def __init__(self, root_dir):
        # init parser
        self.parser = argparse.ArgumentParser(prog='blog', description='jekyll blog CLI tool.')
        subparsers = self.parser.add_subparsers(dest='command', title='commands')

        # read config
        with open('../config.yml', 'r') as f:
            config = yaml.safe_load(f)

        # import commands dynamically
        for filename in os.listdir('commands'):
            if filename.endswith('.py'):
                module = importlib.import_module(f'commands.{filename[:-3]}')
                for name in dir(module):
                    cls = getattr(module, name)
                    if isinstance(cls, type):
                        cls(subparsers, root_dir, config)

    def parse(self):
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()
        if args.command is None:
            self.parser.print_help()
        else:
            args.execute(args)
