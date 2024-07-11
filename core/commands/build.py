# -*- coding: UTF-8 -*-
import os

from utils import root_dir


class BuildCommand:

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('build', help='build jekyll site.', aliases=['b'])
        self.parser.add_argument('-d', '--draft', help='build including drafts', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        os.chdir(root_dir)
        command = 'bundle exec jekyll build'
        if args.draft:
            command += ' --drafts'
        os.system(command)
