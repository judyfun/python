# UTF-8
# ==================================================================
# WEST_WORLD MYSQL类
# ==================================================================
# Copyright (c) 2018 http://www.818seo.net All rights reserved.
# ==================================================================
# Author: JESSE
# Contact: 818seo@gmail.com
# ==================================================================
# 示例
# t = Db('table',{'prefix':'your_prefix','host':'your_host','port':'your_port','user':'your_user','password':'your_password','database':'your_database'})
# 增
# addLastRowId = t.add({'age':1,'name':'JESSE'})
# addRows = t.addAll([{'age':1,'name':'JESSE'},{'age':2,'name':'JESSE2'}])
# 删
# deleteRow = t.delete({'id':1})
# 改
# changeRow = t.save({'id':1,'name':'JESSE'})
# 查
# dataRows = t.select(where='id>1',field='id,name',limit='2,3',order='id DESC')
# dataRow = t.find(where='id=1',field='id,name')
# fieldValue = t.getField(field='name',where="id = 1")
# 链式混查
# result = t.table('west_zy',True).limit(1).where('id < 100').order('id DESC').field('name').select(where="id>10")
# 执行SQL
# reslut = t.query("SELECT * FROM west_zy")
# 查看SQL
# sql = t.getsql()
# t.getsql().select(where="id>10")


import pymysql
import traceback


# 我的配置信息
# import config

class Db():
    db = None
    sql = ''
    is_getsql = False
    master_key = 'id'
    sql_prefix = None
    sql_table = None
    # 以下参数用完赋默认值
    sql_where = ''
    sql_limit = '0,1000'
    sql_field = '*'
    sql_order = None

    def __init__(self, table=None, prefix=None, host=None, port=None, user=None, password=None, database=None,
                 connent={}):
        try:
            # 引入配置信息
            # if not connent:
            #     connent = config.get('mysql')
            #     self.sql_prefix = connent['prefix']
            self.db = pymysql.connect(
                host=host if host else connent['host'],
                port=int(port) if port else int(connent['port']),
                user=user if user else connent['user'],
                password=password if password else connent['password'],
                database=database if database else connent['database'],
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('ERROR: MYSQL数据库连接失败!')
            traceback.print_exc()
            exit()
        if prefix:
            self.sql_prefix = prefix
        if table:
            self.sql_table = self.sql_prefix + table

    def __del__(self):
        if self.db:
            self.db.close()

    def query(self, sql):
        # 测试连接是否断开并重连
        # self.db.ping(reconnect=True)
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e

    def exec(self, sql, lastrowid=False):
        cur = self.db.cursor()
        try:
            result = cur.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        if lastrowid:
            return cur.lastrowid
        return result

    def make_select(self):
        self.sql = "SELECT %s FROM `%s` " % (self.sql_field, self.sql_table)
        self.sql_field = '*'
        if self.sql_where:
            self.sql += 'WHERE %s ' % self.sql_where
            self.sql_where = ''
        if self.sql_order:
            self.sql += 'ORDER BY %s ' % self.sql_order
            self.sql_order = None
        if self.sql_limit:
            self.sql += 'LIMIT %s ' % self.sql_limit
            self.sql_limit = '0,1000'
        self.getsql(is_call_in_self=True)
        return self.sql

    def make_insert(self, data, is_double=False):
        sql = 'INSERT INTO `%s` (' % self.sql_table
        # 多条数据
        if is_double and isinstance(data, list):
            sql_value = ''
            sql += '`%s`,' % self.master_key
            # 循环list
            for i, row in enumerate(data):
                if not isinstance(row, dict): return None
                if self.master_key in row: row.pop(self.master_key)
                sql_row = '(NULL,'
                # 循环dict
                for key in row:
                    if i == 0: sql += '`%s`,' % key
                    sql_row += "'%s'," % row[key]
                sql_value += sql_row.strip(',') + '),'
            sql = sql.strip(',') + ') VALUES ' + sql_value.strip(',') + ';'
        # 单条数据
        elif isinstance(data, dict):
            sql_value = '('
            if self.master_key in data and data[self.master_key]:
                sql += '`%s`,' % self.master_key
                sql_value += '%s,' % data[self.master_key]
                data.pop(self.master_key)
            else:
                sql += '`%s`,' % self.master_key
                sql_value += 'NULL, '

            for key in data:
                sql += '`%s`,' % key
                sql_value += "'%s'," % data[key]
            sql = sql.strip(',') + ') VALUES ' + sql_value.strip(',') + ');'
        else:
            print('make_insert 传参错误：单条字典，多条数组')
            return None
        self.sql = sql
        # 显示SQL
        self.getsql(is_call_in_self=True)
        return self.sql

    def where(self, where):
        if isinstance(where, str):
            self.sql_where += ' %s ' % where
            return self
        elif isinstance(where, dict):
            for i, key in enumerate(where):
                if i == 0:
                    self.sql_where += " `%s`='%s' " % (key, where[key])
                else:
                    self.sql_where += " AND `%s`='%s' " % (key, where[key])
        return self

    def table(self, table_name, master_key=None, is_full_name=False):
        if table_name:
            self.sql_table = table_name if is_full_name else self.sql_prefix + table_name
        if master_key:
            self.master_key = master_key
        return self

    def limit(self, limit):
        if limit:
            self.sql_limit = limit
        return self

    def field(self, field):
        if field:
            self.sql_field = field
        return self

    def order(self, order):
        if order:
            self.sql_order = order
        return self

    def getsql(self, is_call_in_self=False):
        # 句中调用输出
        if is_call_in_self:
            if self.is_getsql:
                self.is_getsql = False
                print(self.sql)
                return None
        else:
            # 句尾调用返回SQL
            if self.sql != '':
                return self.sql
            # 句中调用打印SQL后执行
            else:
                self.is_getsql = True
                return self

    def select(self, where=None, field=None, limit=None, order=None):
        if field:
            self.field(field)
        if limit:
            self.limit(limit)
        if order:
            self.order(order)
        if where:
            self.where(where)
        sql = self.make_select()
        return self.query(sql)

    def find(self, where=None, field=None):
        self.limit(1)
        if field:
            self.field(field)
        if where:
            self.where(where)
        sql = self.make_select()
        data = self.query(sql)
        if len(data):
            return data[0]
        return None

    def getField(self, field=None, where=None):
        data = self.find(where, field)
        if data:
            return data[field]
        return None

    def add(self, data):
        sql = self.make_insert(data)
        return self.
        exec (sql, lastrowid=True)

    def addAll(self, data):
        sql = self.make_insert(data, is_double=True)
        return self.
        exec (sql)

    def save(self, data, where=None):
        if not isinstance(data, dict):
            print('data参数必须是dict')
            return None
        sql = 'UPDATE `%s` SET ' % self.sql_table
        # 判断条件
        if where:
            self.where(where)
            sql_where = ' WHERE' + self.sql_where
            self.sql_where = ''
        # 判断主键
        if self.master_key in data:
            self.where({'%s' % self.master_key: data[self.master_key]})
            sql_where = ' WHERE' + self.sql_where
            self.sql_where = ''
            data.pop(self.master_key)
        if not sql_where:
            print('where条件错误')
            return None
        # SET数据
        sql_set = ''
        for key in data:
            sql_set += "`%s`='%s'," % (key, data[key])
        sql = sql + sql_set.strip(',') + sql_where + ';'
        self.getsql(is_call_in_self=True)
        return self.
        exec (sql)

    def delete(self, where):
        # DELETE FROM `west_zy` WHERE (`id`='35')
        if not where:
            print('where条件错误')
            return None
        sql = 'DELETE FROM `%s`' % self.sql_table
        self.where(where)
        sql_where = ' WHERE' + self.sql_where
        self.sql_where = ''
        sql = sql + sql_where + ';'
        self.getsql(is_call_in_self=True)
        return self.
        exec (sql)


# --------------------------- 测试代码
if __name__ == '__main__':
