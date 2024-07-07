# -*- coding: UTF-8 -*-
import fnmatch

from argcomplete.completers import ChoicesCompleter
from git import Repo

from command import Command


class GitAddCommand(Command):

    def __init__(self, subparsers, root_dir, config, repo: Repo):
        super().__init__(root_dir, config)
        self.repo = repo
        self.parser = subparsers.add_parser('add', help='add file(s) to staging area.')
        action = self.parser.add_argument('files', help='the file(s) to be added.', nargs='*', default=[])
        action.completer = self.__add_completer()
        self.parser.set_defaults(execute=self.execute)

    def __add_completer(self):
        modified_files = [item.a_path for item in self.repo.index.diff(None)]
        untracked_files = self.repo.untracked_files
        return ChoicesCompleter(untracked_files + modified_files)

    def execute(self, args):

        modified_files = [item.a_path for item in self.repo.index.diff(None)]
        untracked_files = self.repo.untracked_files
        changed_files = untracked_files + modified_files

        if len(args.files) == 0:
            # if there is no file indicated, add all changed files
            matched_files = changed_files
        else:
            matched_files = [changed for changed in changed_files if
                             any(fnmatch.fnmatch(changed, f'*{file}*') for file in args.files)]

        if len(matched_files) == 0 and len(args.files) > 0:
            print('No such file(s)')
            return

        self.repo.index.add(matched_files)

        print('Files added successfully: \n')
        for file in matched_files:
            print(file)
        print()
