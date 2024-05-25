# -*- coding: UTF-8 -*-
import os

from command import Command
from utils import find_matched_file, get_file_completer


class RemoveCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(subparsers, root_dir, config)
        self.parser = subparsers.add_parser('remove', help='remove a post or draft', aliases=['r'])
        action = self.parser.add_argument('filename', help='post or draft filename', type=str)
        action.completer = get_file_completer(root_dir, 'both')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        filename: str = args.filename

        # find matched file and open it
        for directory in [self.post_dir, self.draft_dir]:
            removed_file = find_matched_file(directory, filename)
            if removed_file is not None:
                removed_file = os.path.join(directory, removed_file)
                os.remove(removed_file)
                print(f'{removed_file} removed successfully.')
                return

        print(f'No such file: {removed_file}')
