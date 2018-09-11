import json
import decimal
import datetime
import math


class JsonEncoder(json.JSONEncoder):
    """
    @desc ： json编码器
    @author Pings
    @date   2018/04/25
    @Version  V1.0
    """
    
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)


class NumberUtil(object):
    """
    @desc ： 数字类型工具类
    @author  Pings
    @date    2018/05/15
    @version V1.0
    """

    @staticmethod
    def to_decimal(number, prec=6):
        """
        @desc ： 计算权重
        @author Pings
        @date   2018/05/15
        @param  number    单个数据出现的次数
        @param  prec      精度，默认小数点后6位
        @return decimal
        """
        number = number if isinstance(number, decimal.Decimal) else decimal.Decimal(str(number))
        return round(number, prec)

class CollectionsUtil(object):
    """
    @desc ： 集合类型工具类
    @author  Pings
    @date    2018/05/17
    @version V1.0
    """

    @staticmethod
    def split(collection, threshold, qty):
        """
        @desc ： 切分集合
        @author Pings
        @date   2018/05/17
        @param  collection    切分的集合
        @param  threshold     阈值（大于阈值才需要切分）
        @param  qty           切分的数量
        @return iterator
        """
        length = len(collection)

        if length <= threshold:
            rst = [collection].__iter__()
        else:
            count = math.ceil(length / qty)
            rst = (collection[i * count: (i + 1) * count] for i in range(qty) if length > i * count)

        return rst
