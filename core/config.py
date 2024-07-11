# -*- coding: UTF-8 -*-
import os
import shutil

from ruamel.yaml import YAML


class Config:

    def __init__(self):
        home = os.environ['USERPROFILE']
        power_jekyll_home = os.path.join(home, '.powerjekyll')
        self.__config_path = os.path.join(power_jekyll_home, 'config.yml')

        # create app home
        if not os.path.exists(power_jekyll_home):
            os.mkdir(power_jekyll_home)

        if not os.path.exists(self.__config_path):
            shutil.move('../config.yml.example', self.__config_path)

        # read config
        with open(self.__config_path, 'r') as f:
            yaml = YAML(typ='safe', pure=True)
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
        yaml = YAML(typ='rt', pure=True)
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
        return self.__config_path
