# -*- coding: UTF-8 -*-
import os.path
import re
import shutil
import time
from enum import Enum

from ruamel.yaml import YAML

from utils import read_markdown, write_markdown, root_dir, config


class ArticleType(Enum):
    Post = '_posts'
    Draft = '_drafts'


class Item:

    def __init__(self, name: str, typ: ArticleType):
        self.name = name
        self.__type = typ
        self.__parent_dir = os.path.join(root_dir, typ.value)
        self.__file_path = None
        self.__path = None

    @property
    def type(self):
        return self.__type

    @property
    def file_path(self) -> str | None:
        if self.__file_path is not None:
            return self.__file_path
        file_dir = self.__parent_dir if config.mode == 'single' else os.path.join(self.__parent_dir, self.name)
        if not os.path.exists(file_dir):
            return None
        # find .md file
        file = None
        for f in os.listdir(file_dir):
            pattern = rf'^\d{{4}}-\d{{2}}-\d{{2}}-{self.name}.md$' if self.__type == ArticleType.Post else rf'^{self.name}.md$'
            if re.match(pattern, f) and os.path.isfile(os.path.join(file_dir, f)):
                file = f
                break
        self.__file_path = os.path.join(file_dir, file) if file else None
        return self.__file_path

    @property
    def path(self) -> str | None:
        if self.__path is not None:
            return self.__path

        item = None
        for f in os.listdir(self.__parent_dir):
            if config.mode == 'single':
                pattern = rf'^\d{{4}}-\d{{2}}-\d{{2}}-{self.name}.md$' if self.__type == ArticleType.Post else rf'^{self.name}.md$'
                if re.match(pattern, f) and os.path.isfile(os.path.join(self.__parent_dir, f)):
                    item = f
                    break
            else:
                pattern = rf'^{self.name}$'
                if re.match(pattern, f) and os.path.isdir(os.path.join(self.__parent_dir, f)):
                    item = f
                    break
        self.__path = os.path.join(self.__parent_dir, item) if item else None
        return self.__path

    def create(self, args):
        # create item directories
        if config.mode == 'item':
            item_dir = os.path.join(self.__parent_dir, self.name)
            assets_dir = os.path.join(item_dir, 'assets')
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)

        # file processing
        filename = self.name + '.md'
        if self.__type == ArticleType.Post:
            filename = f'{time.strftime("%Y-%m-%d")}-{filename}'

        file_path = os.path.join(self.__parent_dir, filename) if config.mode == 'single' \
            else os.path.join(self.__parent_dir, self.name, filename)
        formatter = config.post_formatter if self.__type == ArticleType.Post else config.draft_formatter

        # fill current time in post_formatter
        if self.__type == ArticleType.Post and not formatter['date']:
            formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        # fill formatter
        if args.title is not None:
            formatter['title'] = args.title
        if args.cats is not None:
            formatter['categories'] = args.cats
        if args.tags is not None:
            formatter['tags'] = args.tags

        # output the formatter
        yaml = YAML(typ='rt', pure=True)
        with open(file_path, 'w') as f:
            f.write('---\n')
            yaml.dump(formatter, f)
            f.write('---\n')

    def open(self):
        if self.file_path:
            os.system(f'start {self.file_path}')

    def remove(self):
        if not self.path:
            return
        if config.mode == 'single':
            os.remove(self.path)
        else:
            shutil.rmtree(self.path)

    def publish(self):
        if self.__type != ArticleType.Draft:
            return

        src_parent_dir = self.__parent_dir
        src_path = self.path
        src_file_path = self.file_path
        dest_parent_dir = src_parent_dir.replace('_drafts', '_posts', 1)
        dest_path = src_path.replace('_drafts', '_posts', 1)
        dest_file_path = src_file_path.replace('_drafts', '_posts', 1)

        # move item
        shutil.move(src_path, dest_path)
        self.__parent_dir = dest_parent_dir
        self.__path = dest_path

        # rename .md file
        src_file_path = dest_file_path
        file_dir = os.path.dirname(src_file_path)
        src_filename = os.path.basename(src_file_path)
        dest_filename = f'{time.strftime("%Y-%m-%d")}-{src_filename}'
        dest_file_path = os.path.join(file_dir, dest_filename)
        os.rename(src_file_path, dest_file_path)
        self.__file_path = dest_file_path

        # update .md file
        formatter, article = read_markdown(dest_file_path)
        formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        write_markdown(dest_file_path, formatter, article)
        self.__type = ArticleType.Post

    def unpublish(self):
        if self.__type != ArticleType.Post:
            return

        src_parent_dir = self.__parent_dir
        src_path = self.path
        src_file_path = self.file_path
        dest_parent_dir = src_parent_dir.replace('_posts', '_drafts', 1)
        dest_path = src_path.replace('_posts', '_drafts', 1)
        dest_file_path = src_file_path.replace('_posts', '_drafts', 1)

        # move item
        shutil.move(src_path, dest_path)
        self.__parent_dir = dest_parent_dir
        self.__path = dest_path

        # rename .md file
        src_file_path = dest_file_path
        file_dir = os.path.dirname(src_file_path)
        src_filename = os.path.basename(src_file_path)
        dest_filename = src_filename.split('-', 3)[3]
        dest_file_path = os.path.join(file_dir, dest_filename)
        os.rename(src_file_path, dest_file_path)
        self.__file_path = dest_file_path

        # update .md file
        formatter, article = read_markdown(dest_file_path)
        del formatter['date']
        write_markdown(dest_file_path, formatter, article)
        self.__type = ArticleType.Draft

    def __str__(self):
        return self.name
