# -*- coding: UTF-8 -*-

import sys
import datetime
import traceback
import Utils
import AdxBuildHelper
import InvalidBuildHelper

import MySQLdb

host = "webdb.mobirtb.com"
user = "webadx"
pwd = "Admin@1234"
dbname = "req_res_db"

#####################
# invalid start
#####################

invalid_file_name = "ssp_invalid.log"

"""
{
    'date':20191109,
    'hour': 09,
    'pla':{
        'style':{
            'code':{
                'bud':{
                    'count': 1
                }
            }
        }
    }
}
"""


def parse_sspinvalid_log():
    file_ = Utils.os_file_path() + invalid_file_name + "." + Utils.last_hour2()
    print(file_)
    dict_log = {}
    index = 0
    try:
        f = open(file_, 'r')
        # 按照pla的维度进行聚合
        for line in f:
            index += 1
            if "logt=" in line:
                print(index, line)
                # 解析字段
                date, hour, pla, style, code, bud = parse_invalid_field(line)
                # 判断 下游id
                if pla in dict_log:
                    # 在列表中
                    dict_pla = dict_log[pla]

                    # 判断 style
                    if style in dict_pla:
                        dict_style = dict_pla[style]

                        if code in dict_style:
                            dict_code = dict_style[code]

                            if bud in dict_code:
                                dict_bud = dict_code[bud]
                                dict_bud['count'] += 1
                            else:
                                dict_bud = InvalidBuildHelper.build_new_bud_invalid(date, hour, bud)
                                dict_code.update(dict_bud)
                        else:
                            # code 不在列表中，create new code
                            dict_code = InvalidBuildHelper.build_new_dict_code_invalid(date, hour, code, bud)
                            dict_style.update(dict_code)
                    else:
                        # style 不在列表中, create new style
                        dict_style = InvalidBuildHelper.build_new_dict_style_invalid(date, hour, style, code, bud)
                        dict_pla.update(dict_style)

                else:
                    # 不在列表中，create new dict_pla
                    dict_pla_style = InvalidBuildHelper.build_new_dict_pla_invalid(date, hour, pla, style, code, bud)
                    dict_log.update(dict_pla_style)
        # print(dict_log)
        return dict_log
    except Exception, e:
        print("error: read invalid file error")
        traceback.print_exc()


def parse_invalid_field(line):
    # line = "2019-11-08 06:00:01 INFO :  logt=2 pub=118 pla=1023 app=f4dab4f875ee pos= style=2 code=2 reqf=86 trif= country=usa bud=com.bstech.reader.pdf.viewer os=2"
    # print(line)
    date, hour, post_line = line.split(" ", 2)
    date, hour = Utils.formatDate(date, hour)

    arr = post_line.split()

    pla = ""
    style = ""
    code = -1
    bud = ""

    for field in arr:
        if "pla=" in field:
            pla = field[4:]
        elif "style=" in field:
            if len(field) == 6:
                style = "0"
            else:
                style = field[6:7]
        elif "code=" in field:
            code = field[5:]
        elif "bud=" in field:
            bud = field[4:]

    return date, hour, pla, style, code, bud


#####################
# invalid end
#####################

#################### adx start
adx_file_name = "adx.log"

'''
{
    'pla':{
        'style':{
            'bud':{   
                'date': 20191109,
                'hour': 10,
                'bidf': 123,
                'tobid':2323,
                'wbid':8768,
                'count': 1
            }
        }
    }
}
'''


def parse_adx_log():
    # filePath = "D:\\doc\\MEX\\adx.log"
    file_ = Utils.os_file_path() + adx_file_name + "." + Utils.last_hour2()
    print(file_)
    dict = {}
    try:
        f = open(file_, 'r')
        # 按照pla的维度进行聚合
        for line in f:
            if "logt=" in line:
                # 解析字段
                date, hour, pla, style, bidf, tobid, wbid, dspWin, bud = parse_adx_field(line)

                # 判断 下游id
                if pla in dict:

                    dict_pla = dict[pla]

                    # 判断 style
                    if style in dict_pla:
                        dict_style = dict_pla[style]

                        if bud in dict_style:
                            dict_bud = dict_style[bud]

                            dict_bud['bidf'] += bidf
                            dict_bud['tobid'] += tobid
                            dict_bud['wbid'] += wbid
                            dict_bud['count'] += 1
                            dict_bud['dspWin'] += dspWin

                        else:
                            dict_bud = AdxBuildHelper.build_new_bud_adx(date, hour, bidf, tobid, wbid, dspWin, bud)
                            dict_style.update(dict_bud)
                    # dict[pla][style].update(dict_pla_style)

                    else:
                        # create new style
                        dict_style = AdxBuildHelper.build_new_dict_style_adx(date, hour, style, bidf, tobid, wbid,
                                                                             dspWin, bud)
                        dict_pla.update(dict_style)

                else:
                    # 下游plaid 不在dict中
                    dict_pla_style = AdxBuildHelper.build_new_dict_pla_adx(date, hour, pla, style, bidf, tobid, wbid,
                                                                           dspWin,
                                                                           bud)
                    dict.update(dict_pla_style)

        # print(dict)
        return dict

    except Exception, e:
        print("error: read adx file error")
        print(e)
        traceback.print_exc()

    finally:
        f.close()


# 按line,解析日志字段
def parse_adx_field(line):
    # line = "2019-11-08 06:00:00 INFO :  logt=1 tk=738f3bd56df90c55 tmax=420 code=0 reqf=0 os=1 pla=1003 make=apple model=iphone net=2 aid= ifa=24b52f77-5d26-4a27-8aa4-baa34cf61aa3 mac= imei= country=usa gps=40.102700,-111.644900 reqid=511-c5be30172a709b8-795 comp=13 pub=103 sname= app=1037_341232718 pos=204274c6165ee15c3d7f044d70695e93 bidf=0.220600 bud=341232718 pubn= size=300_250 win=1003 dbid=0.245028 tobid=0.220600 wbid=0.245817 crid=115C4TI2369_123669 adid= dsp=1000,1003 style=2,2 sts=4,1 respf=1,0 fl=0.242660,0.242660 vbid=,0.245817 pkg=, adomain=,internetalerts.org;urbanoutfitters.com dname="
    # print("parse line ===>", line)
    date, hour, post_line = line.split(" ", 2)
    date, hour = Utils.formatDate(date, hour)

    arr = post_line.split()
    pla = ""
    bidf = ""
    tobid = ""
    wbid = ""
    style = ""
    bud = ""
    dspWin = 0

    for field in arr:
        if ("pla=" in field):
            pla = field[4:]
        elif ("style=" in field):
            style = field[6:7]
        elif ("bidf=" in field):
            bidf = field[5:]
        elif ("tobid=" in field):
            tobid = field[6:]
        elif ("wbid=" in field):
            wbid = field[5:]
        elif ("win=" in field):
            if (len(field) > 4):
                dspWin = 1
        elif "bud=" in field:
            bud = field[4:]

    # 转换金额类型
    bidf, tobid, wbid = tranfor_bid_to_float(bidf, tobid, wbid)
    return date, hour, pla, style, bidf, tobid, wbid, dspWin, bud


# 金额字段转float，保留6位小数
def tranfor_bid_to_float(bidf, tobid, wbid):
    if (len(bidf) > 0):
        bidf = float(bidf)
    else:
        bidf = 0

    if (len(tobid)):
        tobid = float(tobid)
    else:
        tobid = 0

    if (len(wbid)):
        wbid = float(wbid)
    else:
        wbid = 0

    return bidf, tobid, wbid


###################### adx end


# 将日志参数转化为sql的参数
def parse_adx_log_to_db_args():
    adx_dict = parse_adx_log()
    adx_list = AdxBuildHelper.adx_dict_to_list(adx_dict)
    return adx_list


def parse_ssp_invalid_log_to_db_args():
    invalid_dict = parse_sspinvalid_log()
    invalid_list = InvalidBuildHelper.invalid_dict_to_list(invalid_dict)
    return invalid_list


# 插入数据
def insert_to_db():
    # insert_adx_db()
    insert_ssp_invalid_db()


def insert_adx_db():
    db = MySQLdb.connect(host, user, pwd, dbname, charset=('utf8'))
    cursor = db.cursor()

    # date, hour, pla, bidf, tobid, wbid = parseField()
    # print(date, hour, pla, bidf, tobid, wbid)

    newSql = "INSERT INTO `req_res_db`.`tab_adx_2` (`date`, `hour`, `pla`, `style`, `bud`, `req_num`, `dsp_win`, `bidfloor`, `tobid`,`wbid`) VALUES " \
             "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    argList = parse_adx_log_to_db_args()
    # print("adx arglist -> ", argList)

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
    newSql = "INSERT INTO `req_res_db`.`tab_ssp_invalid_2` (`date`, `hour`, `req_num`, `pla`, `style`, `scode`, `bud`) VALUES " \
             "(%s,%s,%s,%s,%s,%s,%s);"

    # argList = []
    # arg = ('20191108', '06', '1025', '1', '2', '1080465358', 1)
    # argList.append(arg)
    argList = parse_ssp_invalid_log_to_db_args()
    # print("invalid arglist -> ", argList)



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
    print("ok")
