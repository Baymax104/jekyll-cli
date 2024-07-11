# -*- coding: UTF-8 -*-
import os

from item import Item, ArticleType


class DraftCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog

        # draft command
        self.parser = subparsers.add_parser('draft', help='create a draft in _drafts.', aliases=['d'])
        self.parser.add_argument('name', help='draft name.', type=str)
        self.parser.add_argument('-t', '--title', help='draft title.', type=str)
        self.parser.add_argument('-c', '--cats', help='draft categories.', nargs='*')
        self.parser.add_argument('-T', '--tags', help='draft tags.', nargs='*')
        self.parser.add_argument('-o', '--open', help='open draft.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

        # draft and open command
        self.do_parser = subparsers.add_parser('do', help='create a draft and open it.')
        self.do_parser.add_argument('name', help='draft name.', type=str)
        self.do_parser.add_argument('-t', '--title', help='draft title.', type=str)
        self.do_parser.add_argument('-c', '--cats', help='draft categories.', nargs='*')
        self.do_parser.add_argument('-T', '--tags', help='draft tags.', nargs='*')
        self.do_parser.set_defaults(execute=self.execute, open=True)

    def execute(self, args):
        item = Item(args.name, ArticleType.Draft)
        item.create(args)
        self.blog.add(item)
        print(f'{item.file_path} created as draft successfully.')
        if args.open:
            print('Opening draft...')
            os.system(f'start {item.file_path}')
