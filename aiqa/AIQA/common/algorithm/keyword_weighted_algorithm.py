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
from common.algorithm.relative_base_function import *

logger = logging.getLogger('common.algorithm.keyword_weighted_algorithm')

knowledge = {}
stopwords = []
Extend_more = {}
extend_seg_more = {}
keyword_dict = []

def init():
    """
    @desc ：初始化基础数据
    @author yanwen
    @date   2018/04/16
    @Version  V1.0
    """
    if len(knowledge) != 0 or len(stopwords) != 0 or len(Extend_more) != 0 or len(extend_seg_more) != 0:
        return

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.append(root)
    if os.environ.get('DJANGO_SETTINGS_MODULE') is None:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIQA.settings')

    # 连接数据库，导出数据
    sql_knowledge = "select * from tax_knowledge"
    sql_keyword = "select * from tax_bas_keyword"
    sql_extend = "select h.id extend_question_id,h.knowledge_id, tf_value, idf_value," \
                 " weighted_value, amplification,keyword from tax_extend_question_header h left join " \
                 "tax_extend_question q on h.id = q.extend_question_id "
    sql_stopwords = "select * from tax_bas_stopword"

    dao = MysqlCommonDao()
    data_knowledge = dao.findall(sql_knowledge)
    data_keyword = dao.findall(sql_keyword)
    data_extend = dao.findall(sql_extend)
    data_stopwords = dao.findall(sql_stopwords)

    # 关键词导出，list输出
    for line in data_keyword:
        keyword_dict.append(line["keyword"])

    # 知识，dict输出
    ques_ans = {}
    for line in data_knowledge:
        u = {'ques':line["sd_question"], 'ans':line["sd_answer"]}
        knowledge[line["id"]] = u
        ques_ans[line["sd_question"]] = line["sd_answer"]

    # 扩展问题，dict
    uu = []
    for line in data_extend:
        # print(line)
        id_knowledge = line["knowledge_id"]
        id_extend = line["extend_question_id"]
        if id_knowledge in Extend_more.keys():
            if id_extend in Extend_more[id_knowledge].keys():
                uu.append(line["keyword"])
                Extend_more[id_knowledge][id_extend][line["keyword"]] = float(line["weighted_value"])
                extend_seg_more[id_knowledge][id_extend] = uu
            else:
                uu = []
                uu.append(line["keyword"])
                Extend_more[id_knowledge][id_extend] = {line["keyword"]: float(line["weighted_value"])}
                extend_seg_more[id_knowledge][id_extend] = uu
        else:
            uu = []
            uu.append(line["keyword"])
            Extend_more[id_knowledge] = {id_extend:{line["keyword"]: float(line["weighted_value"])}}
            extend_seg_more[id_knowledge] = {id_extend:uu}
    # 停用词，list
    for line in data_stopwords:
        stopwords.append(line["word"])


def ModelMatchedAnswer1(sentence):
    init()
    dao = MysqlCommonDao()
    min_value = dao.findone("select value from tax_bas_data where code = 'THRESHOLD_MIN'")["value"]
    max_value = dao.findone("select value from tax_bas_data where code = 'THRESHOLD_MAX'")["value"]
    seg_words = question_seg(sentence, keyword_dict, keyword_dict, RMM=False)
    words = deleteSparator(seg_words)
    outcome = delete_stopwords(words, stopwords)
    best_id, best_point, best_question, match_array = count_seg(min_value, 10, outcome, extend_seg_more, Extend_more, knowledge)

    if best_point == [] or best_point[0] < min_value:
        a = {"token": 0, "content": "无匹配结果，请重新输入问题"}
        return a
    elif best_point[0] >= min_value and best_point[0] < max_value:
        question_list = []
        for line in range(len(best_id)):
            question_list.append({"id": best_id[line], "question":best_question[line]["ques"]})
        a = {"token": 1, "content": {"question":sentence, "answer": [], "policyContent": [], "relativeQuestionList": question_list}}
        return a
    else:
        question_list = []
        for line in range(len(best_id)-1):
            question_list.append({"id": best_id[line+1], "question": best_question[line+1]["ques"]})
        url = "http://192.168.1.86:8080/solr/taxtao_law_lib_article/select?indent=on&wt=json&q=articleContent:"
        input_content = best_question[0]["ans"]
        input_url = url+input_content
        req = requests.get(input_url)
        if req.status_code != 200:
            a = {"token": 1, "content": {"question": sentence, "answer": best_question[0]["ans"], "policyContent": [], "relativeQuestionList": question_list}}
        else:
            mid_variant = req.json()["response"]["docs"]
            if mid_variant == []:
                a = {"token": 1, "content": {"question": sentence, "answer": best_question[0]["ans"], "policyContent": [], "relativeQuestionList": question_list}}
            else:
                policy_content = []
                for line in req.json()["response"]["docs"]:
                    policy_content.append({"id": line["id"], "articleTitle": line["articleTitle"], "articleContent": line["articleContent"]})
                a = {"token": 1, "content": {"question": sentence, "answer": best_question[0]["ans"], "policyContent": policy_content, "relativeQuestionList": question_list}}
        return a


def get_similar_knowledge(sentence):
    init()
    dao = MysqlCommonDao()
    min_value = dao.findone("select value from tax_bas_data where code = 'THRESHOLD_MIN'")["value"]
    max_value = dao.findone("select value from tax_bas_data where code = 'THRESHOLD_MAX'")["value"]
    seg_words = question_seg(sentence, keyword_dict, keyword_dict, RMM=False)
    words = deleteSparator(seg_words)
    outcome = delete_stopwords(words, stopwords)
    best_id, best_point, best_question, match_array = count_seg(min_value, 10, outcome, extend_seg_more, Extend_more, knowledge)

    if best_point == [] or best_point[0] < min_value:
        a = {"token": 0, "content": "无匹配结果，请重新输入问题"}
        return a
    elif best_point[0] >= min_value and best_point[0] < max_value:
        question_list = []
        for line in range(len(best_id)):
            question_list.append({"id":best_id[line], "question":best_question[line]["ques"]})
        a = {"token": 1, "content": {"question":sentence, "answer": [], "policyContent": [], "relativeQuestionList": question_list}}
        return a
    else:
        question_list = []
        for line in range(len(best_id)):
            question_list.append({"id": best_id[line], "question": best_question[line]["ques"]})
        url = "http://192.168.1.86:8080/solr/taxtao_law_lib_article/select?indent=on&wt=json&q=articleContent:"
        input_content = best_question[0]["ans"]
        input_url = url+input_content
        req = requests.get(input_url)
        if req.status_code != 200:
            a = {"token": 1, "content": {"question": sentence, "answer": best_question[0]["ans"], "policyContent": [], "relativeQuestionList": question_list}}
        else:
            mid_variant = req.json()["response"]["docs"]
            if mid_variant == []:
                a = {"token": 1, "content": {"question": sentence, "answer": best_question[0]["ans"], "policyContent": [], "relativeQuestionList": question_list}}
            else:
                policy_content = []
                for line in req.json()["response"]["docs"]:
                    policy_content.append({"id": line["id"], "articleTitle": line["articleTitle"], "articleContent": line["articleContent"]})
                a = {"token": 1, "content": {"question": sentence, "answer": best_question[0]["ans"], "policyContent": policy_content, "relativeQuestionList": question_list}}
        return a


def modify_weights_by_amplification(keyword, amplification) -> bool:
    """
    @desc ：  单个关键词，修改全局放大倍数而导致的权重值。
    @author： yanwen
    @date：   2018/04/25
    @Version：V1.0
    @return： boolean
    """
    dao = MysqlCommonDao()
    dao.execute("UPDATE tax_extend_question h SET h.weighted_value = h.amplification * h.tf_value * h.idf_value * %s where h.keyword = %s",
                [amplification, keyword])
    return True


def compute_weighted_value(extend_question_id, amplification) -> dict:
    """
    @desc ：   根据扩展问题明细id和临时的放大倍数计算权重
    @author：  yanwen
    @date：    2018/04/25
    @Version： V1.0
    @return：  dict   例如：{'weighted_value': 0.868}
    """
    dao = MysqlCommonDao()
    values = dao.findone("SELECT h.tf_value,h.idf_value,h.amplification from tax_extend_question h where h.id=%s",
                         [extend_question_id])
    decimal.getcontext().prec = 6
    value = values["tf_value"] * values["idf_value"] * values["amplification"] * decimal.Decimal(str(amplification))

    return {'weighted_value': value}


def participle(sentence) -> list:
    """
    @desc ：分词算法
    @author： yanwen
    @date：   2018/04/25
    @Version：  V1.0
    @return：  dict
    """
    # 结巴分词
    # sd_ques_seg = jieba.cut(sentence)
    # s1 = ' '.join(sd_ques_seg).strip().split()
    # return [{"keyword": i} for i in s1]
    init()
    seg_ques = question_seg(sentence, keyword_dict, keyword_dict, RMM=False)
    words = deleteSparator(seg_ques)
    seg_words = delete_stopwords(words, stopwords)
    outcome = []
    for line in seg_words:
        outcome.append({"keyword": line})
    return outcome


class BaseInitialization:
    """
    @desc ：数据库使用钟涉及的初始化
    @author wen
    @date   2018/04/25
    @Version  V1.0
    """

    @staticmethod
    def tf_part_init(knowledge_id):
        """
        @desc ：tf值局部初始化，只针对单条知识内的所有扩展问题。
        @author wen
        @date   2018/04/25
        @param  knowledge_id    输入知识的编号
        @return 无返回
        """
        dao = MysqlCommonDao()

        sql_extend = "SELECT h.id extend_question_id,h.knowledge_id,q.keyword,q.amplification part_amplification,k.amplification global_amplification " \
                     "  FROM tax_extend_question_header as h " \
                     "  LEFT JOIN tax_extend_question as q ON h.id = q.extend_question_id" \
                     "  LEFT JOIN tax_bas_keyword as k on k.keyword = q.keyword " \
                     " where h.knowledge_id = %s"

        data_extend = dao.findall(sql_extend, [knowledge_id])

        extend_question_words = {}
        keyword_part_amplification = {}          # 关键词的局部放大倍数
        keyword_global_amplification = {}
        keyword_global_amplification_before = {}        # 关键词的全局放大倍数

        extend_one = []
        extend_one_part_amplification = {}

        for line in data_extend:
            id_knowledge = line["knowledge_id"]
            id_extend = line["extend_question_id"]
            if id_knowledge in extend_question_words.keys():
                if id_extend in extend_question_words[id_knowledge].keys():
                    extend_one.append(line["keyword"])
                    # extend_one_part_amplification.append({line["keyword"]: line["part_amplification"]})
                    extend_one_part_amplification[line["keyword"]] = line["part_amplification"]
                    extend_question_words[id_knowledge][id_extend] = extend_one
                    keyword_part_amplification[id_knowledge][id_extend] = extend_one_part_amplification
                    keyword_global_amplification_before[line["keyword"]] = line["global_amplification"]
                else:
                    extend_question_words[id_knowledge][id_extend] = []
                    keyword_part_amplification[id_knowledge][id_extend] = []
                    extend_one = []
                    extend_one_part_amplification = {}
                    keyword_global_amplification_before[line["keyword"]] = line["global_amplification"]

                    extend_one.append(line["keyword"])
                    extend_one_part_amplification[line["keyword"]] = line["part_amplification"]
                     # 当某个扩展问题的明细只有一个关键词的情况
                    extend_question_words[id_knowledge][id_extend] = extend_one
                    keyword_part_amplification[id_knowledge][id_extend] = extend_one_part_amplification
            else:
                extend_question_words[id_knowledge] = {id_extend: []}
                keyword_part_amplification[id_knowledge] = {id_extend: []}
                extend_one = []
                extend_one_part_amplification = {}
                extend_one.append(line["keyword"])
                extend_one_part_amplification[line["keyword"]] = line["part_amplification"]
                keyword_global_amplification_before[line["keyword"]] = line["global_amplification"]
                # 当某个扩展问题的明细只有一个关键词的情况
                extend_question_words[id_knowledge][id_extend] = extend_one
                keyword_part_amplification[id_knowledge][id_extend] = extend_one_part_amplification

        for global_words in set(keyword_global_amplification_before.keys()):
            keyword_global_amplification[global_words] = keyword_global_amplification_before[global_words]

        tf_extend = tf_one(extend_question_words)         # 关键词的TF值
        idf_whole_words = idf_one(extend_question_words)        # 关键词的idf值

        sql = "UPDATE tax_extend_question h " \
              "SET h.tf_value = %s, h.idf_value = %s, h.weighted_value = %s " \
              "where h.extend_question_id = %s and h.keyword = %s"
        params = []
        for id_knowledge in keyword_part_amplification.keys():
            for id_extend in keyword_part_amplification[id_knowledge].keys():
                for word in keyword_part_amplification[id_knowledge][id_extend].keys():

                    decimal.getcontext().prec = 6
                    tf = decimal.Decimal(str(tf_extend[id_knowledge][id_extend][word]))
                    idf = decimal.Decimal(str(idf_whole_words[word]))
                    global_amplification = keyword_global_amplification[word]
                    amplification = keyword_part_amplification[id_knowledge][id_extend][word]
                    weighted_value = tf * idf * global_amplification * amplification

                    params.append([tf, idf, weighted_value, id_extend, word])

        dao.executemany(sql, params)

    @staticmethod
    def tf_and_idf_init():
        """
        @desc ：tf与idf各自的全局初始化
        @author wen
        @date   2018/04/25
        @return 无返回
        """
        dao = MysqlCommonDao()

        sql = "SELECT h.id extend_question_id,h.knowledge_id,q.keyword,q.amplification part_amplification,k.amplification global_amplification " \
              "FROM tax_extend_question_header as h " \
              "LEFT JOIN tax_extend_question as q ON h.id = q.extend_question_id " \
              "LEFT JOIN tax_bas_keyword as k on k.keyword = q.keyword"

        whole_data = dao.findall(sql)

        extend_question_words = {}
        keyword_part_amplification = {}          # 关键词的局部放大倍数
        keyword_global_amplification = {}
        keyword_global_amplification_before = {}        # 关键词的全局放大倍数

        extend_one = []
        extend_one_part_amplification = {}

        for line in whole_data:
            id_knowledge = line["knowledge_id"]
            id_extend = line["extend_question_id"]
            if id_knowledge in extend_question_words.keys():
                if id_extend in extend_question_words[id_knowledge].keys():
                    extend_one.append(line["keyword"])
                    # extend_one_part_amplification.append({line["keyword"]: line["part_amplification"]})
                    extend_one_part_amplification[line["keyword"]] = line["part_amplification"]
                    extend_question_words[id_knowledge][id_extend] = extend_one
                    keyword_part_amplification[id_knowledge][id_extend] = extend_one_part_amplification
                    keyword_global_amplification_before[line["keyword"]] = line["global_amplification"]
                else:
                    extend_question_words[id_knowledge][id_extend] = []
                    keyword_part_amplification[id_knowledge][id_extend] = []
                    extend_one = []
                    extend_one_part_amplification = {}
                    keyword_global_amplification_before[line["keyword"]] = line["global_amplification"]

                    extend_one.append(line["keyword"])
                    extend_one_part_amplification[line["keyword"]] = line["part_amplification"]
                     # 当某个扩展问题的明细只有一个关键词的情况
                    extend_question_words[id_knowledge][id_extend] = extend_one
                    keyword_part_amplification[id_knowledge][id_extend] = extend_one_part_amplification
            else:
                extend_question_words[id_knowledge] = {id_extend: []}
                keyword_part_amplification[id_knowledge] = {id_extend: []}
                extend_one = []
                extend_one_part_amplification = {}
                extend_one.append(line["keyword"])
                extend_one_part_amplification[line["keyword"]] = line["part_amplification"]
                keyword_global_amplification_before[line["keyword"]] = line["global_amplification"]
                # 当某个扩展问题的明细只有一个关键词的情况
                extend_question_words[id_knowledge][id_extend] = extend_one
                keyword_part_amplification[id_knowledge][id_extend] = extend_one_part_amplification

        for global_words in set(keyword_global_amplification_before.keys()):
            keyword_global_amplification[global_words] = keyword_global_amplification_before[global_words]

        tf_extend = tf_whole(extend_question_words)         # 关键词的TF值
        idf_whole_words = idf_whole(extend_question_words)        # 关键词的idf值

        sql = "UPDATE tax_extend_question h SET h.tf_value = %s, h.idf_value = %s, " \
                  "h.weighted_value = %s where h.extend_question_id = %s and h.keyword = %s"
        params = []
        for id_knowledge in keyword_part_amplification.keys():
            for id_extend in keyword_part_amplification[id_knowledge].keys():
                for word in keyword_part_amplification[id_knowledge][id_extend].keys():

                    decimal.getcontext().prec = 6
                    tf = decimal.Decimal(str(tf_extend[id_knowledge][id_extend][word]))
                    idf = decimal.Decimal(str(idf_whole_words[word]))
                    global_amplification = keyword_global_amplification[word]
                    amplification = keyword_part_amplification[id_knowledge][id_extend][word]
                    weighted_value = tf * idf * global_amplification * amplification

                    params.append([tf, idf, weighted_value, id_extend, word])

        dao.executemany(sql, params)


def tf_one(extend_question_words) -> dict:
    """
    @desc ：tf值初始化，用于单条知识。
    @author： yanwen
    @date：   2018/04/25
    @Version：  V1.0
    @return：  dict
    """
    # tf_extend = {}
    # for id_knowledge in extend_question_words.keys():
    #     for id_extend in extend_question_words[id_knowledge].keys():
    #         single_extend = extend_question_words[id_knowledge][id_extend]
    #         set_tf_seg = set(single_extend)
    #         len_tf_seg = len(single_extend)
    #         tf_one = {}
    #         for word in set_tf_seg:
    #             tf_one[word] = round(single_extend.count(word) / len_tf_seg, 6)
    #         tf_extend[id_extend] = tf_one
    tf_extend = {}
    for id_knowledge in extend_question_words.keys():
        extend = {}
        tf_extend[id_knowledge] = extend

        for id_extend in extend_question_words[id_knowledge].keys():

            single_extend = extend_question_words[id_knowledge][id_extend]
            set_tf_seg = set(single_extend)
            len_tf_seg = len(single_extend)
            tf_one = {}
            for word in set_tf_seg:
                # a = {word: round(single_extend.count(word) / len_tf_seg, 6)}
                # tf_one.append(a)
                tf_one[word] = round(single_extend.count(word) / len_tf_seg, 6)
            extend[id_extend] = tf_one

    return tf_extend


def tf_whole(extend_question_words) -> dict:
    """
    @desc ：tf值初始化，用于全部知识。
    @author： yanwen
    @date：   2018/04/25
    @Version：  V1.0
    @return：  dict
    """
    tf_extend = {}
    for id_knowledge in extend_question_words.keys():
        extend = {}
        tf_extend[id_knowledge] = extend

        for id_extend in extend_question_words[id_knowledge].keys():

            single_extend = extend_question_words[id_knowledge][id_extend]
            set_tf_seg = set(single_extend)
            len_tf_seg = len(single_extend)
            tf_one = {}
            for word in set_tf_seg:
                # a = {word: round(single_extend.count(word) / len_tf_seg, 6)}
                # tf_one.append(a)
                tf_one[word] = round(single_extend.count(word) / len_tf_seg, 6)
            extend[id_extend] = tf_one

    return tf_extend


def idf_whole(extend_question_words) -> dict:
    """
    @desc ：idf初始化，用于全部知识。
    @author： yanwen
    @date：   2018/04/25
    @Version：  V1.0
    @return：  dict
    """
    words = []
    words_in_extends = {}
    for id_knowledge in extend_question_words.keys():
        words_in_every_extend = []
        for id_extend in extend_question_words[id_knowledge].keys():
            for line in extend_question_words[id_knowledge][id_extend]:
                words_in_every_extend.append(line)
                words.append(line)
        words_in_extends[id_knowledge] = words_in_every_extend
    set_whole_words = set(words)
    len_title = len(extend_question_words.keys())
    idf_whole_words = {}
    for word in set_whole_words:
        u = 0
        for id_knowledge in words_in_extends.keys():
            if word in words_in_extends[id_knowledge]:
                u += 1
        if u == 0:
            idf_whole_words[word] = 0
        else:
            idf_whole_words[word] = round(math.log(len_title/u), 6)
    return idf_whole_words


def idf_one(extend_question_words) -> dict:
    """
    @desc ：idf初始化，单个关键词。
    @author： yanwen
    @date：   2018/04/26
    @Version：  V1.0
    @return：  dict
    """
    dao = MysqlCommonDao()
    words = []
    for id_knowledge in extend_question_words.keys():
        for id_extend in extend_question_words[id_knowledge].keys():
            for line in extend_question_words[id_knowledge][id_extend]:
                words.append(line)

    set_whole_words = set(words)
    idf_whole_words = {}

    for keyword in set_whole_words:
        sql_len_knowledge = "SELECT COUNT(id) count FROM tax_knowledge"
        len_knowledge = dao.findone(sql_len_knowledge)["count"]
        sql_keyword = "select count(*) count " \
                      "from (select h.knowledge_id " \
                      "from tax_extend_question_header h " \
                      "left join tax_extend_question q on h.id = q.extend_question_id " \
                      "where q.keyword = %s " \
                      "group by h.knowledge_id)tmp"
        param = [keyword]
        keyword_times = dao.findone(sql_keyword, param)["count"]
        idf_whole_words[keyword] = round(math.log(len_knowledge / keyword_times), 6)

    return idf_whole_words


def expert_adjust(sentence):
    """
    @desc ：    通过修改关键词局部放大倍数，改变关键词权重值
    @author：   yanwen
    @date：     2018/04/27
    @Version：  V1.0
    @return：   dict
    """


class ExpertAdjust:
    """
    @desc ：    通过修改关键词局部放大倍数，改变关键词权重值
    @author：   yanwen
    @date：     2018/04/27
    @Version：  V1.0
    """
    @staticmethod
    def calculate_question(sentence) -> dict:
        """
        @desc ：    输入问题，返回计算结果
        @author：   yanwen
        @date：     2018/04/27
        @Version：  V1.0
        @return：   dict
        """
        init()
        dao = MysqlCommonDao()
        min_value = dao.findone("select value from tax_bas_data where code = 'THRESHOLD_MIN'")["value"]
        seg_words = question_seg(sentence, keyword_dict, keyword_dict, RMM=False)
        words = deleteSparator(seg_words)
        outcome = delete_stopwords(words, stopwords)
        best_extend_id, best_point, best_question, match_keywords, extend_question_match = count_seg_for_expert_adjust(min_value, 20, outcome, extend_seg_more, Extend_more, knowledge)

        if best_point == [] or best_point[0] < min_value:
            calculation = {"token": 0, "content": "无匹配结果，请重新输入问题"}
            return calculation
        else:
            question_list = []
            for line in range(len(best_extend_id)):
                question_list.append({"id": best_extend_id[line], "best_point": best_point[line], "question": best_question[line]["ques"],
                                      "match_keywords": match_keywords[line], "extend_question": extend_question_match[line]})
            calculation = {"token": 1, "content": {"question": sentence, "relativeQuestionList": question_list}}
            return calculation

    @staticmethod
    def award(sentence, extend_id, matched_keywords):
        """
        @desc ：    增大句子的相似度评分
        @author：   yanwen
        @date：     2018/04/27
        @Version：  V1.0
        @return：   dict
        """
        dao = MysqlCommonDao()
        modify_step = dao.findone("select value from tax_bas_data where code = 'MODIFY_STEP'")["value"]

        keywords = ""
        for key in matched_keywords:
            keywords += "'{0}',".format(key)
        keywords = keywords[:-1]

        sql_award_amplification = '''UPDATE tax_extend_question h,tax_bas_keyword k
                                        SET h.amplification = h.amplification * %s,
                                            h.weighted_value = h.tf_value * h.idf_value * h.amplification * k.amplification * %s
                                      where h.keyword = k.keyword and h.extend_question_id = %s and h.keyword in ({0})'''.format(keywords)
        params = [1 + modify_step, 1 + modify_step, extend_id]
        dao.execute(sql_award_amplification, params)

    @staticmethod
    def punishment(sentence, extend_id, matched_keywords):
        """
        @desc ：    降低句子的相似度评分
        @author：   yanwen
        @date：     2018/04/27
        @Version：  V1.0
        @return：   dict
        """
        dao = MysqlCommonDao()
        modify_step = dao.findone("select value from tax_bas_data where code = 'MODIFY_STEP'")["value"]

        keywords = ""
        for key in matched_keywords:
            keywords += "'{0}',".format(key)
        keywords = keywords[:-1]

        sql_award_amplification = '''UPDATE tax_extend_question h,tax_bas_keyword k
                                        SET h.amplification = h.amplification * %s,
                                            h.weighted_value = h.tf_value * h.idf_value * h.amplification * k.amplification * %s
                                      where h.keyword = k.keyword and h.extend_question_id = %s and h.keyword in ({0})'''.format(keywords)
        params = [1 - modify_step, 1 - modify_step, extend_id]
        dao.execute(sql_award_amplification, params)
