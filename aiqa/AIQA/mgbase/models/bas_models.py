from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver


class TaxBasData(models.Model):
    """
    @desc ：基础数据
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """

    class Meta:
        # **表名
        db_table = "tax_bas_data"
        # **菜单名
        verbose_name = "基础数据"
        verbose_name_plural = "基础数据"

    id = models.AutoField(primary_key=True, verbose_name="编号")
    code = models.CharField(max_length=20, unique=True, verbose_name="编码")
    name = models.CharField(max_length=100, verbose_name="名称")
    value = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="值")
    sort = models.IntegerField(null=True, blank=True, verbose_name="排序")
    desc = models.CharField(null=True, blank=True, max_length=255, verbose_name="描述")
    type = models.CharField(max_length=20, verbose_name="类型")
    type_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="类型描述")

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    CACHE_KEY = "bas_data_"

    @staticmethod
    @receiver([post_save, post_delete], sender="mgbase.TaxBasData")
    def update_cache(sender, **kwargs) -> None:
        """
        @desc ： 监听修改和删除事件，更新缓存
        @author Pings
        @date   2018/05/14
        """
        for bas_data in TaxBasData.objects.all():
            cache.set(TaxBasData.CACHE_KEY + bas_data.code, bas_data)

        from common.algorithm.keyword_weighted import BaseModelMatchedAnswer
        BaseModelMatchedAnswer.delete_all_cache()

    @staticmethod
    def get(code):
        """
        @desc ： 获取缓存中的数据
        @author Pings
        @date   2018/05/14
        @param  code 基础数据编码
        @return TaxBasData
        """
        key = TaxBasData.CACHE_KEY + code
        rst = cache.get(key)

        if not rst:
            rst = TaxBasData.objects.get(code=code)
            cache.set(key, rst)

        return rst

    @staticmethod
    def set(code, value):
        """
        @desc ：设置缓存中的数据
        @author Pings
        @date   2018/07/19
        @param  code 基础数据编码
        @return TaxBasData
        """
        key = TaxBasData.CACHE_KEY + code
        bas_data = TaxBasData.objects.get(code=code)
        bas_data.value = value
        bas_data.save()
        cache.set(key, bas_data)

        return bas_data

    def __str__(self):
        return self.name


class TaxBasStopWord(models.Model):
    """
    @desc ：停用词
    @author Pings
    @date   2018/04/11
    @Version  V1.0
    """

    class Meta:
        # **表名
        db_table = "tax_bas_stopword"
        # **菜单名
        verbose_name = "停用词"
        verbose_name_plural = "停用词"

    id = models.AutoField(primary_key=True, verbose_name="编号")
    word = models.CharField(max_length=50, unique=True, verbose_name="停用词")

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    CACHE_KEY_ALL = "cache_key_stopword_all"

    @staticmethod
    @receiver([post_save, post_delete], sender="mgbase.TaxBasStopWord")
    def update_cache(sender, **kwargs) -> None:
        """
        @desc ： 监听修改和删除事件，更新缓存
        @author Pings
        @date   2018/05/14
        """
        rst = tuple(key.word for key in TaxBasStopWord.objects.all())
        cache.set(TaxBasStopWord.CACHE_KEY_ALL, rst)

    @staticmethod
    def list_all() -> tuple:
        """
        @desc ： 获取所有缓存中的数据
        @author Pings
        @date   2018/05/14
        @return tuple<string>
        """
        rst = cache.get(TaxBasStopWord.CACHE_KEY_ALL)

        if not rst:
            rst = tuple(key.word for key in TaxBasStopWord.objects.all())
            cache.set(TaxBasStopWord.CACHE_KEY_ALL, rst)

        return rst

    def __str__(self):
        return self.word


class TaxBasKeyword(models.Model):
    """
    @desc ：关键字
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """

    class Meta:
        # **表名
        db_table = "tax_bas_keyword"
        # **菜单名
        verbose_name = "关键字"
        verbose_name_plural = "关键字"

    id = models.AutoField(primary_key=True, verbose_name="编号")
    keyword = models.CharField(max_length=50, unique=True, verbose_name="关键字")
    amplification = models.DecimalField(default=1, max_digits=10, decimal_places=2, verbose_name="全局放大倍数")

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    CACHE_KEY_ALL = "cache_key_keyword_all"

    @staticmethod
    @receiver([post_save, post_delete], sender="mgbase.TaxBasKeyword")
    def update_cache(sender, **kwargs) -> None:
        """
        @desc ： 监听修改和删除事件，更新缓存
        @author Pings
        @date   2018/05/14
        """
        rst = tuple(key.keyword for key in TaxBasKeyword.objects.all())
        cache.set(TaxBasKeyword.CACHE_KEY_ALL, rst)

    @staticmethod
    def list_all() -> tuple:
        """
        @desc ： 获取所有缓存中的数据
        @author Pings
        @date   2018/05/14
        @return tuple<string>
        """
        rst = cache.get(TaxBasKeyword.CACHE_KEY_ALL)

        if not rst:
            rst = tuple(key.keyword for key in TaxBasKeyword.objects.all())
            cache.set(TaxBasKeyword.CACHE_KEY_ALL, rst)

        return rst

    def __str__(self):
        return self.keyword


class TaxBasSynonym(models.Model):
    """
    @desc ：同义词
    @author Pings
    @date   2018/04/16
    @Version  V1.0
    """

    class Meta:
        # **表名
        db_table = "tax_bas_synonym"
        # **菜单名
        verbose_name = "同义词"
        verbose_name_plural = "同义词"

    id = models.AutoField(primary_key=True, verbose_name="编号")
    keyword = models.ForeignKey(TaxBasKeyword, to_field="keyword",
                                db_column="keyword", on_delete=models.CASCADE,
                                verbose_name="关键字", related_name="synonym")
    word = models.CharField(max_length=50, unique=True, verbose_name="同义词")

    add_who = models.IntegerField(verbose_name="添加人", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    edit_who = models.IntegerField(verbose_name="编辑人", blank=True, null=True)
    edit_time = models.DateTimeField(verbose_name="编辑时间", auto_now=True)

    def __str__(self):
        return self.word
