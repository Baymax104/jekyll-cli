# -*- coding: UTF-8 -*-
import fnmatch
import os

from utils import get_file_completer


class OpenCommand(object):

    def __init__(self, subparsers, root_dir, config):
        self.root_dir = root_dir
        self.post_dir = os.path.join(root_dir, '_posts')
        self.draft_dir = os.path.join(root_dir, '_drafts')
        self.config = config

        self.parser = subparsers.add_parser('open', help='open post or draft in editor.', aliases=['o'])
        open_action = self.parser.add_argument('filename', help='post or draft filename.', type=str)
        open_action.completer = get_file_completer(root_dir, 'both')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        filename: str = args.filename

        if not filename.endswith('.md'):
            filename += '.md'

        # find file in _drafts
        file = os.path.join(self.draft_dir, filename)
        if os.path.isfile(file):
            os.system(f'start {file}')
            return

        # find file in _posts
        for file in os.listdir(self.post_dir):
            if fnmatch.fnmatch(file, f'*{filename}*'):
                os.system(f'start {os.path.join(self.post_dir, file)}')
                return

        # not exist
        print(f'No such file named {filename}\n')
