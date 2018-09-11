"""
@desc ： 装饰器
@author  Pings
@date    2018/06/14
"""
import time
import functools

from common.apps import logger


def metric(func):
    """
    @desc ： 打印方法运行的时间
    @author  Pings
    @date    2018/06/14
    @version V1.0
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start = time.time()
        rst = func(*args, **kw)
        diff = time.time() - start
        logger.debug('{}运行时间: {:.0f}s'.format(func.__name__, diff))
        return rst

    return wrapper
