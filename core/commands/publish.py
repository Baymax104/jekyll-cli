# -*- coding: UTF-8 -*-
import os
import time

from utils import get_file_completer, write_markdown, format_print, read_markdown


class PublishCommand(object):

    def __init__(self, subparsers, root_dir, config):
        self.root_dir = root_dir
        self.post_dir = os.path.join(root_dir, '_posts')
        self.draft_dir = os.path.join(root_dir, '_drafts')
        self.config = config

        self.parser = subparsers.add_parser('publish', help='publish a draft.', aliases=['pub'])
        publish_action = self.parser.add_argument('filename', help='draft filename in _drafts.', type=str)
        publish_action.completer = get_file_completer(root_dir, 'draft')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        filename: str = args.filename
        if not filename.endswith('.md'):
            filename += '.md'

        # no such file
        if not os.path.isfile(os.path.join(self.draft_dir, filename)):
            drafts = [file for file in os.listdir(self.draft_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Drafts:\n')
            format_print(drafts)
            print('\nNo such file in _drafts.\n')
            return

        dest_file = os.path.join(self.post_dir, f'{time.strftime("%Y-%m-%d")}-{filename}')
        src_file = os.path.join(self.draft_dir, filename)

        # add date into yaml formatter
        yaml_formatter, article = read_markdown(src_file)
        yaml_formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        write_markdown(dest_file, yaml_formatter, article)

        # remove the draft file
        os.remove(src_file)
        print(f'Draft "{src_file}"\npublished as "{dest_file}"')
