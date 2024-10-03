# -*- coding: UTF-8 -*-
import json
from pathlib import Path
from typing import Dict, Any

from omegaconf import OmegaConf as OC


class __Config:
    __DEFAULT_CONFIG__ = {
        'root': None,
        'mode': 'single',
        'deploy': {
            'draft': False,
            'port': 4000
        },
        'default-formatter': {
            'draft': {
                'layout': 'post',
                'title': None,
                'categories': [],
                'tags': []
            },
            'post': {
                'layout': 'post',
                'title': None,
                'categories': [],
                'tags': [],
                'date': None
            }
        }
    }

    def __init__(self):
        app_home = Path().home() / '.jekyll-cli'
        self.__config_path = app_home / 'config.yml'

        # create app home
        app_home.mkdir(exist_ok=True)

        if not self.__config_path.exists():
            # create config.yml
            self.__config = OC.create(self.__DEFAULT_CONFIG__)
            OC.save(self.__config, self.__config_path)
        else:
            # read config
            self.__config = OC.load(self.__config_path)

    @property
    def root(self) -> Path:
        root: str | None = OC.select(self.__config, 'root')
        if not root:
            raise ValueError('Key "root" is missing.')
        root: Path = Path(root)
        if not root.is_dir():
            raise ValueError('Key "root" is not a directory.')
        return root

    @property
    def mode(self) -> str:
        mode: str | None = OC.select(self.__config, 'mode')
        if not mode:
            raise ValueError('Key "mode" is missing.')
        elif mode not in ['single', 'item']:
            raise ValueError('Unexpected value of mode, it can only be "single" or "item".')
        return mode

    def get_formatter(self, type_: str) -> Dict[str, Any]:
        return self.select(f'default-formatter.{type_.lower()}', default={})

    def select(self, key, **kwargs):
        return OC.select(self.__config, key, **kwargs)

    def update(self, key, value):
        OC.update(self.__config, key, value, merge=False)
        OC.save(self.__config, self.__config_path)

    @property
    def json(self) -> str:
        return json.dumps(OC.to_container(self.__config, resolve=True))

    def __str__(self):
        return OC.to_yaml(self.__config)


Config = __Config()
