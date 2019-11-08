from __future__ import print_function
import sys


print(sys.version)
sql = ('SELECT * from users limit 10')

# MySQLdb
# print('MySQLdb'.center(50, '='))
# import MySQLdb
#
# def connect_mysql(db_host="localhost", user="root",
#                    passwd="root",db="test", charset="utf8"):
#     conn = MySQLdb.connect(host=db_host, user=user, passwd=passwd, db=db, charset=charset)
#     conn.autocommit(True)
#     return conn.cursor()
#
# db1 = connect_mysql()
# db1.execute(sql)
# for row in db1:
#     print(*row)