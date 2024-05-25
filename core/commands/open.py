# -*- coding: UTF-8 -*-
import os

from command import Command
from utils import get_file_completer, find_matched_file


class OpenCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(subparsers, root_dir, config)
        self.parser = subparsers.add_parser('open', help='open post or draft in editor.', aliases=['o'])
        open_action = self.parser.add_argument('filename', help='post or draft filename.', type=str)
        open_action.completer = get_file_completer(root_dir, 'both')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        filename: str = args.filename

        # find matched file and open it
        for directory in [self.post_dir, self.draft_dir]:
            opened_file = find_matched_file(directory, filename)
            if opened_file is not None:
                opened_file = os.path.join(directory, opened_file)
                print(f'Opening {opened_file}')
                os.system(f'start {opened_file}')
                return

        # not exist
        print(f'No such file: {filename}\n')
