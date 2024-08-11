# -*- coding: UTF-8 -*-
from pathlib import Path

from ruamel.yaml import YAML


class Config:
    __DEFAULT_CONFIG = {
        'mode': 'single',
        'port': None,  # default 4000
        'formatter': {
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

    @property
    def draft_formatter(self) -> dict | None:
        formatter = self.__config.get('formatter')
        return formatter.get('draft') if formatter else None

    @property
    def post_formatter(self) -> dict | None:
        formatter = self.__config.get('formatter')
        return formatter.get('post') if formatter else None

    @property
    def path(self) -> str:
        return self.__config_path.name
