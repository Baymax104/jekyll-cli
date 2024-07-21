# -*- coding: UTF-8 -*-

import os

import settings


class ServeCommand:

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('serve', help='start blog server locally through jekyll.', aliases=['s'])
        self.parser.add_argument('-d', '--draft', help='start blog server with drafts.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        os.chdir(settings.root_dir)
        command = 'bundle exec jekyll s'
        if args.draft:
            command += ' --drafts'
        os.system(command)
