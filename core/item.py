# -*- coding: UTF-8 -*-
import os.path
import re
import shutil
import time
from enum import Enum
from pathlib import Path

from ruamel.yaml import YAML

import settings
from utils import read_markdown, write_markdown


class BlogType(Enum):
    Post = '_posts'
    Draft = '_drafts'


class Item:

    def __init__(self, name: str, typ: BlogType, path: Path | None = None, file_path: Path | None = None):
        self.name = name
        self.__type = typ
        # _posts or _drafts
        self.__parent_dir = settings.root_dir / typ.value
        self.__path = path
        self.__file_path = file_path

    @property
    def type(self):
        return self.__type

    @property
    def file_path(self) -> Path | None:
        r"""
        Returns the entire pathlib.Path of item's markdown file.
        :return: the pathlib.Path object or None
        """
        if self.__file_path is not None:
            return self.__file_path
        file_dir = self.__parent_dir if settings.mode == 'single' else self.__parent_dir / self.name
        if not file_dir.exists():
            return None
        # find .md file
        file: Path | None = None
        for f in file_dir.iterdir():
            pattern = rf'^\d{{4}}-\d{{2}}-\d{{2}}-{self.name}.md$' if self.__type == BlogType.Post else rf'^{self.name}.md$'
            if re.match(pattern, f.name) and f.is_file():
                file = f
                break
        self.__file_path = file
        return self.__file_path

    @property
    def path(self) -> Path | None:
        r"""
        Return the pathlib.Path of item

        - 'single' mode: the method returns the entire Path of markdown file.
        - 'item' mode: the method returns the entire Path of the item directory.
        :return: the pathlib.Path object or None
        """
        if self.__path is not None:
            return self.__path

        item: Path | None = None
        for f in self.__parent_dir.iterdir():
            if settings.mode == 'single':
                pattern = rf'^\d{{4}}-\d{{2}}-\d{{2}}-{self.name}.md$' if self.__type == BlogType.Post else rf'^{self.name}.md$'
                if re.match(pattern, f.name) and f.is_file():
                    item = f
                    break
            else:
                pattern = rf'^{self.name}$'
                if re.match(pattern, f.name) and f.is_dir():
                    item = f
                    break
        self.__path = item
        return self.__path

    def create(self, args):
        # create item directories
        if settings.mode == 'item':
            item_dir = self.__parent_dir / self.name
            assets_dir = item_dir / 'assets'
            assets_dir.mkdir(parents=True, exist_ok=True)

        # .md file processing
        filename = self.name + '.md'
        if self.__type == BlogType.Post:
            filename = f'{time.strftime("%Y-%m-%d")}-{filename}'

        file_path = self.__parent_dir / filename if settings.mode == 'single' else self.__parent_dir / self.name / filename
        formatter = settings.config.post_formatter if self.__type == BlogType.Post else settings.config.draft_formatter

        # fill current time in post_formatter
        if self.__type == BlogType.Post and not formatter['date']:
            formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        # fill formatter
        if args.title is not None:
            formatter['title'] = args.title
        if args.cats is not None:
            formatter['categories'] = args.cats
        if args.tags is not None:
            formatter['tags'] = args.tags

        # output the formatter
        yaml = YAML(pure=True)
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
        if settings.mode == 'single':
            self.path.unlink()
        else:
            shutil.rmtree(self.path)

    def publish(self):
        if self.__type != BlogType.Draft:
            return

        if self.path is None or self.file_path is None:
            raise ValueError('Item path or file path is null.')

        src_parent_dir = self.__parent_dir
        src_path = self.path
        src_file_path = self.file_path
        dest_parent_dir = Path(str(src_parent_dir).replace('_drafts', '_posts', 1))
        dest_path = Path(str(src_path).replace('_drafts', '_posts', 1))
        dest_file_path = Path(str(src_file_path).replace('_drafts', '_posts', 1))

        # move item
        shutil.move(src_path, dest_path)
        self.__parent_dir = dest_parent_dir
        self.__path = dest_path

        # rename .md file
        post_filename = f'{time.strftime("%Y-%m-%d")}-{dest_file_path.name}'
        dest_file_path = dest_file_path.rename(dest_file_path.with_name(post_filename))
        self.__file_path = dest_file_path

        # update .md file
        formatter, article = read_markdown(dest_file_path)
        formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        write_markdown(dest_file_path, formatter, article)
        self.__type = BlogType.Post

    def unpublish(self):
        if self.__type != BlogType.Post:
            return

        if self.path is None or self.file_path is None:
            raise ValueError('Item path or file path is null.')

        src_parent_dir = self.__parent_dir
        src_path = self.path
        src_file_path = self.file_path
        dest_parent_dir = Path(str(src_parent_dir).replace('_posts', '_drafts', 1))
        dest_path = Path(str(src_path).replace('_posts', '_drafts', 1))
        dest_file_path = Path(str(src_file_path).replace('_posts', '_drafts', 1))

        # move item
        shutil.move(src_path, dest_path)
        self.__parent_dir = dest_parent_dir
        self.__path = dest_path

        # rename .md file
        draft_filename = dest_file_path.name.split('-', 3)[3]
        dest_file_path = dest_file_path.rename(dest_file_path.with_name(draft_filename))
        self.__file_path = dest_file_path

        # update .md file
        formatter, article = read_markdown(dest_file_path)
        del formatter['date']
        write_markdown(dest_file_path, formatter, article)
        self.__type = BlogType.Draft

    def __str__(self):
        return self.name
