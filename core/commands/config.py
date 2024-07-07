# -*- coding: UTF-8 -*-
import sys

from ruamel.yaml import YAML

from command import Command


class ConfigCommand(Command):

    def __init__(self, subparsers, root_dir, config, config_path):
        super().__init__(root_dir, config)
        self.config_path = config_path
        self.parser = subparsers.add_parser('config', help='configuration command')
        subparsers = self.parser.add_subparsers(dest='config_command', title='config commands')

        # list command
        list_parser = subparsers.add_parser('list', help='list configuration')
        list_parser.set_defaults(execute=self.list_config)

        # set command
        set_parser = subparsers.add_parser('set', help='set configuration')
        set_parser.add_argument('kwargs', type=lambda arg: arg.split('=', 1), help='argument like "<key>=<value>"')
        set_parser.set_defaults(execute=self.set_config)

    def list_config(self, _):
        yaml = YAML(typ='rt', pure=True)
        with open(self.config_path, 'r') as f:
            content = yaml.load(f)
            yaml.dump(content, sys.stdout)

    def set_config(self, args):
        key, value = args.kwargs
        with open(self.config_path, 'a') as f:
            f.write(f'{key}: {value}\n')
        print(f'set {key}={value} successfully.')
