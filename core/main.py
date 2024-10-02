#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: UTF-8 -*-
import typer

from basic_commands import app

try:
    app()
except KeyboardInterrupt:
    raise typer.Exit()
