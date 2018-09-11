import re
import logging
import json

from django.http import HttpResponse

from common.apps import logger
from common.util.commondao import MysqlCommonDao
from common.util.utils import JsonEncoder

dao = MysqlCommonDao()


def findall(request):
    """
    @desc ： 根据sql查询所有数据
    @author  pings
    @date    2018/09/03
    @return  HttpResponse
    """
    fields = request.POST.get("fields")
    table = request.POST.get("table")
    where = request.POST.get("where")
    group = request.POST.get("group")
    order = request.POST.get("order")
    limit = request.POST.get("limit")
    sql = SqlEntity(fields, table, where, group, order, limit).__str__()

    return HttpResponse(json.dumps(dao.findall(sql), ensure_ascii=False, cls=JsonEncoder))


class SqlEntity(object):
    """
    @desc ：  sql实体类
    @author   Pings
    @date     2018/09/03
    @Version  V1.0
    """

    def __init__(self, fields="", table="", where="", group="", order="", limit="") -> None:
        self.fields = fields
        self.table = table
        self.where = where
        self.group = group
        self.order = order
        self.limit = limit
        self._logger = logger

    def get_safe_sql(self, sql)->str:
        reg = "update |insert |delete |truncate "
        pattern = re.compile(reg)

        if pattern.match(sql):
            self._logger.error("不安全的sql: " + sql)
            sql = pattern.sub("", sql)

        return sql

    def __str__(self) -> str:
        sql = "select {0}".format(self.fields)

        sql = sql + " from " + self.table if self.table else sql
        sql = sql + " where " + self.where if self.where else sql
        sql = sql + " group by " + self.group if self.group else sql
        sql = sql + " order by " + self.order if self.order else sql
        sql = sql + " limit " + self.limit if self.limit else sql

        return self.get_safe_sql(sql)
