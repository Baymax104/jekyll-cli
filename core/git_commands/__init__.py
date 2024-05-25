# -*- coding: UTF-8 -*-
import importlib
import inspect
import os

from command import Command

from status import GitStatusCommand

from git import Repo


def import_commands(subparsers, root_dir, config):
    parser = subparsers.add_parser('git', help='use git commands')
    git_subparsers = parser.add_subparsers(dest='git_commands', title='git commands')
    git_repo = Repo(root_dir)

    # init commands
    GitStatusCommand(git_subparsers, git_repo, config, git_repo)
