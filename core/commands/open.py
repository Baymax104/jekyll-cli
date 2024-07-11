# -*- coding: UTF-8 -*-

from argcomplete.completers import ChoicesCompleter


class OpenCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog
        self.parser = subparsers.add_parser('open', help='open post or draft in editor.', aliases=['o'])
        open_action = self.parser.add_argument('name', help='post or draft name.', type=str)
        open_action.completer = ChoicesCompleter(self.blog.articles)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        item = self.blog.find(args.name)
        if item is None:
            print(f'No such item: {args.name}\n')
            return

        print(f'Opening {item.file_path}')
        item.open()
