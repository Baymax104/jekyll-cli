# -*- coding: UTF-8 -*-
import fnmatch

from git import Repo

from command import Command


class GitAddCommand(Command):

    def __init__(self, subparsers, root_dir, config, repo: Repo):
        super().__init__(subparsers, root_dir, config)
        self.repo = repo
        self.parser = subparsers.add_parser('add', help='add file(s) to staging area.')
        self.parser.add_argument('files', help='the file(s) to be added.', nargs='*', default=[])
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):

        if len(args.files) == 0:
            # if there is no file indicated, add all untracked files
            matched_files = self.repo.untracked_files
        else:
            matched_files = [untracked for untracked in self.repo.untracked_files if
                             any(fnmatch.fnmatch(untracked, f'*{file}*') for file in args.files)]

        if len(matched_files) == 0 and len(args.files) > 0:
            print('No such file(s)')
            return

        self.repo.index.add(matched_files)

        print('Files added successfully: \n')
        for file in matched_files:
            print(file)
        print('\n')
