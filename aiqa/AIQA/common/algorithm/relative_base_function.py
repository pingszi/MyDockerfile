import os
import sys
import json
import requests
import logging
import jieba
import math
import decimal
from decimal import *

from common.util.commondao import MysqlCommonDao


# 分词模块
def is_Chinese_char(charater):
    """
    @desc ：判断该字符是否是中文字符（不包括中文标点）
    @author yanwen
    @date   2018/04/20
    @Version  V1.0
    """
    return 0x4e00 <= ord(charater) < 0x9fa6


def isASCIIchar(ch):
    """
    @desc ：判断是否是ASCII码
    @author yanwen
    @date   2018/04/16
    @Version  V1.0
    @return  boolean
    """
    import string
    if ch in string.whitespace:
        return False
    if ch in string.punctuation:
        return False
    # if ch in string.printable:
    #     return False
    return ch in string.printable


def question_seg(sentence, dict_seg, dict_seg1, RMM=True) -> list:
    """
    @desc ：正向最大匹配FMM
    @author yanwen
    @date   2018/04/16
    @Version  V1.0
    @return  list
    """
    result_s = ''
    s_length = len(sentence)
    english_word = ""
    if not RMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if w_length == 1:
                    result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                # 字典1
                elif word in dict_seg:
                    result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                # 字典2
                elif word in dict_seg1:
                    result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                else:
                    while w_length > 0:
                        if isASCIIchar(word[0]):
                            english_word = english_word + str(word[0])
                            word = word[1:]
                            sentence = sentence[1:]
                            w_length = len(word)
                        else:
                            if english_word:
                                result_s += english_word + "/"
                                english_word = ""
                            break
                    if word in dict_seg:
                        result_s += word + "/"
                        sentence = sentence[w_length:]
                        break
                    word = word[:w_length - 1]
                w_length = w_length - 1
            s_length = len(sentence)

    else:
        result_s = []
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if w_length == 1:
                    # print(word)
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in dict_seg:
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    while w_length > 0:
                        if isASCIIchar(word[-1]):
                            english_word = str(word[-1]) + english_word
                            word = word[:-1]
                            sentence = sentence[:-1]
                            w_length = len(word)
                        else:
                            if english_word:
                                result_s = english_word + "/" + result_s
                                english_word = ""
                            break
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
        s_length = len(result_s)
        result_s = result_s[:s_length - 3] + "\n"
    return result_s

    result_s = ''
    sentence = sentence.lower()
    s_length = len(sentence)
    while s_length > 0:
        word = sentence
        w_length = len(word)
        while w_length > 0:
            # 关键词及全局同义词切分
            if word in dict_kw:
                result_s += word
                sentence = sentence[w_length:]
                break
            # 切分至单字
            elif w_length == 1:
                result_s.append(word)
                sentence = sentence[w_length:]
                break
            else:
                word = word[:w_length - 1]
            w_length = w_length - 1
        s_length = len(sentence)
    #result_s = result_s[:len(result_s)-1]
    return result_s


def deleteSparator(words) -> list:
    """
    @desc ：去除反斜杠符号，根据对输入问题进行分词后，分词结果中夹带着符号'/'，所以需要去掉分隔符'/'
    @author： yanwen
    @date：   2018/04/20
    @Version：  V1.0
    @return：  list
    @example：
        # 输入数据words的格式如，words = '第一/定期/电能表/进行/周期/轮换/'
        # seg的输出格式如，seg = ['第一','定期','电能表','进行','周期','轮换']
    """
    seg = words.strip().split('/')
    if seg[-1] == '':
        seg = seg[:-1]
    return seg


def delete_stopwords(words, stopwords) -> list:
    """
    @desc ：去除停用词
    @author： yanwen
    @date：   2018/04/20
    @Version：  V1.0
    @return：  list
    @example：
        输入数据words的格式，words = ['第一','定期','电能表','进行','周期','轮换']
        输出数据segword的格式，segword = ['定期','电能表','进行','周期','轮换']
    """
    segword = []
    for word in words:
        if len(word) == 1:
            continue
        elif word not in stopwords:
            segword.append(word)
    return segword


def count_seg(min_value, output_number, get_seg, questionSeg, extend, knowledge):
    """
    @desc ：计分模块,计算每一条扩展问题与用户提问问题的相似度。
    @author： yanwen
    @date：   2018/04/20
    @Version：  V1.0
    @return：  list
    @imput:
        get_seg：经过分词模块的结果，list格式，如['电费','缴纳']
        questionSeg：所有extend的问题集，是字典格式，如{'25':[['电费','缴纳'],[...],[...]...],'26':[[...],[...],[...]]}
        keywords：关键词字典是字典格式，如{'电费':1.2,'缴纳':0.8}
    """
    INITIAL_VALUE = 0
    best_point = []    # 相关的分数
    best_id = []        # 相关分数的id
    best_question = []  # 相关id下的问题
    match_keywords = []

    best_point_middle = []    # 相关的分数
    best_id_middle = []        # 相关分数的id
    best_question_middle = []  # 相关id下的问题
    match_keywords_middle = []

    qa_id_old = -1
    for qa_id in questionSeg.keys():
        for extend_id in questionSeg[qa_id]:
            QQ = extend[qa_id][extend_id]
            seg_array = questionSeg[qa_id][extend_id]
            max_one, match, un_match, point = 0.0, 0.0, 0.0, 0.0

            # match：单个扩展问的匹配分
            seg_array_match = []   # 各个拓展问的匹配关键词
            get_seg_match = []     # 问句分词结果后的匹配关键词
            for seg in get_seg:
                if seg in seg_array:   # 关键词没有同义词情况
                    match += float(QQ[seg])
                    seg_array_match.append(seg)
                    get_seg_match.append(seg)

            # max_one：单个扩展问的最大匹配分
            for w in seg_array:
                max_one += (float(QQ[w]))

            # 避免出现分母为零的情况
            if max_one == 0:
                max_one += 1
            # un_match：不匹配词
            s2 = set(seg_array).difference(set(seg_array_match))    # 扩展问中，不匹配的关键词
            un_match_words = s2
            for un_word in un_match_words:
                un_match += float(QQ[un_word])
            point = (match - un_match * 0.3) / max_one    # 计算的分数
            # 匹配计算

            if point < min_value:
                continue
            else:
                if qa_id != qa_id_old:
                    best_point_middle.append(point)
                    best_id_middle.append(qa_id)
                    best_question_middle.append(knowledge[qa_id])
                    match_keywords_middle.append(seg_array_match)
                else:
                    if point > best_point_middle[-1]:
                        best_point_middle[-1] = point
                        match_keywords_middle[-1] = seg_array_match
            qa_id_old = qa_id
    for line in sorted(best_point_middle, reverse=True):
        inline = best_point_middle.index(line)
        best_point.append(best_point_middle[inline])
        best_id.append(best_id_middle[inline])
        best_question.append(best_question_middle[inline])
        match_keywords.append(match_keywords_middle[inline])
    return best_id[:output_number], best_point[:output_number], best_question[:output_number], match_keywords[:output_number]


def count_seg_for_expert_adjust(min_value, output_number, get_seg, questionSeg, extend, knowledge):
    """
    @desc ：计分模块,计算每一条扩展问题与用户提问问题的相似度。
    @author： yanwen
    @date：   2018/04/20
    @Version：  V1.0
    @return：  list
    @imput:
        get_seg：经过分词模块的结果，list格式，如['电费','缴纳']
        questionSeg：所有extend的问题集，是字典格式，如{'25':[['电费','缴纳'],[...],[...]...],'26':[[...],[...],[...]]}
        keywords：关键词字典是字典格式，如{'电费':1.2,'缴纳':0.8}
    """
    INITIAL_VALUE = 0
    best_point = []    # 相关的分数
    best_extend_id = []        # 相关分数的id
    best_question = []  # 相关id下的问题
    match_keywords = []
    extend_question_match = []

    best_point_middle = []    # 相关的分数
    best_extend_id_middle = []        # 相关分数的id
    best_question_middle = []  # 相关id下的问题
    match_keywords_middle = []
    extend_question_match_middle = []

    qa_id_old = -1
    for qa_id in questionSeg.keys():
        for extend_id in questionSeg[qa_id]:
            QQ = extend[qa_id][extend_id]
            seg_array = questionSeg[qa_id][extend_id]
            max_one, match, un_match, point = 0.0, 0.0, 0.0, 0.0

            # match：单个扩展问的匹配分
            seg_array_match = []   # 各个拓展问的匹配关键词
            get_seg_match = []     # 问句分词结果后的匹配关键词
            for seg in get_seg:
                if seg in seg_array:   # 关键词没有同义词情况
                    match += float(QQ[seg])
                    seg_array_match.append(seg)
                    get_seg_match.append(seg)

            # max_one：单个扩展问的最大匹配分
            for w in seg_array:
                max_one += (float(QQ[w]))

            # 避免出现分母为零的情况
            if max_one == 0:
                max_one += 1
            # un_match：不匹配词
            s2 = set(seg_array).difference(set(seg_array_match))    # 扩展问中，不匹配的关键词
            un_match_words = s2
            for un_word in un_match_words:
                un_match += float(QQ[un_word])
            point = round((match - un_match * 0.3) / max_one, 3)    # 计算的分数
            # 匹配计算

            if point < min_value:
                continue
            else:
                if qa_id != qa_id_old:
                    best_point_middle.append(point)
                    best_extend_id_middle.append(extend_id)
                    best_question_middle.append(knowledge[qa_id])
                    match_keywords_middle.append(seg_array_match)
                    extend_question_match_middle.append(QQ)
                else:
                    if point > best_point_middle[-1]:
                        best_point_middle[-1] = point
                        best_extend_id_middle[-1] = extend_id
                        match_keywords_middle[-1] = seg_array_match
                        extend_question_match_middle[-1] = QQ
            qa_id_old = qa_id
    for line in sorted(best_point_middle, reverse=True):
        inline = best_point_middle.index(line)
        best_point.append(best_point_middle[inline])
        best_extend_id.append(best_extend_id_middle[inline])
        best_question.append(best_question_middle[inline])
        match_keywords.append(match_keywords_middle[inline])
        extend_question_match.append(extend_question_match_middle[inline])
    return best_extend_id[:output_number], best_point[:output_number], best_question[:output_number], match_keywords[:output_number], extend_question_match[:output_number]
