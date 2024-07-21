# -*- coding: UTF-8 -*-
import os

from item import Item, BlogType


class PostCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog

        # post command
        self.parser = subparsers.add_parser('post', help='create a post in _posts.', aliases=['p'])
        self.parser.add_argument('name', help='post name.', type=str)
        self.parser.add_argument('-t', '--title', help='post title.', type=str)
        self.parser.add_argument('-c', '--cats', help='post categories.', nargs='*')
        self.parser.add_argument('-T', '--tags', help='post tags.', nargs='*')
        self.parser.add_argument('-o', '--open', help='open post.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

        # post and open command
        self.po_parser = subparsers.add_parser('po', help='create a post and open it.')
        self.po_parser.add_argument('name', help='post name.', type=str)
        self.po_parser.add_argument('-t', '--title', help='post title.', type=str)
        self.po_parser.add_argument('-c', '--cats', help='post categories.', nargs='*')
        self.po_parser.add_argument('-T', '--tags', help='post tags.', nargs='*')
        self.po_parser.set_defaults(execute=self.execute, open=True)

    def execute(self, args):
        item = Item(args.name, BlogType.Post)
        item.create(args)
        self.blog.add(item)
        print(f'{item.file_path} created as post successfully.')
        if args.open:
            print('Opening post...')
            os.system(f'start {item.file_path}')
