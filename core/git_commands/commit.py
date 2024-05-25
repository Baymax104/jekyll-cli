# -*- coding: UTF-8 -*-
from git import Repo

from command import Command


class GitCommitCommand(Command):

    def __init__(self, subparsers, root_dir, config, repo: Repo):
        super().__init__(subparsers, root_dir, config)
        self.repo = repo
        self.parser = subparsers.add_parser('commit', help='commit the changes.')
        self.parser.add_argument('message', type=str, help='the commit message')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        commit = self.repo.index.commit(args.message)
        commited_files = commit.stats.files.keys()

        print('Files commited successfully: \n')
        for file in commited_files:
            print(file)
        print()

