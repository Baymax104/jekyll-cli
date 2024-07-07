# -*- coding: UTF-8 -*-
import os
import time

from command import Command
from utils import get_file_completer, write_markdown, format_print, read_markdown, find_matched_file


class PublishCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(root_dir, config)
        self.parser = subparsers.add_parser('publish', help='publish a draft.', aliases=['pub'])
        publish_action = self.parser.add_argument('filename', help='draft filename in _drafts.', type=str)
        publish_action.completer = get_file_completer(root_dir, 'draft')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        filename: str = args.filename

        # find published file
        published_file = find_matched_file(self.draft_dir, filename)

        # no such file
        if published_file is None:
            drafts = [file for file in os.listdir(self.draft_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Drafts:\n')
            format_print(drafts)
            print('\nNo such file in _drafts.\n')
            return

        dest_file = os.path.join(self.post_dir, f'{time.strftime("%Y-%m-%d")}-{published_file}')
        src_file = os.path.join(self.draft_dir, published_file)

        # add date into yaml formatter
        yaml_formatter, article = read_markdown(src_file)
        yaml_formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        write_markdown(dest_file, yaml_formatter, article)

        # remove the draft file
        os.remove(src_file)
        print(f'Draft "{src_file}"\npublished as "{dest_file}"')
