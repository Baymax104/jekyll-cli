# -*- coding: UTF-8 -*-
from argcomplete import ChoicesCompleter

from item import BlogType


class InfoCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog
        self.parser = subparsers.add_parser('info', help='show info about post or draft.', aliases=['i'])
        action = self.parser.add_argument('name', help='post or draft name.', type=str)
        action.completer = ChoicesCompleter(self.blog.articles)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        item = self.blog.find(args.name)
        if not item:
            print('No such item.')
            return

        print(f'Info: {item.name}')
        print('-' * 100)
        print(f'Name: {item.name}')
        print(f'Type: {"post" if item.type == BlogType.Post else "draft"}')
        print(f'Item path: {item.path}')
        print(f'Markdown file path: {item.file_path}')
        print('-' * 100)
