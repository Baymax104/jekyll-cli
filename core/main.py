#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# -*- coding: UTF-8 -*-
from blog import Blog
from parser import BlogParser

try:
    blog = Blog()
    parser = BlogParser(blog)
    parser.parse()
except KeyboardInterrupt:
    pass  # ignored
