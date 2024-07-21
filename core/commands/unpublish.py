# -*- coding: UTF-8 -*-

from argcomplete import ChoicesCompleter

from item import BlogType
from utils import format_print


class UnpublishCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog
        self.parser = subparsers.add_parser('unpublish', help='unpublish a post in _posts.', aliases=['unpub'])
        unpublish_action = self.parser.add_argument('name', help='post name in _posts.', type=str)
        unpublish_action.completer = ChoicesCompleter(self.blog.posts)
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        item = self.blog.find(args.name, BlogType.Post)
        if not item:
            print('-' * 100)
            print('Posts:\n')
            format_print(self.blog.posts)
            print('\nNo such file in _posts.\n')
            return
        item.unpublish()
        print(f'Post "{item.name}"\nunpublished as "{item.file_path}"')
