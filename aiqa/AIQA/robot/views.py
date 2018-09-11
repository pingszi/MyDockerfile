import uuid
import json
import re
import logging

import zmail

from django.http import HttpResponse

from common.algorithm.keyword_weighted import Util
from mgbase.models.bus_models import TaxKnowledge, TaxSolveUnSolve, TaxQuestionSession, TaxUnSolveMail
from mgbase.models.bas_models import TaxBasData
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('robot')

@csrf_exempt
def search(request):
    """
    @desc ： 接受用户问题返回答案
    @author XuJJ
    @date   2018/08/15
    @return HttpResponse
    """
    rst = {'uuid_key': '', 'msg': '意外错误', 'status': 0,'ai_answer': [],'ai_relative_answer':[],'ai_policy_answer':[], 'no_result':0, 'no_relative_result':0, 'no_policy_result':0, 'all_no_answer':'抱歉，您的提问对小穗来说，超纲啦！请在工作时间咨询老师。如有需要，请联系 QQ：4008861778，或致电源恒热线：400-8861-778。', 'question':''}
    
    logger.info("接受参数:%s" % json.loads(request.body.decode("utf-8")))
    
    request_data = json.loads(request.body.decode("utf-8"))
    uuid_exist = request_data.get("uuid_key")
    question = request_data.get("question")
    knowledge_id = request_data.get('knowledge_id')
    client_type = request_data.get('client_type')

    #记录uuid,如无则创建一个
    uuid_key = uuid_exist if uuid_exist else str(uuid.uuid1())
    rst['uuid_key'] = uuid_key
    rst['question'] = question

    if question:
        question = question.strip()
        is_knowledge = True if knowledge_id else False

        #记录客户问答回话,无则创建
        TaxQuestionSession.objects.get_or_create(session_key=uuid_key,source=client_type,status="C")
            
        #查找机器人答案
        ai_rst = Util.model_matched_answer(question)
        ai_answer = ""
        if ai_rst['token'] == 1:
            ai_answer = str(ai_rst['content']['answer'])
            ai_relative_answer = ai_rst['content']['relativeQuestionList']
            ai_policy_answer = ai_rst['content']['policyContent']
            if ai_answer=="":
                rst['no_result'] = 1
            else:
                rst['ai_answer'] = [ai_answer]
            if len(ai_relative_answer) == 0:
                rst['no_relative_result'] = 1
            else:
                rst['ai_relative_answer'] = ai_relative_answer
            if len(ai_policy_answer) == 0:
                rst['no_policy_result'] = 1
            else:
                rst['ai_policy_answer'] = ai_policy_answer
        else:
            rst['no_result'] = 1
            rst['no_relative_result'] = 1
            rst['no_policy_result'] = 1

        #查找映射信息
        session_key = TaxQuestionSession.objects.filter(session_key=uuid_key)[0]

        #记录客户的问题
        TaxSolveUnSolve.objects.create(question=question, is_knowledge=is_knowledge, session_key=session_key, answer=ai_answer, solve=0)
        if is_knowledge:
            knowledge_obj = TaxKnowledge.objects.get(id=knowledge_id)
            knowledge_obj.counter += 1
            knowledge_obj.save(update_fields=['counter'])
        
        rst['msg'] = '成功'
        rst['status'] = 1
    else:
        rst['msg'] = '问题不能为空'
    
    response = HttpResponse(json.dumps(rst, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = "*"
    return response

@csrf_exempt
def unsolved_email(request):
    """
    @desc ： 问题未解决处理方法
    @author XuJJ
    @date   2018/09/03
    @return HttpResponse
    """

    logger.info("接受参数:%s" % json.loads(request.body.decode("utf-8")))
    
    request_data = json.loads(request.body.decode("utf-8"))
    uuid_key = request_data.get("uuid_key")
    email = request_data.get("email")
    question = request_data.get("question")

    #查找老师邮箱
    teacher_email = TaxBasData.get("TEACHER_EMAIL").name
    
    #发送邮件
    def sendEMail(content):
        mail = {
            'subject': '智能问答客户邮件咨询问题',  # Anything you want.
            'content': content,  # Anything you want.
        }
        server = zmail.server('xujunjianyh@163.com', '1qazxsw2') 
        server.send_mail(teacher_email, mail)

    rst = '参数不能为空'
    if uuid_key != '' and email != '': 
        solueUnsolve_sql_datas = TaxSolveUnSolve.objects.filter(session_key=uuid_key).values('question','answer').order_by("add_time")
        solueUnsolve_datas = '邮箱：' + email + '\n' + '问题描述：' + question + '\n' + '\n'
        solueUnsolve_datas += '聊天记录：---------------' + ' ' + '\n' + '\n'
        for item in solueUnsolve_sql_datas:
            answer_notag = re.compile('<[^>]*>').sub('',item['answer']).strip()
            solueUnsolve_datas += '问题：' + item['question'] + '\n' + '机器人答案：' + answer_notag + '\n' + '\n'
        
        #保存邮件记录
        TaxUnSolveMail.objects.create(session_key_id=uuid_key,email=email,desc=question,content=solueUnsolve_datas)
        #发送
        sendEMail(solueUnsolve_datas)
        rst = '成功'

    return HttpResponse(json.dumps(rst, ensure_ascii=False))

def question_resolve(request):
    """
    @desc ： 解决问题，修改当前问题的状态为解决
    @author Pings
    @date   2018/04/28
    @return HttpResponse
    """
    sessid = request.GET.get('uuid_key')
    question = request.GET.get('question')
    solveunsolve_list = TaxSolveUnSolve.objects.filter(question=question, session_key_id=sessid).order_by("-id")

    if solveunsolve_list:
        solveunsolve = solveunsolve_list[0]
        solveunsolve.solve = 1
        solveunsolve.save(update_fields=['solve'])

    return HttpResponse('能够帮助到您，我很开心！如果您还有其他问题请您继续提问')


def question_unresolve(request):
    """
    @desc ： 未解决问题，修改当前问题的状态为未解决
    @author Pings
    @date   2018/04/28
    @return HttpResponse
    """
    sessid = request.GET.get('uuid_key')
    question = request.GET.get('question')
    solveunsolve_list = TaxSolveUnSolve.objects.filter(question=question, session_key_id=sessid).order_by("-id")

    if solveunsolve_list:
        solveunsolve = solveunsolve_list[0]
        solveunsolve.solve = 2
        solveunsolve.save(update_fields=['solve'])

    return HttpResponse('很抱歉，您的问题我暂时无法解答，为了使您更准确的查询到您咨询的信息，请您尝试更改一下提问词汇！')


# 热点问题
def hot_question(request):
    # 去数据库拿出点击次数考前的10个问题
    knowledge_list = TaxKnowledge.objects.order_by("-counter").values('id', 'sd_question')[0:10]

    rst = [{'id': d['id'], 'question': d['sd_question']} for d in knowledge_list]
    return HttpResponse(json.dumps(rst, ensure_ascii=False))


def get_question(request):
    """
    @desc ： 查询问题（对问题切词词后进行模糊匹配）
    @author Pings
    @date   2018/06/07
    @return HttpResponse
    """
    question = request.GET.get("question")

    # **切词
    word_list = Util.part(question)

    # **模糊查询
    query_str = bas_str = "TaxKnowledge.objects"
    for ques in word_list:
        query_str += ".filter(sd_question__contains='{0}')".format(ques["keyword"])

    knowledge_list = eval(query_str + ".values('id', 'sd_question')[:10]") if query_str != bas_str else []
    knowledge_list = [{"id": d["id"], "sd_question": d['sd_question']} for d in knowledge_list]
    rst = {"token": 1 if knowledge_list else 0, "question": question, "match_word": [d["keyword"] for d in word_list],
           "content": knowledge_list}

    return HttpResponse(json.dumps(rst, ensure_ascii=False))
    