# -*- coding: UTF-8 -*-

import argparse
import os

import argcomplete
from argcomplete import completers


class BlogArgumentParser:

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.parser = argparse.ArgumentParser(prog='blog',
                                              description='jekyll blog management tool.')
        subparsers = self.parser.add_subparsers(dest='command', title='commands')

        # serve command parser
        serve_parser = subparsers.add_parser('serve', help='start blog server locally through jekyll.', aliases=['s'])
        serve_parser.add_argument('-d', '--draft', help='start blog server with drafts.', action='store_true')

        # list command parser
        subparsers.add_parser('list', help='list all posts and drafts.', aliases=['l'])

        # open command parser
        open_parser = subparsers.add_parser('open', help='open post or draft in editor.', aliases=['o'])
        open_action = open_parser.add_argument('filename', help='post or draft filename.', type=str)
        open_action.completer = self.__get_file_completer('both')

        # draft command parser
        draft_parser = subparsers.add_parser('draft', help='create a draft in _drafts.', aliases=['d'])
        draft_parser.add_argument('filename', help='draft filename.', type=str)

        # post command parser
        post_parser = subparsers.add_parser('post', help='create a post in _posts.', aliases=['p'])
        post_parser.add_argument('filename', help='post filename.', type=str)

        # publish command parser
        publish_parser = subparsers.add_parser('publish', help='publish a draft.', aliases=['pub'])
        publish_action = publish_parser.add_argument('filename', help='draft filename in _drafts.', type=str)
        publish_action.completer = self.__get_file_completer('draft')

        # unpublish command parser
        unpublish_parser = subparsers.add_parser('unpublish', help='unpublish a post in _posts.', aliases=['unpub'])
        unpublish_action = unpublish_parser.add_argument('filename', help='post filename in _posts.', type=str)
        unpublish_action.completer = self.__get_file_completer('post')

    def __get_file_completer(self, option):
        root_dir = self.root_dir

        if option == 'post':
            return completers.ChoicesCompleter(
                [file for file in os.listdir(os.path.join(root_dir, '_posts')) if file.endswith('.md')])
        elif option == 'draft':
            return completers.ChoicesCompleter(
                [file for file in os.listdir(os.path.join(root_dir, '_drafts')) if file.endswith('.md')])
        elif option == 'both':
            posts = [file for file in os.listdir(os.path.join(root_dir, '_posts')) if file.endswith('.md')]
            drafts = [file for file in os.listdir(os.path.join(root_dir, '_drafts')) if file.endswith('.md')]
            posts.extend(drafts)
            return completers.ChoicesCompleter(posts)

        return None

    def parse(self):
        argcomplete.autocomplete(self.parser)
        return self.parser.parse_args()

    def help(self):
        self.parser.print_help()
