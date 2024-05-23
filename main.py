#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# -*- coding: UTF-8 -*-

import os

from blog import Blog
from parser import BlogArgumentParser


def check_root(root_dir: str) -> str:
    if root_dir is None:
        print('BLOG_ROOT environment variable is not set')
        exit(-1)
    elif not os.path.isdir(root_dir):
        print('BLOG_ROOT environment variable is not a directory')
        exit(-1)
    else:
        return root_dir


def main():

    # get blog root directory
    root_dir = check_root(os.getenv('BLOG_ROOT'))

    # parse arguments
    parser = BlogArgumentParser(root_dir)
    args = parser.parse()
    blog = Blog(args, root_dir)

    # execute
    if args.command == 'serve' or args.command == 's':
        blog.serve()
    elif args.command == 'list' or args.command == 'l':
        blog.list_all()
    elif args.command == 'open' or args.command == 'o':
        blog.open_file()
    elif args.command == 'post' or args.command == 'p':
        blog.post()
    elif args.command == 'draft' or args.command == 'd':
        blog.draft()
    elif args.command == 'publish' or args.command == 'pub':
        blog.publish()
    elif args.command == 'unpublish' or args.command == 'unpub':
        blog.unpublish()
    else:
        parser.help()


try:
    main()
except KeyboardInterrupt:
    pass  # ignored
