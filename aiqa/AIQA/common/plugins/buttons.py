"""xadmin按钮插件"""

from django.forms import Media
from django.template import loader
from xadmin.views import BaseAdminPlugin
from xadmin.plugins.utils import get_context_dict


class CustomButtonPlugin(BaseAdminPlugin):
    """
    @desc ：自定义按钮
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """

    # **示例：custom_button = {"value": "初始化权重", "url": "init_weighted_value"}
    custom_button = {}

    """
    @desc ： 根据'custom_button'属性值设置是否加载本插件
    @author Pings
    @date   2018/04/19
    @param  media  包含其他插件的js,css文件
    @return bool
    """
    def init_request(self, *args, **kwargs):
        return bool(self.custom_button)

    """
    @desc ： 拦截返回Media的方法，加入xadmin.plugin.button.js文件
    @author Pings
    @date   2018/04/19
    @param  media  包含其他插件的js,css文件
    @return Media
    """
    def get_media(self, media):
        media = media + Media(js=["/static/plugins/js/xadmin.plugin.button.js"])
        return media

    """
    @desc ： 在top_toolbar插入点(view_block)插入按钮
    @author Pings
    @date   2018/04/19
    @param  context  TemplateContext
    @param  nodes    包含其他插件的返回内容
    @return 可以直接返回HTML，也可将内容加入到nodes参数中
    """
    def block_top_toolbar(self, context, nodes):
        # **设置页面接收的参数
        context.update({"url": self.custom_button["url"], "value": self.custom_button["value"]})

        # **把页面内容添加到nodes中
        nodes.append(loader.render_to_string("plugins/button.html", context=get_context_dict(context)))
