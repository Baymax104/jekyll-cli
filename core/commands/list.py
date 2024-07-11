# -*- coding: UTF-8 -*-

from utils import format_print


class ListCommand:

    def __init__(self, subparsers, blog):
        self.blog = blog
        self.parser = subparsers.add_parser('list', help='list all posts and drafts.', aliases=['l'])
        self.parser.add_argument('-d', '--draft', help='list all drafts.', action='store_true')
        self.parser.add_argument('-p', '--post', help='list all posts.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        if args.post or (not args.post and not args.draft):
            print('-' * 100)
            print('Posts:\n')
            format_print(self.blog.posts)

        if args.draft or (not args.post and not args.draft):
            print('-' * 100)
            print('Drafts:\n')
            format_print(self.blog.drafts)
