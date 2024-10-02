# -*- coding: UTF-8 -*-
import os.path
import re
import shutil
import time
from enum import Enum
from pathlib import Path

from ruamel.yaml import YAML

from global_config import Config
from utils import read_markdown, write_markdown


class BlogType(Enum):
    Post = '_posts'
    Draft = '_drafts'


class Item:

    def __init__(self, name: str, type_: BlogType, path: Path | None = None, file_path: Path | None = None):
        self.name = name
        self.__type = type_
        # _posts or _drafts
        self.__parent_dir = Config.root / type_.value
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

        # in single mode, file_path equals to path
        if Config.mode == 'single':
            self.__file_path = self.path
            return self.__file_path

        # in item mode, path is parent path of file_path
        if not self.path:
            return None

        # find .md file for item mode
        pattern = rf'^\d{{4}}-\d{{2}}-\d{{2}}-{self.name}.md$' if self.__type == BlogType.Post else rf'^{self.name}.md$'
        matched = [f for f in self.path.iterdir() if re.match(pattern, f.name) and f.is_file()]
        self.__file_path = matched[0] if len(matched) > 0 else None
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

        item_path: Path | None = None
        for path in self.__parent_dir.iterdir():
            if Config.mode == 'single':
                pattern = rf'^\d{{4}}-\d{{2}}-\d{{2}}-{self.name}.md$' if self.__type == BlogType.Post else rf'^{self.name}.md$'
                is_type_valid = path.is_file()
            else:
                pattern = rf'^{self.name}$'
                is_type_valid = path.is_dir()
            if re.match(pattern, path.name) and is_type_valid:
                item_path = path
                break
        self.__path = item_path
        return self.__path

    def create(self, title: str = None, class_: list[str] = None, tag: list[str] = None):
        # create item directories
        if Config.mode == 'item':
            item_dir = self.__parent_dir / self.name
            assets_dir = item_dir / 'assets'
            assets_dir.mkdir(parents=True, exist_ok=True)

        # .md file processing
        filename = self.name + '.md'
        if self.__type == BlogType.Post:
            filename = f'{time.strftime("%Y-%m-%d")}-{filename}'

        file_path = self.__parent_dir / filename if Config.mode == 'single' else self.__parent_dir / self.name / filename
        formatter = Config.get_formatter(self.__type.name)

        # fill current time in post_formatter
        if self.__type == BlogType.Post and not formatter['date']:
            formatter['date'] = time.strftime("%Y-%m-%d %H:%M")
        # fill formatter
        if title is not None:
            formatter['title'] = title
        if class_ is not None:
            formatter['categories'] = class_
        if tag is not None:
            formatter['tags'] = tag

        # output the formatter
        yaml = YAML(pure=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(formatter, f)
            f.write('---\n')

    def open(self):
        if self.file_path:
            os.system(f'start {self.file_path}')

    def remove(self):
        if not self.path:
            return
        if Config.mode == 'single':
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
