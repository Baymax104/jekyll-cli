# -*- coding: UTF-8 -*-
from git import Repo

from command import Command


class GitPushCommand(Command):

    def __init__(self, subparsers, root_dir, config, repo: Repo):
        super().__init__(root_dir, config)
        self.repo = repo
        self.parser = subparsers.add_parser('push', help='push changes to remote repo.')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        remote = self.repo.remote()
        info = remote.push()[0]
        print('Push info: \n')
        print(f"Reference: {info.remote_ref}")
        print(f"Summary: {info.summary}")
        print(f"Flags: {info.flags}")
        if info.flags & info.ERROR:
            print(f"Error: {info.summary}")
        elif info.flags & info.REJECTED:
            print(f"Rejected: {info.summary}")
        elif info.flags & info.UP_TO_DATE:
            print("Everything up to date.")
        elif info.flags & info.FAST_FORWARD:
            print("Fast-forward update.")
        elif info.flags & info.FORCED_UPDATE:
            print("Forced update.")
        else:
            print("Push successful.")
        print()
