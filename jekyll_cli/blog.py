# -*- coding: UTF-8 -*-
from fnmatch import fnmatch
from typing import List

from .config import Config
from .item import Item, BlogType


class __Blog:

    def __init__(self):
        self.__post_items: List[Item] | None = None
        self.__draft_items: List[Item] | None = None

    @property
    def posts(self) -> List[Item]:
        if self.__post_items is not None:
            return self.__post_items

        post_dir = Config.root / '_posts'
        if not post_dir.is_dir():
            return []

        if Config.mode == 'item':
            item_paths = [f for f in post_dir.iterdir() if f.is_dir()]
        else:
            item_paths = [f for f in post_dir.iterdir() if f.is_file() and f.suffix == '.md']

        self.__post_items = []
        for item_path in item_paths:
            if Config.mode == 'item':
                name = item_path.name
                path = post_dir / name
            else:
                name = item_path.stem.split('-', 3)[3]
                path = item_path
            self.__post_items.append(Item(name, BlogType.Post, path))
        return self.__post_items

    @property
    def drafts(self) -> List[Item]:
        if self.__draft_items is not None:
            return self.__draft_items

        draft_dir = Config.root / '_drafts'
        if not draft_dir.is_dir():
            return []

        if Config.mode == 'item':
            item_paths = [f for f in draft_dir.iterdir() if f.is_dir()]
        else:
            item_paths = [f for f in draft_dir.iterdir() if f.is_file() and f.suffix == '.md']

        self.__draft_items = []
        for item_path in item_paths:
            if Config.mode == 'item':
                name = item_path.name
                path = draft_dir / name
            else:
                name = item_path.stem
                path = item_path
            self.__draft_items.append(Item(name, BlogType.Draft, path))
        return self.__draft_items

    @property
    def articles(self) -> List[Item]:
        return self.posts + self.drafts

    def refresh(self):
        self.__post_items = None
        self.__draft_items = None

    def find(self, pattern: str, subset: BlogType | None = None) -> List[Item]:
        match subset:
            case BlogType.Post:
                items = self.posts
            case BlogType.Draft:
                items = self.drafts
            case _:
                items = self.articles
        return [item for item in items if fnmatch(item.name, pattern)]

    def add(self, item: Item):
        if item.type == BlogType.Post:
            self.posts.append(item)
        else:
            self.drafts.append(item)

    def remove(self, item: Item):
        if item.type == BlogType.Post:
            self.posts.remove(item)
        else:
            self.drafts.remove(item)


Blog = __Blog()
