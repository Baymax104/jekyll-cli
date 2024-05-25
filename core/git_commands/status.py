# -*- coding: UTF-8 -*-

from git import Repo

from command import Command
from utils import format_print


class GitStatusCommand(Command):

    def __init__(self, subparsers, root_dir, config, repo: Repo):
        super().__init__(subparsers, root_dir, config)
        self.repo = repo
        self.parser = subparsers.add_parser('status', help='show blog git status', aliases=['s'])
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        untracked_files = self.repo.untracked_files
        modified_files = [item.a_path for item in self.repo.index.diff(None)]
        staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]

        print('\nBlog git status:')

        print('-' * 100)
        print('Untracked files:\n')
        if len(untracked_files) > 0:
            format_print(untracked_files)
        else:
            print('No untracked files.')

        print('-' * 100)
        print('Modified files:\n')
        if len(modified_files) > 0:
            format_print(modified_files)
        else:
            print('No modified files.')

        print('-' * 100)
        print('Staged files:\n')
        if len(staged_files) > 0:
            format_print(staged_files)
        else:
            print('No staged files.')
        print()