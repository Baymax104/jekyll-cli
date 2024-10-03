# -*- coding: UTF-8 -*-
from fnmatch import fnmatch
from typing import List, Dict

from .config import Config
from .item import Item, BlogType


class __Blog:

    def __init__(self):
        self.__post_items: Dict[str, Item] | None = None
        self.__draft_items: Dict[str, Item] | None = None

    @property
    def posts(self) -> List[Item]:
        return list(self.__post_items.values() if self.__post_items else self.__posts_dict.values())

    @property
    def drafts(self) -> List[Item]:
        return list(self.__draft_items.values() if self.__draft_items else self.__drafts_dict.values())

    @property
    def articles(self) -> List[Item]:
        return self.posts + self.drafts

    @property
    def __posts_dict(self) -> Dict[str, Item]:
        self.__post_items = self.__initialize_items(BlogType.Post)
        return self.__post_items

    @property
    def __drafts_dict(self) -> Dict[str, Item]:
        self.__draft_items = self.__initialize_items(BlogType.Draft)
        return self.__draft_items

    def refresh(self):
        self.__post_items = None
        self.__draft_items = None

    def find(self, pattern: str, subset: BlogType | None = None) -> List[Item]:
        match subset:
            case BlogType.Post:
                items = self.__posts_dict
            case BlogType.Draft:
                items = self.__posts_dict
            case _:
                items = dict(self.__posts_dict, **self.__drafts_dict)

        # precise match
        item = items.get(pattern)
        if item is not None:
            return [item]

        # fuzzy match
        return [item for name, item in items.items() if fnmatch(name, f'*{pattern}*')]

    def add(self, item: Item):
        items = self.__post_items if item.type == BlogType.Post else self.__draft_items
        if item.name in items:
            raise KeyError(f'Exists duplicated key: {item.name}.')
        items[item.name] = item

    def remove(self, item: Item):
        items = self.__post_items if item.type == BlogType.Post else self.__draft_items
        if item.name not in items:
            raise KeyError(f'Key {item.name} is missing.')
        del items[item.name]

    def __initialize_items(self, type_: BlogType) -> Dict[str, Item]:
        parent_dir = Config.root / type_.value
        if not parent_dir.is_dir():
            raise ValueError(f'{parent_dir} is not a directory.')

        if Config.mode == 'item':
            item_paths = [f for f in parent_dir.iterdir() if f.is_dir()]
        else:
            item_paths = [f for f in parent_dir.iterdir() if f.is_file() and f.suffix == '.md']

        items = {}
        for item_path in item_paths:
            name = item_path.name if Config.mode == 'item' else item_path.stem
            if name in items:
                raise KeyError(f'Exists duplicated key: {name}.')
            items[name] = Item(name, type_, item_path)
        return items


Blog = __Blog()
