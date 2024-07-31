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
        view_parser = subparsers.add_parser('view', help='view configurations.')
        view_parser.set_defaults(execute=self.view_config)

        # set command
        set_parser = subparsers.add_parser('set', help='set configuration.')
        set_parser.add_argument('--mode', type=str, choices=['single', 'item'], help='manage mode, only single or item')
        set_parser.add_argument('--port', type=int, help='listen on the given port. The default is 4000.')
        set_parser.set_defaults(execute=self.set_config)

    def view_config(self, _):
        json.dump(self.config.content, sys.stdout, indent=4)

    def set_config(self, args):
        if args.mode:
            self.config.mode = args.mode
        if args.port:
            self.config.port = args.port
        self.blog.refresh()
