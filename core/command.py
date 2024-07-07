# -*- coding: UTF-8 -*-
import os.path
from abc import ABC


class Command(ABC):

    def __init__(self, root_dir, config):
        self.root_dir = root_dir
        self.config = config
        self.post_dir = os.path.join(root_dir, '_posts')
        self.draft_dir = os.path.join(root_dir, '_drafts')
