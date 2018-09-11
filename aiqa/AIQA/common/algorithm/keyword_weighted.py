import decimal
import multiprocessing
import requests
from itertools import groupby
from operator import itemgetter
from collections import Counter
from abc import ABCMeta, abstractmethod

from django.core.cache import cache

from AIQA.settings import DEBUG,policy_content_url,policy_content_url_test
from common.util.commondao import MysqlCommonDao
from common.algorithm.common import TfIdf, MMParticiple, individual_tax_decor
from common.util.decorators import metric
from common.util.utils import CollectionsUtil
from mgbase.models.bus_models import TaxKnowledge, TaxExtendQuestion
from mgbase.models.bas_models import TaxBasData, TaxBasKeyword
from common.apps import logger


class AbstractModelMatchedAnswer(object):
    """
    @desc ： （抽象类）根据问题匹配问题和答案
    @author Pings
    @date   2018/05/18
    @version V1.0
    """
    __metaclass__ = ABCMeta

    def start(self, question, show_self=False, qty=10, use_cache=True) -> dict:
        """
        @desc ： 开始匹配
        @author Pings
        @date   2018/05/18
        @param  question   问题
        @param  show_self  是否把匹配答案所属问题显示成扩展问题
        @param  qty        显示相关问题的数量
        @param  use_cache  是否使用缓存
        @return dict
        """
        logger.info("匹配问题:{}".format(question))

        # **对问题进行切分
        word_tuple = self.part_word(question)

        # **根据关键字从缓存中获取匹配的问题和答案
        if use_cache:
            rst = self.get_answer_by_cache(word_tuple)
            if rst:
                return rst

        level1 = level2 = []
        if word_tuple:
            # **查询与关键字相关的知识
            knowledge_tuple = self.get_knowledge_by_words(word_tuple)
            # **计算相关知识的相似度
            knowledge_iter = self.get_similarity(word_tuple, knowledge_tuple)
            # **过滤并排序
            matched_dict = self.filter(knowledge_iter)

            level1 = matched_dict["level1"]
            level2 = matched_dict["level2"]

        return self.get_answer(question, word_tuple, level1, level2, show_self, qty)

    @abstractmethod
    def part_word(self, question) -> tuple:
        """
        @desc ： 分词
        @author Pings
        @date   2018/05/18
        @param  question   问题
        @return tuple      关键字元组
        """
        pass

    @abstractmethod
    def get_answer_by_cache(self, word_tuple) -> dict:
        """
        @desc ： 从缓存中获取答案
        @author Pings
        @date   2018/05/18
        @param  word_tuple   关键字元组
        @return tuple        匹配的答案
        """
        pass

    @abstractmethod
    def get_knowledge_by_words(self, word_tuple) -> tuple:
        """
        @desc ： 查询与关键字相关的知识
        @author Pings
        @date   2018/05/18
        @param  word_tuple   关键字元组
        @return tuple        匹配的知识
        """
        pass

    @abstractmethod
    def get_similarity(self, word_tuple, knowledge_tuple) -> iter:
        """
        @desc ： 计算相似度（一条知识匹配多个扩展问题的，取最大扩展问题的相似度）
        @author Pings
        @date   2018/05/18
        @param  word_tuple       关键字元组
        @param  knowledge_tuple  匹配的知识元组
        @return iter             匹配的知识id、相似度及相似度最高的扩展问题id
        """
        pass

    @abstractmethod
    def filter(self, knowledge_iter) -> dict:
        """
        @desc ： 根据上下限阈值对相似度进行排序并分级
        @author Pings
        @date   2018/05/18
        @param  knowledge_iter   匹配的知识id及相似度
        @return dict
        """
        pass

    @abstractmethod
    def get_policy_content(self, question, answer)  -> tuple:
        """
        @desc ： 调用接口获取相关政策文件
        @author Pings
        @date   2018/05/18
        @param  question 用户的问题
        @param  answer   匹配的答案
        @return tuple
        """
        pass

    @abstractmethod
    def get_answer(self, question, word_tuple, level1, level2, show_self=False, q=10, use_cache=True) -> dict:
        """
        @desc ： 生成最终结果
        @author Pings
        @date   2018/05/21
        @param  question     问题
        @param  word_tuple   关键字元组
        @param  level1       >=上限阈值的知识
        @param  level2       >=下限阈值 and  <上限阈值的知识
        @param  show_self    是否把匹配答案所属问题显示成扩展问题
        @param  q            显示相关问题的数量
        @param  use_cache  是否使用缓存
        @return dict
        """
        pass


class BaseModelMatchedAnswer(AbstractModelMatchedAnswer):
    """
    @desc ： 基础的根据问题匹配问题和答案
    @author  Pings
    @date    2018/05/18
    @version V1.0

    @version V1.1
    Pings 2018-05-29  相似度公式修改
    """
    CACHE_KEY_ANSWER = "answer"

    # **分词
    participle = MMParticiple()
    dao = MysqlCommonDao()

    def part_word(self, question) -> tuple:
        return self.participle.start(question)

    def get_answer_by_cache(self, word_tuple) -> dict:
        return cache.get(self._get_cache_key(word_tuple))

    def get_knowledge_by_words(self, word_tuple) -> tuple:
        keywords = ",".join(["'{0}'".format(key) for key in set(word_tuple)])
        sql = '''select h.knowledge_id,q1.extend_question_id,q1.weighted_value,q1.keyword 
                   from tax_extend_question_header h,tax_extend_question q1,
                       (select extend_question_id
                          from tax_extend_question
                          where keyword in ({0})
                          group by extend_question_id) q2
                  where h.id = q1.extend_question_id and q1.extend_question_id = q2.extend_question_id
                  order by h.knowledge_id,q1.extend_question_id'''.format(keywords)
        return tuple(self.dao.findall(sql))

    def get_similarity(self, word_tuple, knowledge_tuple) -> iter:
        def get_similarity_inner(knowledge_group_tuple):
            """
            计算相似度
            Pings 2018-05-29  相似度公式修改
            """
            max_similarity = -1
            extend_question_id = 0

            for extend_question in groupby(knowledge_group_tuple[1], itemgetter("extend_question_id")):
                match_weight_sum = 0
                no_match_weight_sum = 0
                extend_matched_len = 0

                extend_question_tuple = tuple(extend_question[1])
                for question in extend_question_tuple:
                    if question["keyword"] in word_tuple:
                        match_weight_sum += question["weighted_value"]
                        extend_matched_len += 1
                    else:
                        no_match_weight_sum += question["weighted_value"]

                similarity = TfIdf.similarity(match_weight_sum, no_match_weight_sum, len(word_tuple),
                                              len(extend_question_tuple), extend_matched_len)

                if max_similarity < similarity:
                    max_similarity = similarity
                    extend_question_id = extend_question[0]

            return {"knowledge_id": knowledge_group_tuple[0], "similarity": max_similarity, "extend_question_id": extend_question_id}

        return map(get_similarity_inner, groupby(knowledge_tuple, itemgetter("knowledge_id")))

    def filter(self, knowledge_iter) -> dict:
        level1 = []
        level2 = []

        # **上限阈值/下限阈值
        min_value = TaxBasData.get("THRESHOLD_MIN").value
        max_value = TaxBasData.get("THRESHOLD_MAX").value

        for knowledge_dict in knowledge_iter:
            similarity = knowledge_dict["similarity"]
            # **相似度大于等于max_value的为第一级
            if similarity >= max_value:
                level1.append(knowledge_dict)
            # **相似度大于等于min_value并且小于max_value的为第二级
            elif min_value <= similarity < max_value:
                level2.append(knowledge_dict)

        # **相似度降序
        if level1:
            level1.sort(key=lambda knowledge: knowledge["similarity"], reverse=True)
        if level2:
            level2.sort(key=lambda knowledge: knowledge["similarity"], reverse=True)

        return {"level1": tuple(level1), "level2": tuple(level2)}

    def get_policy_content(self, question, answer) -> tuple:
        url = policy_content_url_test if DEBUG else policy_content_url
        url += question
        try:
            req = requests.get(url)

            if req.status_code != 200:
                logger.error("调用政策法规接口失败......")
                rst = ()
            else:
                logger.info("调用政策法规接口成功......")
                rst = req.json()["response"]["docs"]
        except BaseException as error:
            logger.error(error.args)
            rst = ()

        return rst

    @individual_tax_decor
    def get_answer(self, question, word_tuple, level1, level2, show_self=False, q=10, use_cache=True) -> dict:
        policy_content = self.get_policy_content(question, "")
        end = q

        if not level1 and not level2 and not policy_content:
            rst = {"token": 0, "content": "无匹配结果，请重新输入问题"}
        else:
            answer = ""
            qes = []
            pid = "knowledge_id"
            if level1:
                answer = TaxKnowledge.objects.get(id=level1[0][pid]).sd_answer

                s = 0 if show_self else 1
                end = q - (len(level1) - s)

                qes += [{"id": i[pid], "question": TaxKnowledge.objects.get(id=i[pid]).sd_question} for i in level1[s:q+s]]
            if level2 and end > 0:
                qes += [{"id": i[pid], "question": TaxKnowledge.objects.get(id=i[pid]).sd_question} for i in level2[:end]]

            rst = {"token": 1, "content": {"question": question, "answer": answer,
                                           "policyContent": policy_content,
                                           "relativeQuestionList": qes}}
        if use_cache:
            self._set_answer_by_cache(word_tuple, rst)
        return rst

    def _get_cache_key(self, word_tuple) -> str:
        """
        @desc ： 根据关键字元组获取缓存的键值
        @author  Pings
        @date    2018/05/18
        @param   word_tuple 问题分词结果
        @return  str        缓存的键值
        """
        return self.CACHE_KEY_ANSWER + "_" + "_".join(word_tuple)

    def _set_answer_by_cache(self, word_tuple, answer) -> None:
        """
        @desc ：  把答案存储在缓存中
        @author  Pings
        @date    2018/05/18
        @param   word_tuple 问题分词结果
        @return  answer     回答
        """
        return cache.set(self._get_cache_key(word_tuple), answer)

    @staticmethod
    def delete_cache_by_question(question) -> None:
        """
        @desc ：  删除问题的缓存
        @author  Pings
        @date    2018/05/18
        @param   question   问题
        """
        word_tuple = BaseModelMatchedAnswer.participle.start(question)
        return BaseModelMatchedAnswer.delete_cache(word_tuple)

    @staticmethod
    def delete_cache(word_tuple) -> None:
        """
        @desc ：  删除问题的缓存
        @author  Pings
        @date    2018/05/18
        @param   word_tuple   问题分词结果
        """
        for w in word_tuple:
            cache.delete_pattern("{0}_{1}_*".format(BaseModelMatchedAnswer.CACHE_KEY_ANSWER, w))

    @staticmethod
    def delete_all_cache() -> None:
        """
        @desc ：  删除所有问题的缓存
        @author  Pings
        @date    2018/05/22
        """
        cache.delete_pattern("{0}_*".format(BaseModelMatchedAnswer.CACHE_KEY_ANSWER))


class BaseModelMatchedRelative(BaseModelMatchedAnswer):
    """
    @desc ： 基础的根据问题匹配相关问题
    @author  Pings
    @date    2018/05/21
    @version V1.0
    """
    def filter(self, knowledge_iter) -> dict:
        # **专家调整下限阈值
        min_value = TaxBasData.get("THRESHOLD_MIN_ADJUST").value

        level2 = [i for i in knowledge_iter if i["similarity"] >= min_value]

        # **相似度降序
        if level2:
            level2.sort(key=lambda knowledge: knowledge["similarity"], reverse=True)

        return {"level1": tuple(), "level2": tuple(level2)}

    def get_answer(self, question, word_tuple, level1, level2, show_self=False, q=10, use_cache=False) -> dict:
        level = level2

        if not level:
            rst = {"token": 0, "content": "无匹配结果，请重新输入问题"}
        else:
            qes = []

            for i in level:
                eid = i["extend_question_id"]
                # **问题
                question = TaxKnowledge.objects.get(id=i["knowledge_id"]).sd_question
                # **扩展问题
                sql = "select keyword,weighted_value from tax_extend_question where extend_question_id = %s"
                extend_question = {q["keyword"]: q["weighted_value"] for q in self.dao.findall(sql, [eid])}
                # **匹配的关键字
                match_keywords = [w for w in word_tuple if w in extend_question]

                qes.append({"id": eid, "best_point": i["similarity"], "question": question,
                            "extend_question": extend_question, "match_keywords": match_keywords})

            rst = {"token": 1, "content": {"question": question, "relativeQuestionList": qes}}

        return rst


class SynonymeModelMatchedAnswer(BaseModelMatchedAnswer):
    """
    @desc ： 根据问题匹配问题和答案(包含同义词)
    @author  Pings
    @date    2018/08/15
    @version V1.4
    """

    def get_knowledge_by_words(self, word_tuple) -> tuple:
        # **查找全局同义词
        sql = '''select '{0}' keyword,concat(group_concat(keyword), ',',group_concat(word)) synonym
                   from tax_bas_synonym
                   where keyword = '{0}' or word = '{0}'
              '''
        sql = " union ".join((sql.format(w) for w in set(word_tuple)))
        synonyms = (d for d in self.dao.findall(sql) if d["synonym"])
        synonyms = set(list(word_tuple) + [k for d in synonyms for k in d["synonym"].split(",")])

        keywords = ",".join(("'{0}'".format(key) for key in synonyms))

        # **查找包含关键字的扩展问题
        sql = '''select h.knowledge_id,q1.extend_question_id,q1.weighted_value,q1.keyword,
                        group_concat(qs.word) synonym              
                   from tax_extend_question_header h
                   inner join tax_extend_question q1 on h.id = q1.extend_question_id
                   inner join 
                        (select q.extend_question_id 
                           from tax_extend_question q
                           where q.keyword in ({0})
                           group by q.extend_question_id
                         union
                         select q.extend_question_id 
                           from tax_extend_question q
                           left join tax_extend_question_synonym qs on q.id = qs.extend_question_id
                           where qs.word in ({0})
                           group by q.extend_question_id) q2
                        on q1.extend_question_id = q2.extend_question_id
                   left join tax_extend_question_synonym qs on q1.id = qs.extend_question_id
                   group by h.knowledge_id,q1.extend_question_id,q1.weighted_value,q1.keyword
                   order by h.knowledge_id,q1.extend_question_id'''.format(keywords)
        knowledge_list = self.dao.findall(sql)
        for knowledge in knowledge_list:
            knowledge["keyword"] = tuple([knowledge["keyword"]] + knowledge["synonym"].split(
                ",")) if knowledge["synonym"] else (knowledge["keyword"],)
            del knowledge["synonym"]

        return tuple(knowledge_list)

    def get_similarity(self, word_tuple, knowledge_tuple) -> iter:
        def get_similarity_inner(knowledge_group_tuple):
            max_similarity, extend_question_id, extend_keywords, match_keywords = -1, 0, None, None

            for extend_question in groupby(knowledge_group_tuple[1], itemgetter("extend_question_id")):
                match_weight_sum = no_match_weight_sum = extend_matched_len = 0
                extend_keyword_list, match_keyword_list = [], []

                extend_question_tuple = tuple(extend_question[1])
                for question in extend_question_tuple:
                    extend_keyword_list.append(tuple((question["keyword"], question["weighted_value"])))
                    # **查找扩展问题关键字集合与问题关键字集合的并集
                    intersection_iter = filter(lambda s: len(s & set(question["keyword"])) > 0, word_list)
                    # **如果有并集则匹配
                    if len(tuple(intersection_iter)):
                        match_weight_sum += question["weighted_value"]
                        extend_matched_len += 1
                        match_keyword_list.append(question["keyword"])
                    else:
                        no_match_weight_sum += question["weighted_value"]

                similarity = TfIdf.similarity(match_weight_sum, no_match_weight_sum, len(word_tuple),
                                              len(extend_question_tuple), extend_matched_len)

                if max_similarity < similarity:
                    max_similarity, extend_question_id = similarity, extend_question[0]
                    extend_keywords, match_keywords = extend_keyword_list, match_keyword_list

            return {"knowledge_id": knowledge_group_tuple[0], "similarity": max_similarity,
                    "extend_question_id": extend_question_id, "match_keywords": match_keywords,
                    "extend_question": extend_keywords}

        sql = '''select '{0}' keyword,concat(group_concat(keyword), ',',group_concat(word)) synonym
                   from tax_bas_synonym
                   where keyword = '{0}' or word = '{0}'
              '''
        sql = " union ".join((sql.format(w) for w in set(word_tuple)))
        synonym_list = (d for d in self.dao.findall(sql) if d["synonym"])

        # **问题关键字(包含全局同义词)
        def get_synonym(word):
            """根据问题的关键字获取全局同义词"""
            synon = tuple(filter(lambda d: d["keyword"] == word, synonym_list))
            return set([word] + synon[0]["synonym"].split(",")) if len(synon) else {word}
        word_list = [get_synonym(word) for word in set(word_tuple)]

        return map(get_similarity_inner, groupby(knowledge_tuple, itemgetter("knowledge_id")))


class SynonymeModelMatchedRelative(SynonymeModelMatchedAnswer):
    """
    @desc ： 根据问题匹配相关问题(包含同义词)
    @author  Pings
    @date    2018/08/16
    @version V1.4
    """
    def filter(self, knowledge_iter) -> dict:
        # **专家调整下限阈值
        min_value = TaxBasData.get("THRESHOLD_MIN_ADJUST").value

        level2 = [i for i in knowledge_iter if i["similarity"] >= min_value]

        # **相似度降序
        if level2:
            level2.sort(key=lambda knowledge: knowledge["similarity"], reverse=True)

        return {"level1": tuple(), "level2": tuple(level2)}

    def get_answer(self, question, word_tuple, level1, level2, show_self=False, q=10, use_cache=False) -> dict:
        level = level2

        if not level:
            rst = {"token": 0, "content": "无匹配结果，请重新输入问题"}
        else:
            qes = []

            for i in level:
                # **问题
                question = TaxKnowledge.objects.get(id=i["knowledge_id"]).sd_question
                # **扩展问题
                extend_question = {(" | ").join(i[0]): i[1] for i in i["extend_question"]}
                # **匹配的关键字
                match_keywords = [(" | ").join(s) for s in i["match_keywords"]]

                qes.append({"id": i["extend_question_id"], "best_point": i["similarity"],
                            "question": question, "extend_question": extend_question,
                            "match_keywords": match_keywords})

            rst = {"token": 1, "content": {"question": question, "words": word_tuple,
                                           "relativeQuestionList": qes}}

        return rst


class Util(object):
    """
    @desc ： tf/idf/weight算法
    @author  Pings
    @date    2018/05/17
    @version V1.0
    """

    dao = MysqlCommonDao()
    matched_answer = SynonymeModelMatchedAnswer()
    matched_relative = SynonymeModelMatchedRelative()
    participle = MMParticiple()

    @staticmethod
    def part(question) -> list:
        """
        @desc ： 分词
        @author Pings
        @date   2018/05/21
        @param  question     需要分词的问题
        @return list
        """
        word_tuple = Util.participle.start(question)
        return [{"keyword": key} for key in word_tuple]

    @staticmethod
    def modify_weights_by_amplification(keyword, amplification) -> bool:
        """
        @desc ： 根据关键词的全局放大倍数修改权重
        @author Pings
        @date   2018/05/14
        @param  keyword       关键词
        @param  amplification 全局放大倍数
        @return boolean
        """
        Util.dao.execute('''UPDATE tax_extend_question h SET h.weighted_value = round(h.amplification * h.tf_value * 
                            h.idf_value * %s, 6) where h.keyword = %s''', [amplification, keyword])
        return True

    @staticmethod
    def get_weighted_by_amplification(extend_question_id, amplification) -> dict:
        """
        @desc ： 根据扩展问题明细id和临时的放大倍数计算权重
        @author  Pings
        @date：  2018/05/14
        @param   extend_question_id   扩展问题明细id
        @param   amplification        临时的局部放大倍数
        @return：dict   例如：{'weighted_value': 0.868}
        """
        extend_question = TaxExtendQuestion.objects.get(id=extend_question_id)
        global_amplification = TaxBasKeyword.objects.get(keyword=extend_question.keyword).amplification
        value = TfIdf.weighted(extend_question.tf_value, extend_question.idf_value, amplification, global_amplification)

        return {'weighted_value': value}

    @staticmethod
    def modify_values_by_id(knowledge_id) -> bool:
        """
        @desc ： 根据知识id修改扩展问题明细的tf/idf/weight
        @author Pings
        @date   2018/05/14
        @param  knowledge_id   知识id
        @return boolean
        """
        def tf(question_group_tuple):
            """计算关键字的tf"""
            # **计算每个关键字在扩展问题明细中出现的次数
            question_tuple = tuple(question_group_tuple[1])
            keyword_tuple = tuple(question["keyword"] for question in question_tuple)
            counter = Counter(keyword_tuple)

            total = len(keyword_tuple)
            for question in question_tuple:
                question["tf"] = TfIdf.tf(counter.get(question["keyword"]), total)

            return question_tuple

        def get_values(extend_question, qty):
            """获取tf/idf/weight/扩展问题明细id"""
            # **tf
            tfv = extend_question["tf"]
            # **计算idf
            idf = Util.__idf(extend_question["keyword"], qty)
            # **计算weight
            weight = TfIdf.weighted(tfv, idf, extend_question["amplification"],
                                    extend_question["global_amplification"])
            return tfv, idf, weight, extend_question["extend_question_id"]

        # **查询知识的扩展问题
        sql = '''select h.id,q.id extend_question_id,q.keyword,q.amplification,
                        k.amplification global_amplification
                   from tax_extend_question_header h
                   left join tax_extend_question q on h.id = q.extend_question_id
                   left join tax_bas_keyword k on k.keyword = q.keyword
                   where h.knowledge_id = %s
                   order by h.id'''
        extend_question_list = Util.dao.findall(sql, [knowledge_id])

        # **计算tf
        extend_question_iter = map(tf, groupby(extend_question_list, itemgetter("id")))

        # **tf/idf/weight/扩展问题明细id
        knowledge_qty = TaxKnowledge.objects.count()
        values_iter = (get_values(extend_question, knowledge_qty)
                       for extend_question_tuple in extend_question_iter
                       for extend_question in extend_question_tuple)

        # **批量修改tf/idf/weight
        sql = '''update tax_extend_question set tf_value = %s, idf_value = %s,
                        weighted_value = %s where id = %s'''
        Util.dao.executemany(sql, values_iter)

        return True

    @staticmethod
    def modify_all_values() -> bool:
        """
        @desc ： 修改所有扩展问题明细的idf/weight(使用多进程，未成功)
        @author Pings
        @date   2018/05/15
        @return boolean
        """
        qty = 10          # **进程的数量
        threshold = 2000  # **启用多个进程的阈值

        def set_task(que, key_query_set):
            """把所有的关键字分成10个任务"""
            keyword_iter = CollectionsUtil.split(key_query_set, threshold, qty)
            for i in keyword_iter:
                que.put(i)

        def get_task(que):
            """获取关键字任务，根据关键字修改扩展问题明细表的idf和权重"""
            def get_idf_weighted(keyword_dict):
                """获取idf和全局放大倍数"""
                idf = Util.__idf(keyword_dict["keyword"], knowledge_qty)
                global_amplification = keyword_dict["amplification"]
                keyword = keyword_dict["keyword"]
                return idf, idf, global_amplification, keyword

            keyword_list = que.get(block=False)
            knowledge_qty = TaxKnowledge.objects.count()

            sql = '''update tax_extend_question h set idf_value = %s, h.weighted_value =
                            round(h.tf_value * %s  * h.amplification * %s, 6), edit_who = 0, 
                            edit_time = now() where h.keyword = %s'''
            keyword_tuple = tuple(get_idf_weighted(i) for i in keyword_list)
            Util.dao.executemany(sql, keyword_tuple)

        keyword_query_set = TaxBasKeyword.objects.values("id", "keyword", "amplification")

        queue = multiprocessing.Queue()
        set_task(queue, keyword_query_set)
        count = 1 if len(keyword_query_set) < threshold else qty
        for _ in range(count):
            get_task(queue)

        return True

    @staticmethod
    def modify_amplification_by_step(extend_question_id, matched_keyword_list, oper_type) -> bool:
        """
        @desc ： 根据步长修改匹配的关键字局部放大倍数
        @author Pings
        @date   2018/05/17
        @param  extend_question_id    扩展问题明细id
        @param  matched_keyword_list  匹配的关键字
        @param  oper_type             操作类型(0奖励，1惩罚)
        @return boolean
        """
        base_data = TaxBasData.objects.get(code="MODIFY_STEP")
        keywords = ",".join(["'{0}'".format(key) for key in matched_keyword_list])

        sql = '''update tax_extend_question h,tax_bas_keyword k
                    set h.amplification = round(h.amplification * %s, 2),
                        h.weighted_value = round(h.tf_value * h.idf_value * h.amplification * k.amplification * %s, 6)
                  where h.keyword = k.keyword and h.extend_question_id = %s and h.keyword in ({0})'''.format(keywords)
        coefficient = 1 + base_data.value if oper_type == "0" else 1 - base_data.value
        Util.dao.execute(sql, [coefficient, coefficient, extend_question_id])

    @staticmethod
    def model_matched_answer(sentence, show_self=False, qty=10, use_cache=True) -> dict:
        """
        @desc ： 根据问题匹配问题和答案
        @author Pings
        @date   2018/05/17
        @param  sentence    问题
        @param  show_self   是否把匹配答案所属问题显示成扩展问题
        @param  qty         显示相关问题的数量
        @param  use_cache   是否使用缓存
        @return dict
        """
        return Util.matched_answer.start(sentence, show_self, qty, use_cache)

    @staticmethod
    def model_matched_relative(sentence) -> dict:
        """
        @desc ： 根据问题匹配相关问题
        @author Pings
        @date   2018/05/17
        @param  sentence    问题
        @return dict
        """
        return Util.matched_relative.start(sentence, use_cache=False)

    @staticmethod
    def __idf(keyword, knowledge_qty) -> decimal:
        """计算关键字的idf"""

        # **关键字出现在多少条知识中
        sql = '''select count(*) count
                   from 
                   (select h.knowledge_id
                      from tax_extend_question_header h
                      left join tax_extend_question q on h.id = q.extend_question_id
                      where q.keyword = %s
                      group by h.knowledge_id)tmp'''
        keyword_qty = Util.dao.findone(sql, [keyword])["count"]

        return TfIdf.idf(keyword_qty, knowledge_qty) if keyword_qty else 0
