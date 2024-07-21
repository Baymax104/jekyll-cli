# -*- coding: UTF-8 -*-

from argcomplete import ChoicesCompleter

from item import BlogType
from utils import format_print


class PublishCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog
        self.parser = subparsers.add_parser('publish', help='publish a draft.', aliases=['pub'])
        publish_action = self.parser.add_argument('name', help='draft name in _drafts.', type=str)
        publish_action.completer = ChoicesCompleter(self.blog.drafts)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        item = self.blog.find(args.name, BlogType.Draft)
        if not item:
            print('-' * 100)
            print('Drafts:\n')
            format_print(self.blog.drafts)
            print('\nNo such item in _drafts.\n')
            return
        item.publish()
        print(f'Draft "{item.name}"\npublished as "{item.file_path}"')
