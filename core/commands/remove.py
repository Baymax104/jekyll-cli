# -*- coding: UTF-8 -*-

from argcomplete import ChoicesCompleter

from blog import Blog
from utils import confirm_removed_items


class RemoveCommand:

    def __init__(self, subparsers, blog: Blog):
        self.blog = blog
        self.parser = subparsers.add_parser('remove', help='remove a post or draft.', aliases=['r'])
        action = self.parser.add_argument('pattern', help='pattern of post or draft name.', type=str)
        action.completer = ChoicesCompleter(self.blog.articles)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        items = self.blog.find(args.pattern)

        if len(items) == 0:
            print(f'No such item: {args.pattern}')
            return

        if confirm_removed_items(items):
            for item in items:
                item.remove()
                self.blog.remove(item)
            print('Remove successfully.')
