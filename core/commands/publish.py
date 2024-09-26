# -*- coding: UTF-8 -*-

from argcomplete import ChoicesCompleter

from blog import Blog
from item import BlogType
from utils import format_print, select_item_matches


class PublishCommand:

    def __init__(self, subparsers, blog: Blog):
        self.blog = blog
        self.parser = subparsers.add_parser('publish', help='publish a draft.', aliases=['pub'])
        publish_action = self.parser.add_argument('pattern', help='pattern of draft name.', type=str)
        publish_action.completer = ChoicesCompleter(self.blog.drafts)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        items = self.blog.find(args.pattern, BlogType.Draft)

        if len(items) == 0:
            print('-' * 100)
            print('Drafts:\n')
            format_print(self.blog.drafts)
            print('\nNo such item in _drafts.\n')
            return

        item = items[0] if len(items) == 1 else select_item_matches(items)
        item.publish()
        print(f'Draft "{item.name}"\npublished as "{item.file_path}"')
