from django.conf.urls import url
from mgbase.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # **验证知识是否重复
    url("validate_knowledge_repeat", validate_knowledge_repeat, name="validate_knowledge_repeat"),
    # **对知识的问题分词
    url("split_knowledge", split_knowledge, name="split_knowledge"),
    # **根据问题查询知识
    url("get_knowledge/(\d+)", get_knowledge, name="get_knowledge"),
    # **根据扩展问题明细id和临时的放大倍数获取权重
    url("get_weighted_value/(\d+)/(\S+)", get_weighted_value, name="get_weighted_value"),
    # **根据问题获取匹配的知识
    url("list_knowledge", list_knowledge, name="list_knowledge"),
    # **奖励/惩罚
    url("modify_amplification", modify_amplification, name="modify_amplification"),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
