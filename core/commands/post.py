# -*- coding: UTF-8 -*-
import os
import time

from ruamel.yaml import YAML

from command import Command


class PostCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(root_dir, config)
        self.post_formatter = config['formatter']['post']

        # post command
        self.parser = subparsers.add_parser('post', help='create a post in _posts.', aliases=['p'])
        self.parser.add_argument('filename', help='post filename.', type=str)
        self.parser.add_argument('-t', '--title', help='post title.', type=str)
        self.parser.add_argument('-c', '--cats', help='post categories.', nargs='*')
        self.parser.add_argument('-T', '--tags', help='post tags.', nargs='*')
        self.parser.add_argument('-o', '--open', help='open post.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

        # post and open command
        self.po_parser = subparsers.add_parser('po', help='create a post and open it.')
        self.po_parser.add_argument('filename', help='post filename.', type=str)
        self.po_parser.add_argument('-t', '--title', help='post title.', type=str)
        self.po_parser.add_argument('-c', '--cats', help='post categories.', nargs='*')
        self.po_parser.add_argument('-T', '--tags', help='post tags.', nargs='*')
        self.po_parser.set_defaults(execute=self.execute, open=True)

    def execute(self, args):
        filename: str = args.filename

        # add .md suffix
        if not filename.endswith('.md'):
            filename += '.md'

        # add date prefix
        filename = f'{time.strftime("%Y-%m-%d")}-{filename}'

        # fill current time in post_formatter
        if self.post_formatter['date'] is None:
            self.post_formatter['date'] = time.strftime("%Y-%m-%d %H:%M")

        # fill formatter
        if args.title is not None:
            self.post_formatter['title'] = args.title

        if args.cats is not None:
            self.post_formatter['categories'] = args.cats

        if args.tags is not None:
            self.post_formatter['tags'] = args.tags

        # output the post formatter
        yaml = YAML(typ='rt', pure=True)
        with open(os.path.join(self.post_dir, filename), 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(self.post_formatter, f)
            f.write('---\n')
        print(f'{os.path.join(self.post_dir, filename)} created as post successfully.')

        if args.open:
            print('Opening post...')
            os.system(f'start {os.path.join(self.post_dir, filename)}')
