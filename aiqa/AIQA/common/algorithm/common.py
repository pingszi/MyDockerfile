import sys
import decimal
import math
import re
import functools
from abc import ABCMeta, abstractmethod
from itertools import zip_longest  

from mgbase.models.bas_models import TaxBasKeyword, TaxBasStopWord
from common.util.utils import NumberUtil
from common.apps import logger

# **递归调用深度，默认1000，设置成10000 
sys.setrecursionlimit(10000)  


class AbstractParticiple(object):
    """
    @desc ： 抽象分词算法
    @author  Pings
    @date    2018/05/14
    @version V1.0
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        # **关键词元组
        self.keyword_tuple = ()
        # **停用词元组
        self.stopword_tuple = ()

    def start(self, sentence) -> tuple:
        """
        @desc ： 开始分词
        @author Pings
        @date   2018/05/11
        @param  sentence   需要分词的语句
        @return tuple<string>
        """
        self.keyword_tuple = TaxBasKeyword.list_all()
        self.stopword_tuple = TaxBasStopWord.list_all()

        word_tuple = self._segment(sentence)
        return self._delete_stopword(word_tuple)

    @abstractmethod
    def _segment(self, sentence):
        """
        @desc ：  分词算法
        @author  Pings
        @date    2018/05/11
        @version V1.0
        """
        pass

    @abstractmethod
    def _delete_stopword(self, word_tuple):
        """
        @desc ：删除停用词
        @author Pings
        @date   2018/05/11
        @param  word_tuple   分词结果列表
        @return tuple<string>
        """
        pass


class MMParticiple(AbstractParticiple):
    """
    @desc ： （正向最大匹配）分词算法
    @author  Pings
    @date    2018/05/11
    @version V1.0
    """
    def _segment(self, sentence) -> tuple:
        """
        @desc ： 对语句进行切分(正向最大匹配)
        @author Pings
        @date   2018/05/10
        @param  sentence    需要分词的语句
        @return tuple<string>
        """
        rst = []

        def recursion_matcher(question):
            keyword = "N"

            if question in self.keyword_tuple:
                keyword = question
            elif len(question) > 1:
                keyword = recursion_matcher(question[:-1])

            return keyword

        # **字母数字直接做为分词结果
        pattern = re.compile("[A-Za-z0-9]+")
        rst += pattern.findall(sentence)
        sentence = pattern.sub("~", sentence)

        while len(sentence):
            key = recursion_matcher(sentence)
            if key != "N":
                rst.append(key)
            sentence = sentence[len(key):]

        return tuple(rst)

    def _delete_stopword(self, word_tuple) -> tuple:
        return tuple(word for word in word_tuple if word not in self.stopword_tuple)


class TfIdf(object):
    """
    @desc ：tf/idf算法
    @author Pings
    @date   2018/05/15
    @version V1.0

    @version V1.1
    Pings 2018-05-29  相似度公式修改
    """

    @staticmethod
    def tf(qty, total, prec=6) -> decimal:
        """
        @desc ： 计算tf值
        @author Pings
        @date   2018/05/15
        @param  qty    单个数据出现的次数
        @param  total  总数据量
        @param  prec   精度，默认小数点后6位
        @return decimal
        """
        qty = NumberUtil.to_decimal(qty, prec)
        total = NumberUtil.to_decimal(total, prec)
        return NumberUtil.to_decimal(qty / total)

    @staticmethod
    def idf(qty, total, prec=6) -> decimal:
        """
        @desc ： 计算idf值
        @author Pings
        @date   2018/05/15
        @param  qty    单个数据出现的次数
        @param  total  总数据量
        @param  prec   精度，默认小数点后6位
        @return decimal
        """
        qty = NumberUtil.to_decimal(qty, prec)
        total = NumberUtil.to_decimal(total, prec)

        return NumberUtil.to_decimal(math.log(total / qty), prec)

    @staticmethod
    def weighted(tf, idf, amplification=1, global_amplification=1, prec=6) -> decimal:
        """
        @desc ： 计算权重
        @author Pings
        @date   2018/05/15
        @param  tf    单个数据出现的次数
        @param  idf  总数据量
        @param  amplification         局部放大倍数，默认为1
        @param  global_amplification  全局放大倍数，默认为1
        @param  prec   精度，默认小数点后6位
        @return decimal
        """
        tf = NumberUtil.to_decimal(tf, prec)
        idf = NumberUtil.to_decimal(idf, prec)
        amplification = NumberUtil.to_decimal(amplification, prec)
        global_amplification = NumberUtil.to_decimal(global_amplification, prec)

        return NumberUtil.to_decimal(tf * idf * amplification * global_amplification)

    # @staticmethod
    # def similarity(match_sum, no_match_sum, word_len, extend_len, coeff1=0.3, coeff2=0.001, prec=6) -> decimal:
    #     """
    #     @desc ： 计算相似度（相似度 = （匹配关键词的权重和 - 0.3*不匹配的关键词权重和）/ 扩展问题的关键词权重和）
    #     @author Pings
    #     @date   2018/05/17
    #     @param  match_sum           匹配上的关键字权重之和
    #     @param  no_match_sum        未匹配上的关键字权重之和
    #     @param  word_len            问题的关键字个数
    #     @param  extend_len          扩展问题关键字个数
    #     @param  coeff1              未匹配上的关键字权重系数
    #     @param  coeff2              调整系数
    #     @param  prec                精度，默认小数点后6位
    #     @return decimal

    #     Pings 2018-05-29  相似度公式修改
    #     相似度 = （匹配关键词的权重和 - 0.3*不匹配的关键词权重和）/ 扩展问题的关键词权重和 - 0.01 * |（用户提问问题的关键词个数-扩展问题的关键词个数）|
    #     """
    #     match_weight_sum = NumberUtil.to_decimal(match_sum, prec)
    #     no_match_weight_sum = NumberUtil.to_decimal(no_match_sum, prec)
    #     coeff1 = NumberUtil.to_decimal(coeff1, prec)
    #     coeff2 = NumberUtil.to_decimal(coeff2, prec)

    #     similarity = (match_weight_sum - coeff1 * no_match_weight_sum) / (match_weight_sum + no_match_weight_sum)
    #     similarity -= abs(coeff2 * (word_len - extend_len))
    #     return similarity

    @staticmethod
    def similarity(match_sum, no_match_sum, word_len, extend_len, extend_matched_len, coeff1=0.195, coeff2=1.0, prec=6) -> decimal:
        """
        @desc ： 计算相似度
        相似度1 = （匹配关键词的权重和 - 0.3*不匹配的关键词权重和）/ 扩展问题的关键词权重和
        扩展问题匹配个数高斯分布 = [1-exp(-pow((扩展问题匹配上的关键字个数 - 问题的关键字个数), 2) / (2*sig1)]
        扩展问题个数高斯分布 = [1-exp(-pow((扩展问题关键字个数 - 问题的关键字个数), 2) / (2*sig2)]
        相似度 = 相似度1 - 调整系数 * 相似度1 * 扩展问题匹配个数高斯分布 * 扩展问题个数高斯分布
        @author Pings
        @date   2018/08/10
        @version V1.4
        @param  match_sum           匹配上的关键字权重之和
        @param  no_match_sum        未匹配上的关键字权重之和
        @param  word_len            问题的关键字个数
        @param  extend_len          扩展问题关键字个数
        @param  extend_matched_len  扩展问题匹配上的关键字个数
        @param  coeff1              未匹配上的关键字权重系数
        @param  coeff2              调整系数
        @param  prec                精度，默认小数点后6位
        @return decimal
        """
        sig1 = 1.5
        sig2 = 1

        match_weight_sum = NumberUtil.to_decimal(match_sum, prec)
        no_match_weight_sum = NumberUtil.to_decimal(no_match_sum, prec)
        coeff1 = NumberUtil.to_decimal(coeff1, prec)
        coeff2 = NumberUtil.to_decimal(coeff2, prec)
        
        similarity = (match_weight_sum - coeff1 * no_match_weight_sum) / (match_weight_sum + no_match_weight_sum) * NumberUtil.to_decimal(0.6)
        # value1 = 1 - math.exp(-math.pow(extend_matched_len - word_len, 2) / (2 * sig1))
        # value2 = 1 - math.exp(-math.pow(extend_len - word_len, 2) / (2 * sig2))
        # similarity -= coeff2 * similarity * NumberUtil.to_decimal(value1) * NumberUtil.to_decimal(value2)

        value1 = math.exp(-math.pow(extend_matched_len - word_len, 2) / (2 * sig1))
        value2 = math.exp(-math.pow(extend_len - word_len, 2) / (2 * sig2))
        similarity += coeff2 * similarity * NumberUtil.to_decimal(value1) * NumberUtil.to_decimal(value2)
    
        return NumberUtil.to_decimal(similarity)

    @staticmethod
    def individual_tax(salary, fund, insurance, base=3500, prec=2):
        """
        @desc ：计算个税
        @author Pings
        @date   2018/09/06
        @version V1.5
        @param  salary      工资
        @param  fund        公积金
        @param  insurance   保险
        @param  base        免税基数
        @param  prec        精度，默认小数点后6位
        @return decimal
        """
        # **应纳税所得额
        money = salary - fund - insurance - base
        if money <= 1500:
            rst = money * 0.03
        elif 1500 < money <= 4500:
            rst = money * 0.1 - 105
        elif 4500 < money <= 9000:
            rst = money * 0.2 - 555
        elif 9000 < money <= 35000:
            rst = money * 0.25 - 1005
        elif 35000 < money <= 55000:
            rst = money * 0.3 - 2755
        elif 55000 < money <= 80000:
            rst = money * 0.35 - 5505
        elif money > 80000:
            rst = money * 0.45 - 13505

        return NumberUtil.to_decimal(rst, prec)


def individual_tax_decor(func):
    """
    @desc ： 个税计算装饰器
    @author  Pings
    @date    2018/09/06
    @version V1.5
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        rst = func(*args, **kw)
        # **结果中有{0}占位符，表示匹配到计算个税知识的问题
        if rst["token"] and rst["content"]["answer"] and ("{0}" in rst["content"]["answer"]):
            # **替换答案中的p标签，并根据br截取
            answer = rst["content"]["answer"]
            logger.info("{0}计算个税：\n问题：{1}\n答案：{2}".format(func.__name__, args[1], answer))
            pattern = re.compile("<[/|p]+>")
            answer = pattern.sub("", answer)
            answers = answer.split("<br/>")

            keys = ("工资", "公积金", "社会保险")

            # **分词结果
            word_tuple = args[2]
            # **匹配的关键字
            match_keywords = args[3][0]["match_keywords"]
            keyword_numbers = tuple(key for key in word_tuple if key.isdecimal())
            match_keywords = tuple((word, keywords[0]) for word in word_tuple for keywords
                                   in match_keywords if word in keywords and keywords[0] in keys)
            # **如果数值比匹配的关键字多，删除多余的数值
            if len(keyword_numbers) > len(match_keywords):
                keyword_numbers = keyword_numbers[:len(match_keywords)]

            # **获取工资/公积金/社会保险
            message = None
            salary = fund = insurance = 0
            for k, n in zip_longest(match_keywords, keyword_numbers):
                if k[1] == keys[0]:
                    if n:
                        salary = int(n)
                    else:
                        message = answers[0].format(k[0])
                        break
                elif k[1] == keys[1]:
                    if n:
                        fund = int(n)
                    else:
                        message = answers[0].format(k[0])
                        break
                elif k[1] == keys[2]:
                    if n:
                        insurance = int(n)
                    else:
                        message = answers[0].format(k[0])
                        break

            if message or not salary:  # **各项没有金额/没有工资数
                message = answers[0].format("工资") if not salary else message
            elif salary and fund and insurance:  # **各项均有金额
                individual_tax = TfIdf.individual_tax(salary, fund, insurance)
                message = answers[2].format(individual_tax)
            else:  # **部分项有金额
                individual_tax = TfIdf.individual_tax(salary, fund, insurance)
                message = answers[1].format(individual_tax)

            logger.info("{0}计算个税：\n问题：{1}\n答案：{2}".format(func.__name__, args[1], message))
            rst["content"]["answer"] = message

            # **重新设置缓存
            use_cache = args[7] if len(args) > 7 else True
            if use_cache:
                args[0]._set_answer_by_cache(word_tuple, rst)

        return rst

    return wrapper
