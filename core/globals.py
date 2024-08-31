# -*- coding: UTF-8 -*-
import os
from pathlib import Path

import utils
from config import Config

root_dir = Path(utils.check_root(os.getenv('BLOG_ROOT')))
config = Config()
mode = config.mode
