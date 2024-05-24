# -*- coding: UTF-8 -*-
import fnmatch
import os

from utils import get_file_completer, write_markdown, read_markdown, format_print


class UnpublishCommand(object):

    def __init__(self, subparsers, root_dir, config):
        self.root_dir = root_dir
        self.post_dir = os.path.join(root_dir, '_posts')
        self.draft_dir = os.path.join(root_dir, '_drafts')
        self.config = config

        self.parser = subparsers.add_parser('unpublish', help='unpublish a post in _posts.', aliases=['unpub'])
        unpublish_action = self.parser.add_argument('filename', help='post filename in _posts.', type=str)
        unpublish_action.completer = get_file_completer(root_dir, 'post')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        filename: str = args.filename
        if not filename.endswith('.md'):
            filename += '.md'

        unpublished_file = None

        # find unpublished file
        for file in os.listdir(self.post_dir):
            if fnmatch.fnmatch(file, f'*{filename}*'):
                unpublished_file = file

        # no such file
        if unpublished_file is None:
            posts = [file for file in os.listdir(self.post_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Posts:\n')
            format_print(posts)
            print('\nNo such file in _posts.\n')
            return

        src_file = os.path.join(self.post_dir, unpublished_file)
        dest_file = os.path.join(self.draft_dir, unpublished_file.split('-', maxsplit=3)[3])

        # remove the date in yaml formatter
        yaml_formatter, article = read_markdown(src_file)
        del yaml_formatter['date']
        write_markdown(dest_file, yaml_formatter, article)

        os.remove(src_file)
        print(f'Post "{src_file}"\nunpublished as "{dest_file}"')
