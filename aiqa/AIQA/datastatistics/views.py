from django.shortcuts import render
from xadmin.views.base import CommAdminView, TemplateResponse


class VersionInfoAdminView(CommAdminView):
    def get_breadcrumb(self):
        """获取头部面包屑导航"""
        breadcrumb = CommAdminView.get_breadcrumb(self)
        breadcrumb.append({'title': '版本信息', 'url': '/datastatistics/version/index'})
        return breadcrumb

    def get(self, request, *args, **kwargs):
        """
        @desc ： 版本信息
        @author  pings
        @date    2018/09/03
        @return  TemplateResponse
        """
        return TemplateResponse(request, 'version_info_index.html', self.get_context())


class VisitorVolumeAdminView(CommAdminView):
    def get_breadcrumb(self):
        """获取头部面包屑导航"""
        breadcrumb = CommAdminView.get_breadcrumb(self)
        breadcrumb.append({'title': '访问量统计', 'url': '/datastatistics/visitorvolume/index'})
        return breadcrumb

    def get(self, request, *args, **kwargs):
        """
        @desc ： 访问量统计
        @author  pings
        @date    2018/09/03
        @return  TemplateResponse
        """
        return TemplateResponse(request, 'visitor_volume_index.html', self.get_context())


class KnowledgeQtyAdminView(CommAdminView):
    def get_breadcrumb(self):
        """获取头部面包屑导航"""
        breadcrumb = CommAdminView.get_breadcrumb(self)
        breadcrumb.append({'title': '知识量统计', 'url': '/datastatistics/knowledgeqty/index'})
        return breadcrumb

    def get(self, request, *args, **kwargs):
        """
        @desc ： 知识量统计
        @author  pings
        @date    2018/09/03
        @return  TemplateResponse
        """
        return TemplateResponse(request, 'knowledge_qty_index.html', self.get_context())


class SolveRateAdminView(CommAdminView):
    def get_breadcrumb(self):
        """获取头部面包屑导航"""
        breadcrumb = CommAdminView.get_breadcrumb(self)
        breadcrumb.append({'title': '解决率统计', 'url': '/datastatistics/solverate/index'})
        return breadcrumb

    def get(self, request, *args, **kwargs):
        """
        @desc ： 解决率统计
        @author  pings
        @date    2018/09/03
        @return  TemplateResponse
        """
        return TemplateResponse(request, 'solve_rate_index.html', self.get_context())
        