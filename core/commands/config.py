# -*- coding: UTF-8 -*-
import sys

from ruamel.yaml import YAML

from command import Command


class ConfigCommand(Command):

    def __init__(self, subparsers, root_dir, config, config_path):
        super().__init__(root_dir, config)
        self.config_path = config_path
        self.parser = subparsers.add_parser('config', help='configuration command.')
        subparsers = self.parser.add_subparsers(dest='config_command', title='config commands')

        # list command
        list_parser = subparsers.add_parser('list', help='list configurations.')
        list_parser.set_defaults(execute=self.list_config)

        # set command
        set_parser = subparsers.add_parser('set', help='set configuration.')
        set_parser.add_argument('--mode', type=str, choices=['single', 'item'], help='manage mode, only single or item')
        set_parser.set_defaults(execute=self.set_config)

    def list_config(self, _):
        yaml = YAML(typ='rt', pure=True)
        with open(self.config_path, 'r') as f:
            content = yaml.load(f)
            yaml.dump(content, sys.stdout)

    def set_config(self, args):
        if args.mode is not None:
            self.config['mode'] = args.mode
            yaml = YAML(typ='rt', pure=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f)
