from django.db import models
from DjangoUeditor.models import UEditorField

class TaxKnowledge(models.Model):
    """
    @desc ：知识
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    counter = models.PositiveIntegerField(default=0, verbose_name="点击数")
    sd_question = models.CharField(max_length=1000, verbose_name="问题")
    sd_answer = UEditorField(verbose_name="答案", height=300, width=600, max_length=4000,
                             settings={"toolbars": [['source', '|', 'undo', 'redo', '|',
                             'bold', 'italic', 'underline', 'formatmatch', 
                             'autotypeset', '|', 'forecolor', 'backcolor']],
                             'maximumWords': 4000})

    # **v1.4
    class_tag = models.CharField(verbose_name="分类标签", max_length=100, null=True, blank=True)

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    class Meta:
        db_table = 'tax_knowledge'
        # **菜单名
        verbose_name = "知识"
        verbose_name_plural = "知识"

    def __str__(self):
        return self.sd_question

    def question_qty(self) -> int:
        """
        @desc ： 获取扩展问题数量
        @author Pings
        @date   2018/04/19
        @return int
        """
        return self.extend_question.count()
    # **扩展问题数量显示标题
    question_qty.short_description = "扩展问题数量"


class TaxExtendQuestionHeader(models.Model):
    """
    @desc ：扩展问题
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    knowledge = models.ForeignKey(TaxKnowledge, related_name="extend_question", on_delete=models.CASCADE,
                                  verbose_name="知识")
    desc = models.CharField(max_length=255, verbose_name="描述")

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    class Meta:
        db_table = 'tax_extend_question_header'
        # **菜单名
        verbose_name = "扩展问题"
        verbose_name_plural = "扩展问题"

    def __str__(self):
        return self.desc


class TaxExtendQuestion(models.Model):
    """
    @desc ：扩展问题明细
    @author Pings
    @date   2018/04/17
    @Version  V1.0
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    extend_question = models.ForeignKey(TaxExtendQuestionHeader, on_delete=models.CASCADE, verbose_name="扩展问题")
    keyword = models.CharField(max_length=50, verbose_name="关键字")
    tf_value = models.DecimalField(default=0, max_digits=10, decimal_places=6, verbose_name="tf")
    idf_value = models.DecimalField(default=0, max_digits=10, decimal_places=6, verbose_name="idf")
    weighted_value = models.DecimalField(default=0, max_digits=10, decimal_places=6, verbose_name="权重")
    amplification = models.DecimalField(default=1, max_digits=10, decimal_places=2, verbose_name="放大倍数")

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    class Meta:
        db_table = 'tax_extend_question'
        # **菜单名
        verbose_name = "扩展问题明细"
        verbose_name_plural = "扩展问题明细"

    def __str__(self):
        return self.keyword.__str__()


class TaxSolveUnSolve(models.Model):
    """
    @desc ：会话明细
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    question = models.CharField(max_length=1000, verbose_name="问题")
    solve = models.PositiveIntegerField(default=0, verbose_name="解决/未解决")
    is_knowledge = models.BooleanField(default=False, verbose_name="是否知识")

    # **V1.3添加
    session_key = models.ForeignKey("TaxQuestionSession", to_field="session_key", db_column="session_key", 
                                    on_delete=models.CASCADE, verbose_name="标识符")
    answer = models.TextField(verbose_name="答案(小穗)", null=True, blank=True)

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    class Meta:
        db_table = 'tax_solve_unsolve'
        # **菜单名
        verbose_name = "会话明细"
        verbose_name_plural = "会话明细"


class TaxKnowledgeProxy(TaxKnowledge):
    """
    @desc ：专家调整,代理知识
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """
    class Meta:
        proxy = True
        # **菜单名
        verbose_name = "专家调整"
        verbose_name_plural = "专家调整"


class TaxQuestionSession(models.Model):
    """
    @desc ：  问答会话
    @author   Pings
    @date     2018/07/04
    @Version  V1.3
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    session_key = models.CharField(max_length=50, unique=True, verbose_name="标识符")
    source = models.CharField(max_length=10, verbose_name="来源")
    # **A.待接入，B.已接入，C.已完成，D.已过期
    status = models.CharField(max_length=1, verbose_name="状态")

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    class Meta:
        db_table = 'tax_question_session'
        # **菜单名
        verbose_name = "问答会话"
        verbose_name_plural = "人工审核"


class TaxExtendQuestionSynonym(models.Model):
    """
    @desc ：  局部同义词
    @author   Pings
    @date     2018/08/14
    @Version  V1.4
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    extend_question = models.ForeignKey(TaxExtendQuestion, on_delete=models.CASCADE, verbose_name="扩展问题明细")
    word = models.CharField(max_length=50, verbose_name="同义词")                                                     

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    class Meta:
        db_table = 'tax_extend_question_synonym'
        # **菜单名
        verbose_name = "局部同义词"
        verbose_name_plural = "局部同义词"

    def __str__(self):
        return self.word.__str__()


class TaxUnSolveMail(models.Model):
    """
    @desc ：  未解决邮件
    @author   Pings
    @date     2018/09/04
    @Version  V1.5
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    session_key = models.ForeignKey(TaxQuestionSession, to_field="session_key", db_column="session_key",
                                    on_delete=models.CASCADE, verbose_name="标识符")
    email = models.CharField(max_length=50, verbose_name="邮箱")
    content = models.TextField(verbose_name="邮件内容")
    desc = models.CharField(max_length=1000, verbose_name="描述", null=True, blank=True)

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    class Meta:
        db_table = 'tax_unsolve_mail'
        # **菜单名
        verbose_name = "未解决邮件"
        verbose_name_plural = "未解决邮件"

    def __str__(self):
        return self.email
