import xadmin
from xadmin import views
from xadmin.views import ListAdminView

from mgbase.models.bas_models import *
from mgbase.models.bus_models import *
from common.plugins.buttons import *
from common.plugins.upload import *
from common.plugins.export import *
from mgbase.views import *

# **注册Plugin
xadmin.site.register_plugin(CustomExportPlugin, ListAdminView)
xadmin.site.register_plugin(CustomButtonPlugin, ListAdminView)
xadmin.site.register_plugin(CustomUploadPlugin, ListAdminView)

# **注册AdminView
# **初始化权重
xadmin.site.register_view('init_weighted_value', InitWeightedValueAdminView, name='init_weighted_value')
# **上传知识
xadmin.site.register_view('upload_knowledge', UploadKnowledgeAdminView, name='upload_knowledge')
xadmin.site.register_view('upload_synonym_knowledge', UploadKnowledgeSynonymAdminView, name='upload_synonym_knowledge')
# **导出模板
xadmin.site.register_view('export_template_knowledge', ExportTemplateKnowledgeAdminView, name='export_template_knowledge')


class BaseSetting(object):
    """基本管理器配置"""

    # **开启主题功能
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    """全局配置"""

    # **设置base_site.html的Title
    site_title = '智能问答管理系统'
    # **设置base_site.html的Footer
    site_footer = '广东源恒软件科技有限公司'

    # **菜单折叠
    # menu_style = "accordion"

    def get_site_menu(self):
        """自定义菜单"""
        return [{
            'title': '数据统计',
            # 'icon': 'fa fa-users',
            'menus': (
                {'title': '版本信息', 'url': "/datastatistics/version/index"},
                {'title': '访问量统计', 'url': "/datastatistics/visitorvolume/index"},
                {'title': '知识量统计', 'url': "/datastatistics/knowledgeqty/index"},
                {'title': '解决率统计', 'url': "/datastatistics/solverate/index"},
            )
        }]

xadmin.site.register(views.CommAdminView, GlobalSetting)


@xadmin.sites.register(TaxBasData)
class TaxBasDataAdmin(object):
    """基础数据"""
    list_display = ("code", "name", "value", "sort", "desc", "type", "type_desc")
    list_exclude = ("add_who", "add_time", "edit_who", "edit_time") 

    # **筛选器
    search_fields = ("code", "name", "type")    # **搜索字段

    list_per_page = 20
    fields = ("code", "name", "value", "sort", "desc", "type", "type_desc")
    ordering = ("-id",)
    list_editable = ('value',)
    show_bookmarks = False


@xadmin.sites.register(TaxBasStopWord)
class TaxBasStopWordAdmin(object):
    """停用词"""
    list_display = ("word", "add_time")
    list_exclude = ("add_who", "edit_who", "edit_time") 

    # **筛选器
    search_fields = ("word",)    # **搜索字段

    list_per_page = 20
    fields = ('word',)
    ordering = ("-id",)
    list_editable = ('word',)
    show_bookmarks = False


class TaxBasSynonymInline(object):
    """同义词内联"""
    model = TaxBasSynonym
    extra = 0
    exclude = ('add_who', 'edit_who')


@xadmin.sites.register(TaxBasKeyword)
class TaxBasKeywordAdmin(object):
    """关键词"""
    # **关联
    inlines = [TaxBasSynonymInline]
    list_display = ("keyword", "amplification")
    list_exclude = ("add_who", "add_time", "edit_who", "edit_time") 

    # **筛选器
    search_fields = ("keyword",)    # **搜索字段

    list_per_page = 20
    fields = ("keyword", "amplification")
    ordering = ("-id",)
    list_editable = ("keyword",)
    show_bookmarks = False

    def save_models(self):
        # **根据关键词的全局放大倍数修改扩展问题的权重
        Util.modify_weights_by_amplification(self.new_obj.keyword, self.new_obj.amplification)
        self.new_obj.save()

        # **日志
        flag = self.org_obj is None and 'create' or 'change'
        self.log(flag, self.change_message(), self.new_obj)


@xadmin.sites.register(TaxBasSynonym)
class TaxBasSynonymAdmin(object):
    """同义词"""
    list_display = ("keyword", "word")
    list_exclude = ("add_who", "add_time", "edit_who", "edit_time") 

    # **筛选器
    search_fields = ("word",)    # **搜索字段
    list_filter = ("keyword__keyword",)   # **过滤器

    list_per_page = 20
    fields = ("keyword", "word")
    ordering = ("-id",)
    show_bookmarks = False

    def save_models(self):
        # **保存同义词
        synonym = self.new_obj
        synonym.save()
        TaxBasKeyword.objects.get_or_create(keyword=synonym.word)

        # **日志
        flag = self.org_obj is None and 'create' or 'change'
        self.log(flag, self.change_message(), self.new_obj)


@xadmin.sites.register(TaxKnowledge)
class TaxKnowledgeAdmin(object):
    """知识"""
    list_display = ("sd_question", "question_qty")
    list_exclude = ("add_who", "add_time", "edit_who", "edit_time")

    # **筛选器
    search_fields = ("sd_question",)    # **搜索字段

    list_per_page = 20
    fields = ("sd_question", "sd_answer",)
    ordering = ("-id",)
    show_bookmarks = False

    # **自定义按钮，需要注册AdminView(init_weighted_value)
    custom_button = {"value": "初始化权重", "url": "init_weighted_value"}
    # **自定义上传按钮，需要注册AdminView(upload_knowledge)
    custom_upload = {"url": ["upload_knowledge", "upload_synonym_knowledge"]}
    custom_export = {"name": ["模板", "分类同义词模板"]}

    add_form_template = "taxknowledge/tax_knowledge_add.html"
    change_form_template = "taxknowledge/tax_knowledge_modify.html"

    style_fields = {"sd_answer": "ueditor"}

    def save_models(self):
        flag = self.org_obj is None and 'create' or 'change'

        keyword_count = 0

        # **知识
        knowledge = self.new_obj
        knowledge.save()

        if flag == 'change':
            # **删除原来扩展问题
            TaxExtendQuestionHeader.objects.filter(knowledge=knowledge).delete()

        # **扩展问题
        question_index = self.request.POST.getlist("questionIndex")
        desc_list = self.request.POST.getlist("desc")
        extend_question_header_list = [TaxExtendQuestionHeader(
            knowledge=knowledge, desc=i) for i in desc_list]

        # **扩展问题明细
        keyword_prefix = "keyword_"
        amplification_prefix = "amplification_"
        for i, extend_question_header in enumerate(extend_question_header_list):
            # **创建扩展问题
            extend_question_header.save()

            # **关键字
            keyword_key = keyword_prefix + str(question_index[i])
            keyword_list = self.request.POST.getlist(keyword_key)

            # **修改页面，获取放大倍数
            if flag == 'change':
                amplification_key = amplification_prefix + str(question_index[i])
                amplification_list = self.request.POST.getlist(amplification_key)

            for j, keyword in enumerate(keyword_list):
                # **关键字
                keywords = keyword.split("|")

                # **放大倍数
                amplification = 1
                # **修改页面，保存放大倍数
                if flag == 'change':
                    amplification = amplification_list[j]

                extend_obj = TaxExtendQuestion(extend_question=extend_question_header,
                                               keyword=keywords[0], amplification=amplification)
                extend_obj.save()
                TaxBasKeyword.objects.get_or_create(keyword=keywords[0])

                # **保存局部同义词
                if len(keywords) > 1:
                    for word in keywords[1:]:
                        # **保存关键字
                        TaxBasKeyword.objects.get_or_create(keyword=word)
                        # **保存局部同义词
                        TaxExtendQuestionSynonym.objects.create(extend_question=extend_obj,
                                                                word=word)

                keyword_count += 1

        # **更新本条知识的tf值
        if keyword_count:
            Util.modify_values_by_id(knowledge.id)

        # **使相关缓存失效
        BaseModelMatchedAnswer.delete_cache_by_question(knowledge.sd_question)

        # **日志
        self.log(flag, self.change_message(), self.new_obj)


@xadmin.sites.register(TaxKnowledgeProxy)
class TaxKnowledgeProxyAdmin(object):
    """专家调整"""
    list_display = ("id", "sd_question")
    fields = ("id", "sd_question")

    list_per_page = 1
    show_bookmarks = False
    list_export = ()

    # **不显示增删改功能
    remove_permissions = ['add', 'change', 'delete']

    object_list_template = "taxknowledge/tax_specialist_adjust_list.html"
