# -*- coding: UTF-8 -*-

"""
Usage: blog [command] [option] [args...]
Command:
 s, serve:            start blog server locally through jekyll.
 l, list:             list all blog posts.
 o, open:             open post or draft in editor.
 d, draft:            create a draft in _drafts.
 p, post:             create a post in _posts.
 pub, publish:        publish a draft.
 unpub, unpublish:    unpublish a post.
"""

import argparse
import fnmatch
import os
import time

from ruamel import yaml


class Blog:

    def __init__(self, args: argparse.Namespace, root_dir: str) -> None:
        self.args = args
        self.root_dir = root_dir
        self.post_dir = os.path.join(root_dir, '_posts')
        self.draft_dir = os.path.join(root_dir, '_drafts')
        with open('config.yml', 'r') as f:
            config = yaml.safe_load(f)
            self.draft_formatter = config['formatter']['draft']
            self.post_formatter = config['formatter']['post']

    @staticmethod
    def __format_print(files):
        max_len = max(len(f"[{i + 1}] {file}") for i, file in enumerate(files))
        format_str = f"{{:<{max_len}}} \t\t {{}}"

        for i in range(0, len(files), 2):
            if i + 1 < len(files):
                file1 = f"[{i + 1}] {files[i]}"
                file2 = f"[{i + 2}] {files[i + 1]}"
                print(format_str.format(file1, file2))
            else:
                file1 = f"[{i + 1}] {files[i]}"
                print(file1)

    @staticmethod
    def __read_yaml_formatter(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # split the content
        parts = content.split('---\n', maxsplit=2)
        yaml_formatter = yaml.safe_load(parts[1])
        article = parts[2]
        return yaml_formatter, article

    @staticmethod
    def __write_yaml_formatter(file, yaml_formatter, article):
        yaml_formatter = yaml.dump(yaml_formatter, default_flow_style=False,
                                   Dumper=yaml.RoundTripDumper, allow_unicode=True)
        with open(file, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml_formatter)
            f.write('---\n')
            f.write(article)

    def serve(self):
        os.chdir(self.root_dir)
        command = 'bundle exec jekyll s'
        if self.args.draft:
            command += ' --drafts'
        os.system(command)

    def list_all(self):
        if self.args.post or (not self.args.post and not self.args.draft):
            # print posts
            posts = [file for file in os.listdir(self.post_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Posts:\n')
            self.__format_print(posts)

        if self.args.draft or (not self.args.post and not self.args.draft):
            # print drafts
            drafts = [file for file in os.listdir(self.draft_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Drafts:\n')
            self.__format_print(drafts)

    def open_file(self):
        filename: str = self.args.filename

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

    def post(self):
        filename: str = self.args.filename

        # add .md suffix
        if not filename.endswith('.md'):
            filename += '.md'

        # add date prefix
        date = time.strftime('%Y-%m-%d')
        filename = f'{date}-{filename}'

        # fill current time in post_formatter
        if self.post_formatter['date'] is None:
            self.post_formatter['date'] = time.strftime("%Y-%m-%d %H:%M")

        # fill formatter
        if self.args.title is not None:
            self.post_formatter['title'] = self.args.title

        if self.args.cats is not None:
            self.post_formatter['categories'] = self.args.cats

        if self.args.tags is not None:
            self.post_formatter['tags'] = self.args.tags

        # output the post formatter
        yaml_formatter = yaml.dump(self.post_formatter, default_flow_style=False,
                                   Dumper=yaml.RoundTripDumper, allow_unicode=True)
        with open(os.path.join(self.post_dir, filename), 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml_formatter)
            f.write('---\n')
        print(f'{os.path.join(self.post_dir, filename)} created as post.')

    def draft(self):
        filename: str = self.args.filename

        # add .md suffix
        if not filename.endswith('.md'):
            filename += '.md'

        # fill formatter
        if self.args.title is not None:
            self.draft_formatter['title'] = self.args.title

        if self.args.cats is not None:
            self.draft_formatter['categories'] = self.args.cats

        if self.args.tags is not None:
            self.draft_formatter['tags'] = self.args.tags

        # output the draft formatter
        yaml_formatter = yaml.dump(self.draft_formatter, default_flow_style=False,
                                   Dumper=yaml.RoundTripDumper, allow_unicode=True)
        with open(os.path.join(self.draft_dir, filename), 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml_formatter)
            f.write('---\n')
        print(f'{os.path.join(self.draft_dir, filename)} created as draft.')

    def publish(self):
        filename: str = self.args.filename
        if not filename.endswith('.md'):
            filename += '.md'

        # no such file
        if not os.path.isfile(os.path.join(self.draft_dir, filename)):
            drafts = [file for file in os.listdir(self.draft_dir) if file.endswith('.md')]
            print('-' * 100)
            print('Drafts:\n')
            self.__format_print(drafts)
            print('\nNo such file in _drafts.\n')
            return

        dest_file = os.path.join(self.post_dir, f'{time.strftime("%Y-%m-%d")}-{filename}')
        src_file = os.path.join(self.draft_dir, filename)

        # add date into yaml formatter
        yaml_formatter, article = self.__read_yaml_formatter(src_file)
        yaml_formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        self.__write_yaml_formatter(dest_file, yaml_formatter, article)

        # remove the draft file
        os.remove(src_file)
        print(f'Draft "{src_file}"\npublished as "{dest_file}"')

    def unpublish(self):
        filename: str = self.args.filename
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
            self.__format_print(posts)
            print('\nNo such file in _posts.\n')
            return

        src_file = os.path.join(self.post_dir, unpublished_file)
        dest_file = os.path.join(self.draft_dir, unpublished_file.split('-', maxsplit=3)[3])

        # remove the date in yaml formatter
        yaml_formatter, article = self.__read_yaml_formatter(src_file)
        del yaml_formatter['date']
        self.__write_yaml_formatter(dest_file, yaml_formatter, article)

        os.remove(src_file)
        print(f'Post "{src_file}"\nunpublished as "{dest_file}"')
