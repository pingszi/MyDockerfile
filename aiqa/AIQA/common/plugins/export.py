"""xadmin导出插件"""

from django.forms import Media
from django.template import loader
from xadmin.views import BaseAdminPlugin
from xadmin.plugins.utils import get_context_dict

class CustomExportPlugin(BaseAdminPlugin):
    """
    @desc ：自定义导出按钮
    @author XuJJ
    @date   2018/08/16
    @Version  V1.0
    """

    custom_export = {}

    """
    @desc ： 根据'custom_export'属性值设置是否加载本插件
    @author XuJJ
    @date   2018/08/16
    @return bool
    """
    def init_request(self, *args, **kwargs):
        return bool(self.custom_export)

    """
    @desc ： 拦截返回Media的方法，加入xadmin.plugin.button.js文件
    @author XuJJ
    @date   2018/08/16
    @param  media  包含其他插件的js,css文件
    @return Media
    """
    def get_media(self, media):
        media = media + Media(js=["/static/plugins/js/xadmin.plugin.export.js"])
        return media

    """
    @desc ： 在top_toolbar插入点(view_block)插入按钮
    @author XuJJ
    @date   2018/08/16
    @param  context  TemplateContext
    @param  nodes    包含其他插件的返回内容
    @return 可以直接返回HTML，也可将内容加入到nodes参数中
    """
    def block_top_toolbar(self, context, nodes):
        # **设置页面接收的参数
        context.update({"name": self.custom_export["name"], "value": self.custom_export.get("value", "下载模板")})

        # **把页面内容添加到nodes中
        nodes.append(loader.render_to_string("plugins/export.html", context=get_context_dict(context)))
