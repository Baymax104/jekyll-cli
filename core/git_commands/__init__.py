# -*- coding: UTF-8 -*-

from git import Repo

from git_commands.add import GitAddCommand
from git_commands.status import GitStatusCommand


def import_commands(subparsers, root_dir, config):
    parser = subparsers.add_parser('git', help='use git commands')
    git_subparsers = parser.add_subparsers(dest='git_commands', title='git commands')
    git_repo = Repo(root_dir)

    # init commands
    GitStatusCommand(git_subparsers, root_dir, config, git_repo)
    GitAddCommand(git_subparsers, root_dir, config, git_repo)
