# -*- coding: UTF-8 -*-
from argcomplete import ChoicesCompleter

from blog import Blog
from item import BlogType
from utils import select_item_matches


class InfoCommand:

    def __init__(self, subparsers, blog: Blog):
        self.blog = blog
        self.parser = subparsers.add_parser('info', help='show info about post or draft.', aliases=['i'])
        action = self.parser.add_argument('pattern', help='pattern of post or draft name.', type=str)
        action.completer = ChoicesCompleter(self.blog.articles)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        items = self.blog.find(args.pattern)

        if len(items) == 0:
            print('No such item.')
            return

        item = items[0] if len(items) == 1 else select_item_matches(items)
        print('-' * 100)
        print(f'Info:')
        print(f'Name: {item.name}')
        print(f'Type: {"post" if item.type == BlogType.Post else "draft"}')
        print(f'Item path: {item.path}')
        print(f'Markdown file path: {item.file_path}')
        print('-' * 100)
