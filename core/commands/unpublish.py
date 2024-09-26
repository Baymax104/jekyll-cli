# -*- coding: UTF-8 -*-

from argcomplete import ChoicesCompleter

from blog import Blog
from item import BlogType
from utils import format_print, select_item_matches


class UnpublishCommand:

    def __init__(self, subparsers, blog: Blog):
        self.blog = blog
        self.parser = subparsers.add_parser('unpublish', help='unpublish a post in _posts.', aliases=['unpub'])
        unpublish_action = self.parser.add_argument('pattern', help='pattern of post name.', type=str)
        unpublish_action.completer = ChoicesCompleter(self.blog.posts)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        items = self.blog.find(args.pattern, BlogType.Post)

        if len(items) == 0:
            print('-' * 100)
            print('Posts:\n')
            format_print(self.blog.posts)
            print('\nNo such file in _posts.\n')
            return

        item = items[0] if len(items) == 1 else select_item_matches(items)
        item.unpublish()
        print(f'Post "{item.name}"\nunpublished as "{item.file_path}"')
