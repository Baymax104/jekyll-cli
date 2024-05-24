# -*- coding: UTF-8 -*-
import os

from utils import format_print


class ListCommand(object):

    def __init__(self, subparsers, root_dir, config):
        self.root_dir = root_dir
        self.post_dir = os.path.join(root_dir, '_posts')
        self.draft_dir = os.path.join(root_dir, '_drafts')
        self.config = config

        self.parser = subparsers.add_parser('list', help='list all posts and drafts.', aliases=['l'])
        self.parser.add_argument('-d', '--draft', help='list all drafts.', action='store_true')
        self.parser.add_argument('-p', '--post', help='list all posts.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        if args.post or (not args.post and not args.draft):
            # print posts
            posts = [file for file in os.listdir(self.post_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Posts:\n')
            format_print(posts)

        if args.draft or (not args.post and not args.draft):
            # print drafts
            drafts = [file for file in os.listdir(self.draft_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Drafts:\n')
            format_print(drafts)
