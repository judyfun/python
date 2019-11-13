# -*- coding: UTF-8 -*-

import MySQLdb
import traceback

import ParseAdx
import ParseInvalidLog

host = "webdb.mobirtb.com"
user = "webadx"
pwd = "Admin@1234"
dbname = "req_res_db"


def selectData():
    db = MySQLdb.connect(host, user, pwd, dbname, charset=('utf8'))
    cursor = db.cursor()

    sql = "SELECT * FROM tab_adx"

    results = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if 0 == len(results):
            print("get empty data from table req_res_db.tab_adx")

        for i in results:
            print(i)
    except:
        print("error: unable to fetchdata from db req_res_db.tab_adx")


# 将日志参数转化为sql的参数
def parse_adx_log_to_db_args():
    adx_dict = ParseAdx.parse_adx_log()
    adx_list = ParseAdx.adx_dict_to_list(adx_dict)
    return adx_list


def parse_ssp_invalid_log_to_db_args():
    invalid_dict = ParseInvalidLog.parse_sspinvalid_log()
    invalid_list = ParseInvalidLog.invalid_dict_to_list(invalid_dict)
    return invalid_list


# 插入数据
def insert_to_db():
    insert_adx_db()
    insert_ssp_invalid_db()


def insert_adx_db():
    db = MySQLdb.connect(host, user, pwd, dbname, charset=('utf8'))
    cursor = db.cursor()

    # date, hour, pla, bidf, tobid, wbid = parseField()
    # print(date, hour, pla, bidf, tobid, wbid)

    newSql = "INSERT INTO `req_res_db`.`tab_adx` (`date`, `hour`, `pla`, `style`, `req_num`, `dsp_win`, `bidfloor`, `tobid`,`wbid`) VALUES " \
             "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    argList = parse_adx_log_to_db_args()

    try:
        cursor.executemany(newSql, argList)
        db.commit()
        print("insert %s into db success.", len(argList))

    except:
        db.rollback()
        print("error: unable to insert db req_res_db.tab_adx")
        traceback.print_exc()


def insert_ssp_invalid_db():
    db = MySQLdb.connect(host, user, pwd, dbname, charset=('utf8'))
    cursor = db.cursor()

    # date, hour, pla, bidf, tobid, wbid = parseField()
    # print(date, hour, pla, bidf, tobid, wbid)

    newSql = "INSERT INTO `req_res_db`.`tab_ssp_invalid` (`date`, `hour`, `pla`, `style`, `req_num`,  `reqf`, `trif`, `country`) VALUES " \
             "(%s,%s,%s,%s,%s,%s,%s,%s)"

    argList = parse_ssp_invalid_log_to_db_args()

    try:
        cursor.executemany(newSql, argList)
        db.commit()
        print("insert %s into tab_ssp_invalid success.", len(argList))

    except Exception, e:
        db.rollback()
        print("error: unable to insert db req_res_db.tab_ssp_invalid")
        traceback.print_exc()
    finally:
        db.close()


if __name__ == '__main__':
    insert_to_db()
