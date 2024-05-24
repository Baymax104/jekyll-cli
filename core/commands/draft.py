# -*- coding: UTF-8 -*-
import os

from ruamel import yaml

from command import Command


class DraftCommand(Command):

    def __init__(self, subparsers, root_dir, config):
        super().__init__(subparsers, root_dir, config)
        self.draft_formatter = config['formatter']['draft']

        self.parser = subparsers.add_parser('draft', help='create a draft in _drafts.', aliases=['d'])
        self.parser.add_argument('filename', help='draft filename.', type=str)
        self.parser.add_argument('-t', '--title', help='draft title.', type=str)
        self.parser.add_argument('-c', '--cats', help='draft categories.', nargs='*')
        self.parser.add_argument('-T', '--tags', help='draft tags.', nargs='*')
        self.parser.add_argument('-o', '--open', help='open draft.', action='store_true')
        self.parser.set_defaults(execute=self.execute)

    def execute(self, args):
        filename: str = args.filename

        # add .md suffix
        if not filename.endswith('.md'):
            filename += '.md'

        # fill formatter
        if args.title is not None:
            self.draft_formatter['title'] = args.title

        if args.cats is not None:
            self.draft_formatter['categories'] = args.cats

        if args.tags is not None:
            self.draft_formatter['tags'] = args.tags

        # output the draft formatter
        yaml_formatter = yaml.dump(self.draft_formatter, default_flow_style=False,
                                   Dumper=yaml.RoundTripDumper, allow_unicode=True)
        with open(os.path.join(self.draft_dir, filename), 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml_formatter)
            f.write('---\n')
        print(f'{os.path.join(self.draft_dir, filename)} created as draft.')

        if args.open:
            print('Opening draft...')
            os.system(f'start {os.path.join(self.draft_dir, filename)}')
