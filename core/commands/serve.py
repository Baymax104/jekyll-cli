# -*- coding: UTF-8 -*-

import os

from global_config import Config


class ServeCommand:

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('serve', help='start blog server locally through jekyll.', aliases=['s'])
        self.parser.add_argument('-d', '--draft', help='start blog server with drafts.', action='store_true')
        self.parser.add_argument('--port', help='listen on the given port. The default is 4000.', type=int)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        os.chdir(Config.root)
        command = 'bundle exec jekyll s'
        # draft option
        if args.draft:
            command += ' --drafts'

        port = args.port if args.port else Config.port
        if port:
            command += f' --port {port}'
        os.system(command)
