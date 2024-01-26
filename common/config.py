'''
Author: bananalone
Date: 2024-01-03
Copyright (c) 2024 by bananalone, All Rights Reserved.
'''


from typing import Any, Callable
from functools import wraps

import toml


class Config:
    def __init__(self, path: str) -> None:
        self._conf = toml.load(path)

    def inject(self, *args, **kwargs):
        """根据配置文件向函数注入参数, 返回柯里化的函数

        Returns:
            function: 包含剩余参数的柯里化函数

        Example:
            # config.toml\n
            [line]\n
            a = 2\n
            b = 1\n

            # example.py\n
            conf = Config('config.toml')\n

            @conf.inject('line.a', b='line.b')\n
            def calc_y(a, x, b):\n
                return a * x + b\n
            
            y = calc_y(10)\n
            print(y)  # 21\n
        """

        inject_args = [self._get_value(conf_key) for conf_key in args]
        inject_kwargs = {}
        for param_name in kwargs:
            conf_key = kwargs[param_name]
            inject_kwargs[param_name] = self._get_value(conf_key)

        def wrapper(func: Callable):
            @wraps(func)
            def func_wrapper(*rest_args, **rest_kwargs):
                func_args = [*inject_args, *rest_args]
                func_kwargs = {**inject_kwargs, **rest_kwargs}
                return func(*func_args, **func_kwargs)
            
            return func_wrapper

        return wrapper

    def _get_value(self, key: str) -> Any:
        """根据配置文件的键获取对应的值

        Args:
            key (str): 配置文件的键

        Returns:
            Any: 配置文件的值
        """
        dict_keys = key.split('.')
        value = self._conf
        for dict_key in dict_keys:
            value = value[dict_key]
        return value


