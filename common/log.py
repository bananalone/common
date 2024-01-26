'''
Author: bananalone
Date: 2024-01-03
Copyright (c) 2024 by bananalone, All Rights Reserved.
'''


import logging

from rich.logging import RichHandler


def get_logger(
        level: str = 'INFO', 
        format: str = '%(message)s', 
        datefmt: str = '[%X]'
    ):
    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        handlers=[RichHandler()]
    )
    return logging.getLogger('rich')

