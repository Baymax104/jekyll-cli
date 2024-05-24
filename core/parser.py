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
        list_parser = subparsers.add_parser('list', help='list all posts and drafts.', aliases=['l'])
        list_parser.add_argument('-d', '--draft', help='list all drafts.', action='store_true')
        list_parser.add_argument('-p', '--post', help='list all posts.', action='store_true')

        # open command parser
        open_parser = subparsers.add_parser('open', help='open post or draft in editor.', aliases=['o'])
        open_action = open_parser.add_argument('filename', help='post or draft filename.', type=str)
        open_action.completer = self.__get_file_completer('both')

        # draft command parser
        draft_parser = subparsers.add_parser('draft', help='create a draft in _drafts.', aliases=['d'],)
        draft_parser.add_argument('filename', help='draft filename.', type=str)
        draft_parser.add_argument('-t', '--title', help='draft title.', type=str)
        draft_parser.add_argument('-c', '--cats', help='draft categories.', nargs='*')
        draft_parser.add_argument('-T', '--tags', help='draft tags.',  nargs='*')
        draft_parser.add_argument('-o', '--open', help='open draft.', action='store_true')

        # post command parser
        post_parser = subparsers.add_parser('post', help='create a post in _posts.', aliases=['p'])
        post_parser.add_argument('filename', help='post filename.', type=str)
        post_parser.add_argument('-t', '--title', help='post title.', type=str)
        post_parser.add_argument('-c', '--cats', help='post categories.', nargs='*')
        post_parser.add_argument('-T', '--tags', help='post tags.',  nargs='*')
        post_parser.add_argument('-o', '--open', help='open post.', action='store_true')

        # do command parser
        do_parser = subparsers.add_parser('do', help='create a draft and open it.')
        do_parser.add_argument('filename', help='draft filename.', type=str)
        do_parser.add_argument('-t', '--title', help='draft title.', type=str)
        do_parser.add_argument('-c', '--cats', help='draft categories.', nargs='*')
        do_parser.add_argument('-T', '--tags', help='draft tags.', nargs='*')

        # po command parser
        po_parser = subparsers.add_parser('po', help='create a post and open it.')
        po_parser.add_argument('filename', help='post filename.', type=str)
        po_parser.add_argument('-t', '--title', help='post title.', type=str)
        po_parser.add_argument('-c', '--cats', help='post categories.', nargs='*')
        po_parser.add_argument('-T', '--tags', help='post tags.', nargs='*')

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
