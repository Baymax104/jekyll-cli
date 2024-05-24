# -*- coding: UTF-8 -*-

from git import Repo

from command import Command


class GitStatusCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(subparsers, root_dir, config)
        self.parser = subparsers.add_parser('status', help='show blog git status')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        print(self.root_dir)
