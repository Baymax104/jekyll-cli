# -*- coding: UTF-8 -*-

import json
import sys


class ConfigCommand:

    def __init__(self, subparsers, config, blog):
        self.config = config
        self.blog = blog
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
        json.dump(self.config.content, sys.stdout, indent=4)

    def set_config(self, args):
        self.config.mode = args.mode
        self.blog.refresh()
