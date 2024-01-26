from typing import Callable
from functools import wraps
import time


def try_catch(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
    return wrapper


def print_time(func: Callable):
    """计算函数执行时间的装饰器

    Args:
        func (Callable): 函数

    Returns:
        None: None

    Examples:
        @print_time\n
        def func():
            time.sleep(2)
        
        func() # 函数 func 耗时 2.00 秒
    """
    func_name = func.__name__
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        consumed = end_time - start_time
        print(f"函数 {func_name} 耗时 {consumed:.2f} 秒")
        return result
    return wrapper

