# -*- coding: UTF-8 -*-
import os

from command import Command


class BuildCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(root_dir, config)
        self.parser = subparsers.add_parser('build', help='build jekyll site.', aliases=['b'])
        self.parser.add_argument('-d', '--draft', help='build including drafts', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        os.chdir(self.root_dir)
        command = 'bundle exec jekyll build'
        if args.draft:
            command += ' --drafts'
        os.system(command)
