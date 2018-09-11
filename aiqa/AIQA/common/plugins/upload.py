"""xadmin上传插件"""

from django.forms import Media
from django.template import loader
from xadmin.views import BaseAdminPlugin
from xadmin.plugins.utils import get_context_dict


class CustomUploadPlugin(BaseAdminPlugin):
    """
    @desc ：自定义上传按钮
    @author Pings
    @date   2018/07/09
    @Version  V1.0
    """

    # **custom_upload = {"value": "上传", "url": "upload_knowledge"}
    custom_upload = {}

    """
    @desc ： 根据'custom_upload'属性值设置是否加载本插件
    @author Pings
    @date   2018/07/09
    @return bool
    """
    def init_request(self, *args, **kwargs):
        return bool(self.custom_upload)

    """
    @desc ： 拦截返回Media的方法，加入xadmin.plugin.button.js文件
    @author Pings
    @date   2018/07/09
    @param  media  包含其他插件的js,css文件
    @return Media
    """
    def get_media(self, media):
        media = media + Media(js=["/static/plugins/js/xadmin.plugin.upload.js"])
        return media

    """
    @desc ： 在top_toolbar插入点(view_block)插入按钮
    @author Pings
    @date   2018/07/09
    @param  context  TemplateContext
    @param  nodes    包含其他插件的返回内容
    @return 可以直接返回HTML，也可将内容加入到nodes参数中
    """
    def block_top_toolbar(self, context, nodes):
        # **设置页面接收的参数
        context.update({"url": self.custom_upload["url"], "value": self.custom_upload.get("value", "导入")})

        # **把页面内容添加到nodes中
        nodes.append(loader.render_to_string("plugins/upload.html", context=get_context_dict(context)))
