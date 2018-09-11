import xadmin

from .views import *


# **注册AdminView
# **版本信息
xadmin.site.register_view('datastatistics/version/index', VersionInfoAdminView, name='versionindex')
# **访问量统计
xadmin.site.register_view('datastatistics/visitorvolume/index', VisitorVolumeAdminView, name='visitorvolumeindex')
# **知识量统计
xadmin.site.register_view('datastatistics/knowledgeqty/index', KnowledgeQtyAdminView, name='knowledgeqtyindex')
# **解决率统计
xadmin.site.register_view('datastatistics/solverate/index', SolveRateAdminView, name='solverateindex')
