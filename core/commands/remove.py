# -*- coding: UTF-8 -*-

from argcomplete import ChoicesCompleter


class RemoveCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog
        self.parser = subparsers.add_parser('remove', help='remove a post or draft', aliases=['r'])
        action = self.parser.add_argument('name', help='post or draft name', type=str)
        action.completer = ChoicesCompleter(self.blog.articles)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        item = self.blog.find(args.name)
        if not item:
            print(f'No such item: {args.name}')
            return
        item.remove()
        self.blog.remove(item)
        print(f'{item.path} removed successfully.')
