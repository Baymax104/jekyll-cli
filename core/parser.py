# -*- coding: UTF-8 -*-
import argparse

import argcomplete

from blog import Blog
from commands.build import BuildCommand
from commands.config import ConfigCommand
from commands.draft import DraftCommand
from commands.info import InfoCommand
from commands.list import ListCommand
from commands.open import OpenCommand
from commands.post import PostCommand
from commands.publish import PublishCommand
from commands.remove import RemoveCommand
from commands.serve import ServeCommand
from commands.unpublish import UnpublishCommand


class BlogParser:

    def __init__(self, blog: Blog):
        # init parser
        self.parser = argparse.ArgumentParser(prog='blog', description='Jekyll blog CLI tool.')
        subparsers = self.parser.add_subparsers(dest='command', title='commands')

        # import basic commands
        ServeCommand(subparsers)
        BuildCommand(subparsers)
        ListCommand(subparsers, blog)
        OpenCommand(subparsers, blog)
        PostCommand(subparsers, blog)
        DraftCommand(subparsers, blog)
        PublishCommand(subparsers, blog)
        UnpublishCommand(subparsers, blog)
        RemoveCommand(subparsers, blog)
        InfoCommand(subparsers, blog)
        ConfigCommand(subparsers, blog)


    def parse(self):
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()
        if args.command is None:
            self.parser.print_help()
        else:
            args.execute(args)
