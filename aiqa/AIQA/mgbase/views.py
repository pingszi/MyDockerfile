import json
import time
import os
import re
import xlrd
import io

from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.db import connection,transaction
from django.utils.http import urlquote
from xadmin.views.base import CommAdminView
from mgbase.models.bus_models import TaxKnowledge, TaxExtendQuestionHeader
from mgbase.models.bus_models import TaxQuestionSession, TaxSolveUnSolve, TaxExtendQuestionSynonym

from .apps import logger
from common.algorithm.common import *
from common.algorithm.keyword_weighted import *
from common.util.commondao import *
from common.util.utils import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class InitWeightedValueAdminView(CommAdminView):
    """
    @desc ： 初始化权重，xadmin的adminview
    @author pings
    @date   2018/04/19
    @return httpresponse
    """
    def post(self, request, *args, **kwargs):
        logger.info("初始化权重......")

        rst = Util.modify_all_values()
        return HttpResponse(json.dumps({"rst": rst}, ensure_ascii=False))


class UploadKnowledgeAdminView(CommAdminView):
    """
    @desc ：上传知识，xadmin的adminview
    @author XuJJ
    @date   2018/07/10
    @return httpresponse
    """
    def post(self, request, *args, **kwargs):

        def UploadKnowledgeAdminView_post_main() -> str:
            logger.info("上传知识......")

            #返回结果
            rst = ""

            #获取上传表格
            excel_file = request.FILES.get('file').read()

            #创建文件名
            file_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) 
            source = '%s/upload/%s.xlsx' % (BASE_DIR,file_name)
            if not os.path.exists('%s/upload/' % BASE_DIR):
                os.mkdir('%s/upload/' % BASE_DIR)

            #保存文件
            with open(source, 'wb') as f:
                f.write(excel_file)

            #打开表格
            data = xlrd.open_workbook(source)
            table = data.sheets()[0]
            nrows = table.nrows
            result=[]
            if nrows <= 1:
                rst += '上传数据的为空'
            for i in range(0, nrows):
                rows = table.row_values(i)
                if i == 0:
                    continue
                #判断关键字是否为空
                if rows[2] == '' or rows[3] == '' or rows[6] == '':
                    rst += '第%s行有必填项为空' % (i+1) + '\n'
                    continue
                
                #问题去重
                repeat_list = TaxKnowledge.objects.filter(sd_question=str(rows[2]))
                if len(repeat_list) > 0:
                    rst += '第%s行问题已经存在' % (i+1) + '\n'
                    continue
                
                #检测扩展跟关键字数量是否对应
                extend_list = str(rows[3]).split('\n')
                keyword_list = str(rows[4]).split('\n')
                if len(extend_list) != len(keyword_list) and rows[4] != '':
                    rst += '第%s行扩展问题数量跟关键字数量不一致' % (i+1) + '\n'
                    continue

                #知识问题等数据插入
                def UploadKnowledgeAdminView_post_main_insert() -> str:
                    #创建知识sql先不保存
                    knowledge = TaxKnowledge(sd_question=str(rows[2]),sd_answer=str(rows[6]))

                    keyword_count=0

                    #拆分扩展问题
                    for m in range(len(extend_list)):
                        extend = extend_list[m]

                        keyword_ar = []
                        #判断是否自带关键字,如无则自动分词
                        if len(keyword_list) == len(extend_list) and keyword_list[0] != '':
                            keywords = keyword_list[m]
                            el = '\[(.*?)\]'
                            matchers = re.compile(el).findall(keywords)
                            for key_one in matchers:
                                keyword_ar.append(key_one)
                        else:
                            keywords = Util.part(extend)
                            if len(keywords) == 0:
                                #不能分出关键字 整条忽略
                                raise Exception('第%s行关键字无可用分词' % (i+1) + '\n')
                            else:
                                for key_one in keywords:
                                    keyword_ar.append(key_one['keyword'])
                        
                        
                        #保存知识
                        knowledge.save()
                        #保存扩展问题
                        extend_question_header = TaxExtendQuestionHeader(knowledge=knowledge,desc=extend)
                        extend_question_header.save()
                        
                        for key_one in keyword_ar:
                            # **关键字不存在则创建关键字
                            TaxBasKeyword.objects.get_or_create(keyword=key_one)

                            # **放大倍数
                            amplification = 1

                            TaxExtendQuestion.objects.create(extend_question=extend_question_header, keyword=key_one,
                                                    amplification=amplification)
                        
                            keyword_count += 1
                    
                    # **更新本条知识的tf值
                    if keyword_count:
                        Util.modify_values_by_id(knowledge.id)
                    
                    # **使相关缓存失效
                    BaseModelMatchedAnswer.delete_cache_by_question(str(knowledge.sd_question))

                    return ""

                
                try:
                    #开启事务
                    with transaction.atomic():
                        rst += UploadKnowledgeAdminView_post_main_insert()
                except Exception as e:
                    rst += str(e)


            return rst
        
        try:
            rst = UploadKnowledgeAdminView_post_main()
            if rst == "":
                rst = "上传成功"
        except Exception as e:
            logger.info(e)
            rst = '意外问题'

        
        return HttpResponse(json.dumps({"rst": rst}, ensure_ascii=False))

class UploadKnowledgeSynonymAdminView(CommAdminView):
    def post(self, request, *args, **kwargs):
        def UploadKnowledgeSynonymAdminView_post_main() -> str:
            logger.info("上传知识-同义词......")

            #返回结果
            rst = ""

            #获取上传表格
            excel_file = request.FILES.get('file').read()

            #创建文件名
            file_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) 
            source = '%s/upload/%s.xlsx' % (BASE_DIR,file_name)
            if not os.path.exists('%s/upload/' % BASE_DIR):
                os.mkdir('%s/upload/' % BASE_DIR)

            #保存文件
            with open(source, 'wb') as f:
                f.write(excel_file)

            #打开表格
            data = xlrd.open_workbook(source)
            table = data.sheets()[0]
            nrows = table.nrows
            result=[]
            if nrows <= 1:
                rst += '上传数据的为空'
            #本地知识所有标题
            local_knowledge_ar = []
            #开始批量判断
            for i in range(0, nrows):
                rows = table.row_values(i)
                if i == 0:
                    continue
                #判断关键字是否为空
                if rows[1] == '' or rows[2] == '' or rows[4] == '':
                    rst += '第%s行有关键字为空' % (i+1) + '\n'
                    continue
                
                #检测扩展跟关键字数量是否对应
                extend_list = str(rows[2]).split('\n')
                keyword_list = str(rows[3]).split('\n')
                if len(extend_list) != len(keyword_list) and rows[3] != '':
                    rst += '第%s行扩展问题数量跟分词结果数量不一致' % (i+1) + '\n'
                    continue
                
                if rows[1] in local_knowledge_ar:
                    rst += '第%s行存在重复的知识' % (i+1) + '\n'
                    continue
                else:
                    local_knowledge_ar.append(rows[1])

                #检测格式是否有1.
                for extend in extend_list:
                    ifmatch = re.compile('^\d{1,3}\.').findall(extend)
                    if len(ifmatch) == 0:
                        rst += '第%s行扩展问题格式不正确' % (i+1) + '\n'
                        break

                #如无分词结果，检测是否能分词
                if rows[3] == '':
                    for extend in extend_list:
                        #检查扩展问题是否能分词
                        keywords = Util.part(extend)
                        if len(keywords) == 0:
                            #不能分出关键字 整条忽略
                            rst += '第%s行扩展问题无法分词' % (i+1) + '\n'
                            continue
                else:
                    for keywords in keyword_list:
                        #检测格式是否有1.
                        ifmatch = re.compile('^\d{1,3}\.').findall(keywords)
                        if len(ifmatch) == 0:
                            rst += '第%s行分词结果格式不正确' % (i+1) + '\n'
                            break
                        #检测是否包含有关键字
                        el = '\[([^\[\]]*?)\]'
                        matchers = re.compile(el).findall(keywords)
                        if len(matchers) == 0:
                            #检测内容是否有关键词
                            rst += '第%s行分词结果无有效关键字' % (i+1) + '\n'
                            continue
            
            #如无问题开始进行入库
            if rst=='':
                #获取数据库知识所有标题
                sql_knowledge_ar = []
                sql_knowledge_dict = TaxKnowledge.objects.values('sd_question')
                for skd in sql_knowledge_dict:
                    sql_knowledge_ar.append(skd['sd_question'])
                
                #获取数据库知识所有关键字
                local_keyword_ar = []
                sql_keyword_ar = []
                sql_keyword_dict = TaxBasKeyword.objects.values('keyword')
                for skd in sql_keyword_dict:
                    sql_keyword_ar.append(skd['keyword'])
                
                #保存知识数组
                knowledge_ar = []

                #开始导入
                for i in range(0, nrows):
                    rows = table.row_values(i)
                    if i == 0:
                        continue
                    
                    #税种处理
                    tax_type_ar = str(rows[0]).split('\n')
                    tax_type = ','.join(tax_type_ar)
                    
                    #分解扩展问题与分词结果
                    extend_list = str(rows[2]).split('\n')
                    keyword_list = str(rows[3]).split('\n')

                    '''如数据库有重复知识，覆盖'''
                    if rows[1] in sql_knowledge_ar:
                        TaxKnowledge.objects.filter(sd_question=str(rows[1])).delete()

                    #保存知识
                    knowledge = TaxKnowledge(sd_question=str(rows[1]),sd_answer=str(rows[4]),class_tag=str(tax_type))
                    knowledge.save()
                    knowledge_ar.append(knowledge)

                    keyword_count=0
                    for m in range(len(extend_list)):
                        extend = extend_list[m]
                        extend = re.compile('^\d{1,3}\.').sub('',extend)

                        keyword_ar = []
                        #判断是否自带关键字,如无则自动分词
                        if rows[3] == '':
                            keywords = Util.part(extend)
                            for key_one in keywords:
                                keyword_ar.append(key_one['keyword'])
                        else:
                            keywords = keyword_list[m]
                            el = '\[([^\[\]]*?)\]'
                            matchers = re.compile(el).findall(keywords)
                            for key_one in matchers:
                                keyword_ar.append(key_one)
                        
                        #保存扩展问题
                        extend_question_header = TaxExtendQuestionHeader(knowledge=knowledge,desc=extend)
                        extend_question_header.save()

                        for key_one in keyword_ar:
                            key_one_u = key_one.strip()
                            key_word = key_one_u
                            synonym_ar = []
                            #拆分同义词
                            if '|' in key_one_u:
                                key_words = key_one_u.split('|')
                                key_word = key_words[0]
                                synonym_ar = key_words[1:]

                            # **关键字不存在则创建关键字
                            if key_word not in sql_keyword_ar:
                                if key_word not in local_keyword_ar:
                                    local_keyword_ar.append(key_word)

                            # **放大倍数
                            amplification = 1

                            TaxExtend = TaxExtendQuestion(extend_question=extend_question_header, keyword=key_word,
                                                    amplification=amplification)
                            TaxExtend.save()
                            
                            # **如有同义词则创建同义词
                            for synonym in synonym_ar:
                                TaxExtendQuestionSynonym.objects.create(extend_question=TaxExtend,word=synonym)
                        
                            keyword_count += 1
                
                #批量插入关键字
                local_keyword_ar_sql = []
                for item in local_keyword_ar:
                    local_keyword_ar_sql.append(TaxBasKeyword(keyword=item)) 
                TaxBasKeyword.objects.bulk_create(local_keyword_ar_sql)

                for knowledge in knowledge_ar:
                    # **更新本条知识的tf值
                    Util.modify_values_by_id(knowledge.id)
                    
                    # **使相关缓存失效
                    BaseModelMatchedAnswer.delete_cache_by_question(str(knowledge.sd_question))

                
                rst = '成功导入%s条' % (nrows-1)
                logger.info(rst)
            return rst
        
        try:
            rst = UploadKnowledgeSynonymAdminView_post_main()
            if rst == "":
                rst = "上传成功"
        except Exception as e:
            logger.info(e)
            rst = '意外问题'

        
        return HttpResponse(json.dumps({"rst": rst}, ensure_ascii=False))

class ExportTemplateKnowledgeAdminView(CommAdminView):
    """
    @desc ： 导出模板
    @author XuJJ
    @date   2018/08/21
    @return HttpResponse
    """
    def get(self, request, *args, **kwargs):
        logger.info("导出模板......")

        name = request.GET.get("name")

        def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        the_file_name = '%s/mgbase/export_template/%s.xlsx' % (BASE_DIR, name)
        filename = urlquote(name)
        response = StreamingHttpResponse(file_iterator(the_file_name))#这里创建返回
        response['Content-Type'] = 'application/vnd.ms-excel'#注意格式
        response['Content-Disposition'] = 'attachment;filename="%s.xlsx"' % filename
        return response


def validate_knowledge_repeat(request):
    """
    @desc ： 验证知识是否重复
    @author Pings
    @date   2018/04/23
    @return HttpResponse
    """
    question = request.GET.get("question")
    return HttpResponse(json.dumps(Util.model_matched_answer(question, show_self=True), ensure_ascii=False))


def split_knowledge(request):
    """
    @desc ： 对知识的问题分词
    @author Pings
    @date   2018/04/24
    @return HttpResponse
    """
    question = request.GET.get("question")
    return HttpResponse(json.dumps(Util.part(question), ensure_ascii=False))


def get_knowledge(request, knowledgeid):
    """
    @desc ： 根据问题查询知识
    @author Pings
    @date   2018/04/25
    @return HttpResponse
    """
    dao = MysqlCommonDao()

    # **查询扩展问题
    sql = "select id,`desc` from tax_extend_question_header where knowledge_id = %s"
    extend_question_header_list = dao.findall(sql, [knowledgeid])

    # **查询扩展问题明细
    sql = '''select q.id,q.keyword,q.tf_value,q.idf_value,q.weighted_value,q.amplification,
                    group_concat(qs.word separator '|') synonym
               from tax_extend_question q
               left join tax_extend_question_synonym qs on q.id = qs.extend_question_id
               where q.extend_question_id = %s
               group by q.id,q.keyword,q.tf_value,q.idf_value,q.weighted_value,q.amplification 
               order by q.id'''
    for i in extend_question_header_list:
        extend_question_list = dao.findall(sql, [i["id"]])
        for j in extend_question_list:
            if j["synonym"]:
                j["keyword"] = j["keyword"] + "|" + j["synonym"]

        i["extend_question_list"] = extend_question_list

    return HttpResponse(json.dumps({"id": knowledgeid, "list": extend_question_header_list},
                                   ensure_ascii=False, cls=JsonEncoder))


def get_weighted_value(request, extend_question_id, amplification):
    """
    @desc ： 根据扩展问题明细id和临时的放大倍数获取权重
    @author Pings
    @date   2018/04/25
    @return HttpResponse
    """
    return HttpResponse(json.dumps(Util.get_weighted_by_amplification(extend_question_id, amplification),
                                   ensure_ascii=False, cls=JsonEncoder))


def list_knowledge(request):
    """
    @desc ： 根据问题获取匹配的知识
    @author Pings
    @date   2018/05/02
    @return HttpResponse
    """
    question = request.GET.get("question")
    return HttpResponse(json.dumps(Util.model_matched_relative(question), ensure_ascii=False, cls=JsonEncoder))


def modify_amplification(request):
    """
    @desc ： 奖励/惩罚
    @author Pings
    @date   2018/05/02
    @return HttpResponse
    """
    oper_type = request.POST.get("type")
    extend_question_id = request.POST.get("extend_id")
    matched_keyword_list = request.POST.getlist("matched_keywords[]")

    Util.modify_amplification_by_step(extend_question_id, matched_keyword_list, oper_type)

    # **使相关缓存失效
    BaseModelMatchedAnswer.delete_cache(matched_keyword_list)

    return HttpResponse('{"rst": "true"}')
