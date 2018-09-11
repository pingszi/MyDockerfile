from django.db import connection, transaction

from common.apps import logger


class BaseCommonDao:
    """
    @desc ：基础的sql工具类
    @author Pings
    @date   2018/03/29
    @Version  V1.0
    """

    def connect(self, func, trans=False):
        """
        @desc ：获取连接，执行增删改查动作
        @author Pings
        @date   2018/03/29
        @param  func    执行增删改查动作
        @param  trans   事务
        @return func的返回类型
        """
        cursor = None
        try:
            # **创建游标对象
            cursor = connection.cursor()
            if trans:
                with transaction.atomic():
                    rst = func(cursor)
            else:
                rst = func(cursor)
            return rst
        except:
            logger.error("执行sql错误......")
            raise               # **抛出异常
        finally:
            cursor.close()      # **关闭游标

    def findone(self, sql, args=None) -> dict:
        """
        @desc ： 查询单个数据
        @author Pings
        @date   2018/03/29
        @param  sql     sql语句
        @param  args  参数
        @return dict
        """
        return self.connect(lambda cursor: dict(zip([col[0] for col in cursor.description],
                                                    cursor.fetchone())) if cursor.execute(sql, args) > 0 else {})

    def findoneastuple(self, sql, args=None) -> tuple:
        """
        @desc ： 查询单个数据
        @author Pings
        @date   2018/03/29
        @param  sql     sql语句
        @param  args  参数
        @return tuple
        """
        return self.connect(lambda cursor: cursor.fetchone() if cursor.execute(sql, args) > 0 else ())

    def findall(self, sql, args=None) -> list:
        """
        @desc ： 查询多个数据
        @author Pings
        @date   2018/03/29
        @param  sql     sql语句
        @param  args  参数
        @return list<dict>
        """
        return self.connect(lambda cursor: [dict(zip([col[0] for col in cursor.description], row))
                                            for row in cursor.fetchall()] if cursor.execute(sql, args) > 0 else [])

    def findallastuple(self, sql, args=None) -> tuple:
        """
        @desc ： 查询多个数据
        @author Pings
        @date   2018/03/29
        @param  sql     sql语句
        @param  args  参数
        @return list<tuple>
        """
        return self.connect(lambda cursor: cursor.fetchall() if cursor.execute(sql, args) > 0 else ())

    def execute(self, sql, args=None) -> None:
        """
        @desc ： 执行增删改操作
        @author Pings
        @date   2018/03/29
        @param  sql     sql语句
        @param  args  参数
        @return None
        """
        self.connect(lambda cursor: cursor.execute(sql, args))

    def batchexec(self, sqls) -> None:
        """
        @desc ： 执行多个增删改操作
        @author Pings
        @date   2018/03/29
        @param  sqls   sql列表
        @return None
        """
        self.connect(lambda cursor: [cursor.execute(s) for s in sqls], True)

    def executemany(self, sql, args) -> None:
        """
        @desc ： 批量执行同一操作
        @author Pings
        @date   2018/03/29
        @param  sql   sql语句
        @param  args  参数列表
        @return None
        """
        self.connect(lambda cursor: cursor.executemany(sql, args))


class MysqlCommonDao(BaseCommonDao):
    """
    @desc ：mysql工具类
    @author Pings
    @date   2018/03/30
    @Version  V1.0
    """

    def findpage(self, sql, page=1, pagesize=20, args=None) -> dict:
        """
        @desc ： 分页查询
        @author Pings
        @date   2018/03/30
        @param  sql     sql语句
        @param  page  当前页
        @param  pagesize  每页的行数
        @param  args  参数
        @return dict
        """
        total = self.findone(self.getcountsql(sql), args)["count"]
        datalist = self.findall(self.getpagesql(sql, page, pagesize), args)

        return {"total": total, "datalist": datalist, "page": page, "pagesize": pagesize}

    @staticmethod
    def getcountsql(sql) -> str:
        """
        @desc ： 获取查询数量语句
        @author Pings
        @date   2018/03/30
        @param  sql   sql语句
        @return str
        """
        return "select count(*) as count from ({0})tmp".format(sql)

    @staticmethod
    def getpagesql(sql, page, pagesize) -> str:
        """
        @desc ： 获取查询分页语句
        @author Pings
        @date   2018/03/30
        @param  sql   sql语句
        @param  page  当前页
        @param  pagesize  每页的行数
        @return str
        """
        if page == 1:
            start = 0
        else:
            start = page * pagesize - 1

        param = "limit {0}, {1}".format(start, pagesize)

        # **sql包含limit
        if sql.find("limit ") != -1:
            rst = "select * from {0}tmp {1}".format(sql, param)
        else:
            rst = sql + ' ' + param

        return rst
