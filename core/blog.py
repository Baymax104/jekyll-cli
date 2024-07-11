# -*- coding: UTF-8 -*-
import os.path
import re

from item import Item, ArticleType
from utils import root_dir, config


class Blog:

    def __init__(self):
        self.__post_items: list[Item] | None = None
        self.__draft_items: list[Item] | None = None

    @property
    def posts(self) -> list[Item]:
        if self.__post_items is not None:
            return self.__post_items

        post_dir = os.path.join(root_dir, '_posts')
        if not os.path.isdir(post_dir):
            return []

        if config.mode == 'item':
            item_names = [f for f in os.listdir(post_dir) if os.path.isdir(os.path.join(post_dir, f))]
        else:
            item_names = [f for f in os.listdir(post_dir) if
                          os.path.isfile(os.path.join(post_dir, f)) and f.endswith('.md')]
            item_names = [re.search(r'\d{4}-\d{2}-\d{2}-(.+)\.md', item).group(1) for item in item_names]

        self.__post_items = [Item(item_name, ArticleType.Post) for item_name in item_names]
        return self.__post_items

    @property
    def drafts(self) -> list[Item]:
        if self.__draft_items is not None:
            return self.__draft_items

        draft_dir = os.path.join(root_dir, '_drafts')
        if not os.path.isdir(draft_dir):
            return []

        if config.mode == 'item':
            item_names = [f for f in os.listdir(draft_dir) if os.path.isdir(os.path.join(draft_dir, f))]
        else:
            item_names = [f for f in os.listdir(draft_dir) if
                          os.path.isfile(os.path.join(draft_dir, f)) and f.endswith('.md')]
            item_names = [re.search(r'(.+)\.md', item).group(1) for item in item_names]

        self.__draft_items = [Item(item_name, ArticleType.Draft) for item_name in item_names]
        return self.__draft_items

    @property
    def articles(self) -> list[Item]:
        return self.posts + self.drafts

    def refresh(self):
        self.__post_items = None
        self.__draft_items = None

    def find(self, name: str, typ: ArticleType | None = None) -> Item | None:
        # TODO post的name会把draft的name覆盖，导致搜索不到draft
        if typ is None:
            items = self.articles
        elif typ == ArticleType.Post:
            items = self.posts
        else:
            items = self.drafts
        for item in items:
            if name in item.name:
                return item
        return None

    def add(self, item: Item):
        if item.type == ArticleType.Post:
            self.posts.append(item)
        else:
            self.drafts.append(item)

    def remove(self, item: Item):
        if item.type == ArticleType.Post:
            self.posts.remove(item)
        else:
            self.drafts.remove(item)
