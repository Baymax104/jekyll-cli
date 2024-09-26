# -*- coding: UTF-8 -*-
import os
from pathlib import Path

from ruamel.yaml import YAML

from utils import check_root


class __Config:
    __DEFAULT_CONFIG = {
        'mode': 'item',
        'port': None,  # default 4000
        'default_formatter': {
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
                'date': None  # use current time automatically if there is no value
            }
        }
    }

    def __init__(self):
        self.__root = Path(check_root(os.getenv('BLOG_ROOT')))
        power_jekyll_home = Path().home() / '.powerjekyll'
        self.__config_path = power_jekyll_home / 'config.yml'
        yaml = YAML(pure=True)

        # create app home
        if not power_jekyll_home.exists():
            power_jekyll_home.mkdir(exist_ok=True)

        # create config.yml
        if not self.__config_path.exists():
            with open(self.__config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.__DEFAULT_CONFIG, f)

        # read config
        with open(self.__config_path, 'r', encoding='utf-8') as f:
            self.__config = yaml.load(f)

    @property
    def root(self) -> Path:
        return self.__root

    @property
    def content(self) -> dict:
        return self.__config

    @property
    def mode(self) -> str:
        mode = self.__config.get('mode')
        if not mode:
            raise ValueError('Key "mode" is missing in config.yml')
        elif mode not in ['single', 'item']:
            raise ValueError('Unexpected value of mode, it can only be single or item.')
        return mode

    @mode.setter
    def mode(self, mode: str):
        self.__config['mode'] = mode
        yaml = YAML(pure=True)
        with open(self.__config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.__config, f)

    @property
    def port(self):
        return self.__config.get('port')

    @port.setter
    def port(self, port: int):
        self.__config['port'] = port
        yaml = YAML(pure=True)
        with open(self.__config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.__config, f)

    def get_formatter(self, typ: str):
        formatter = self.__config.get('default_formatter')
        return formatter.get(typ.lower()) if formatter else None

    @property
    def path(self) -> str:
        return self.__config_path.name


Config = __Config()
