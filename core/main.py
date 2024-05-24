#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# -*- coding: UTF-8 -*-

import os

from parser import BlogParser
from utils import check_root

try:
    root_dir = check_root(os.getenv('BLOG_ROOT'))
    parser = BlogParser(root_dir)
    parser.parse()
except KeyboardInterrupt:
    pass  # ignored
