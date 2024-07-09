# -*- coding: UTF-8 -*-
import os
import re

from command import Command
from utils import format_print


class ListCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(root_dir, config)
        self.parser = subparsers.add_parser('list', help='list all posts and drafts.', aliases=['l'])
        self.parser.add_argument('-d', '--draft', help='list all drafts.', action='store_true')
        self.parser.add_argument('-p', '--post', help='list all posts.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        mode = self.config['mode']
        if mode == 'single':
            self.single_action(args)
        elif mode == 'item':
            self.item_action(args)

    def single_action(self, args):
        if args.post or (not args.post and not args.draft):
            # print posts
            posts = [file for file in os.listdir(self.post_dir) if file.endswith('.md')]
            posts = [re.search(r'\d{4}-\d{2}-\d{2}-(.+)\.md', file).group(1) for file in posts]
            print('-' * 100)
            print('Posts:\n')
            format_print(posts)

        if args.draft or (not args.post and not args.draft):
            # print drafts
            drafts = [file for file in os.listdir(self.draft_dir) if file.endswith('.md')]
            drafts = [re.search(r'(.+)\.md', file).group(1) for file in drafts]
            print('-' * 100)
            print('Drafts:\n')
            format_print(drafts)

    def item_action(self, args):
        if args.post or (not args.post and not args.draft):
            # print posts
            posts = [file for file in os.listdir(self.post_dir) if os.path.isdir(os.path.join(self.post_dir, file))]
            print('-' * 100)
            print('Posts:\n')
            format_print(posts)

        if args.draft or (not args.post and not args.draft):
            # print drafts
            drafts = [file for file in os.listdir(self.draft_dir) if os.path.isdir(os.path.join(self.post_dir, file))]
            print('-' * 100)
            print('Drafts:\n')
            format_print(drafts)
