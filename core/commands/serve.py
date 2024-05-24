# -*- coding: UTF-8 -*-

import os

from command import Command


class ServeCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(subparsers, root_dir, config)
        self.parser = subparsers.add_parser('serve', help='start blog server locally through jekyll.', aliases=['s'])
        self.parser.add_argument('-d', '--draft', help='start blog server with drafts.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        os.chdir(self.root_dir)
        command = 'bundle exec jekyll s'
        if args.draft:
            command += ' --drafts'
        os.system(command)
