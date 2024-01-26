'''
Author: bananalone
Date: 2024-01-03
Copyright (c) 2024 by bananalone, All Rights Reserved.
'''


import json
from typing import Any


def pretty(obj: Any):
    return json.dumps(obj, indent=4, ensure_ascii=False)

