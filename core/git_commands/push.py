# -*- coding: UTF-8 -*-
from git import Repo

from command import Command


class GitPushCommand(Command):

    def __init__(self, subparsers, root_dir, config, repo: Repo):
        super().__init__(subparsers, root_dir, config)
        self.repo = repo
        self.parser = subparsers.add_parser('push', help='push changes to remote repo.')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        remote = self.repo.remote()
        info = remote.push()[0]
        print('Push info: \n')
        print(info.summary)
        print()
