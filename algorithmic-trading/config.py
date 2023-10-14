# coding: utf-8
from enum import Enum
from os import path
from typing import Dict


basedir = path.abspath(path.dirname(__file__))


class Config:

    ALPHA_VANTAGE_API_KEY: str = ''
