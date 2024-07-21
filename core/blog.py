# -*- coding: UTF-8 -*-
import settings
from item import Item, BlogType


class Blog:

    def __init__(self):
        self.__post_items: list[Item] | None = None
        self.__draft_items: list[Item] | None = None

    @property
    def posts(self) -> list[Item]:
        if self.__post_items is not None:
            return self.__post_items

        post_dir = settings.root_dir / '_posts'
        if not post_dir.is_dir():
            return []

        if settings.mode == 'item':
            item_names = [f.name for f in post_dir.iterdir() if f.is_dir()]
        else:
            item_names = [f.stem.split('-', 3)[3] for f in post_dir.iterdir() if f.is_file() and f.suffix == '.md']

        self.__post_items = [Item(item_name, BlogType.Post) for item_name in item_names]
        return self.__post_items

    @property
    def drafts(self) -> list[Item]:
        if self.__draft_items is not None:
            return self.__draft_items

        draft_dir = settings.root_dir / '_drafts'
        if not draft_dir.is_dir():
            return []

        if settings.mode == 'item':
            item_names = [f.name for f in draft_dir.iterdir() if f.is_dir()]
        else:
            item_names = [f.stem for f in draft_dir.iterdir() if f.is_file() and f.suffix == '.md']

        self.__draft_items = [Item(item_name, BlogType.Draft) for item_name in item_names]
        return self.__draft_items

    @property
    def articles(self) -> list[Item]:
        return self.posts + self.drafts

    def refresh(self):
        self.__post_items = None
        self.__draft_items = None

    def find(self, name: str, subset: BlogType | None = None) -> Item | None:
        # TODO post的name会把draft的name覆盖，导致搜索不到draft
        if subset is None:
            items = self.articles
        elif subset == BlogType.Post:
            items = self.posts
        else:
            items = self.drafts
        for item in items:
            if name in item.name:
                return item
        return None

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
