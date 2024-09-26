# -*- coding: UTF-8 -*-

from argcomplete.completers import ChoicesCompleter

from blog import Blog
from utils import select_item_matches


class OpenCommand:

    def __init__(self, subparsers, blog: Blog):
        self.blog = blog
        self.parser = subparsers.add_parser('open', help='open post or draft in editor.', aliases=['o'])
        open_action = self.parser.add_argument('pattern', help='pattern of post or draft name.', type=str)
        open_action.completer = ChoicesCompleter(self.blog.articles)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        items = self.blog.find(args.pattern)

        if len(items) == 0:
            print(f'No such item.')
            return

        item = items[0] if len(items) == 1 else select_item_matches(items)
        print(f'Opening {item.file_path}')
        item.open()
