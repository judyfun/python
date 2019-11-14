# -*- coding: UTF-8 -*-


import datetime
import traceback

import MySQLdb

host = "webdb.mobirtb.com"
user = "webadx"
pwd = "Admin@1234"
dbname = "req_res_db"

# file_path = "D:\\mexdoc\\adx_new\\"
file_path = "/data/adbin/ad_adx/log/"

def formatDate(date, hour):
    date = date.replace('-', '')
    hour = hour[:2]
    return date, hour


# 2019-11-12-18
def last_hour2():
    last = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d-%H")
    print(last)
    return last


#####################
# invalid start
#####################

invalid_file_name = "ssp_invalid.log"


def build_new_dict_plaStyle_invalid(date, hour, pla, style, reqf, trif, country):
    if (len(trif) == 0):
        return {
            pla: {
                style: {
                    'date': date,
                    'hour': hour,
                    'count': 1,
                    'reqf': {
                        reqf: 1
                    },
                    'trif': {},
                    'country': {
                        country: 1
                    }
                }
            }
        }
    else:
        # trif不为空
        return {
            pla: {
                style: {
                    'date': date,
                    'hour': hour,
                    'count': 1,
                    'reqf': {
                        reqf: 1
                    },
                    'trif': {
                        trif: 1
                    },
                    'country': {
                        country: 1
                    }
                }
            }
        }


def build_new_dict_style_invalid(date, hour, pla, style, reqf, trif, country):
    return {
        style: {
            'date': date,
            'hour': hour,
            'count': 1,
            'reqf': {
                reqf: 1
            },
            'trif': {
                trif: 1
            },
            'country': {
                country: 1
            }
        }
    }


"""
{
    'date':20191109,
    'hour': 09,
    '1003':{
        '2':{
            'reqf':{
                '86':123,
                '90': 33
            },
            'trif':{
                '11':123,
                '13':55
            },
            'country':{
                'usa':123,
                'mex':44
            }
        }
    }
}
"""


def re_build_reqf_invalid(dict_pla_style, reqf):
    dict_reqf = dict_pla_style['reqf']
    if (reqf in dict_reqf):
        # 有reqf
        dict_reqf[reqf] += 1
    else:
        # 没有reqf
        dict_reqf[reqf] = 1


# trif=11_1,13_8,17_2
def re_build_trif_invalid(dict_pla_style, trif):
    dict_reqf = dict_pla_style['trif']
    if (trif in dict_reqf):
        # 有reqf
        dict_reqf[trif] += 1
    else:
        # 没有reqf
        dict_reqf[trif] = 1


def re_build_country_invalid(dict_pla_style, country):
    dict_reqf = dict_pla_style['country']
    if (len(dict_reqf) < 10):
        if (country in dict_reqf):
            # 有reqf
            dict_reqf[country] += 1
        else:
            # 没有reqf
            dict_reqf[country] = 1
    else:
        #print("country bigger than 10")
        pass


def parse_sspinvalid_log():
    file_ = file_path + invalid_file_name + "." + last_hour2()
    dict_log = {}
    try:
        f = open(file_, 'r')
        # 按照pla的维度进行聚合
        for line in f:
            if "logt=" in line:
                # 解析字段
                date, hour, pla, style, reqf, trif, country = parse_invalid_field(line)
                # 判断 下游id
                if pla in dict_log:
                    # 在列表中
                    dict_pla = dict_log[pla]

                    # 判断 style
                    if style in dict_pla:
                        dict_pla_style = dict_pla[style]
                        dict_pla_style['count'] += 1
                        if len(reqf) > 0:
                            re_build_reqf_invalid(dict_pla_style, reqf)
                        # if len(trif) > 0:
                        #     reBuildTrif(dict_pla_style, trif)
                        if len(country) > 0:
                            re_build_country_invalid(dict_pla_style, country)



                    else:
                        # style 不在列表中, create new style
                        dict_style = build_new_dict_style_invalid(date, hour, pla, style, reqf, trif, country)
                        dict_pla.update(dict_style)

                else:
                    # 不在列表中，create new dict_pla
                    dict_pla_style = build_new_dict_plaStyle_invalid(date, hour, pla, style, reqf, trif, country)
                    dict_log.update(dict_pla_style)
                # print(line)
        print(dict_log)
        return dict_log
    except Exception, e:
        print("error: read invalid file error")
        traceback.print_exc()


def parse_invalid_field(line):
    # line = "2019-11-08 06:00:01 INFO :  logt=2 pub=118 pla=1023 app=f4dab4f875ee pos= style=2 code=2 reqf=86 trif= country=usa bud=com.bstech.reader.pdf.viewer os=2"
    # print(line)
    date, hour, post_line = line.split(" ", 2)
    date, hour = formatDate(date, hour)

    arr = post_line.split()

    pla = ""
    style = ""
    reqf = ""
    trif = ""
    country = ""

    for field in arr:
        if ("pla=" in field):
            pla = field[4:]
        elif ("style=" in field):
            if (len(field) == 6):
                style = "0"
            else:
                style = field[6:7]
        elif ("reqf=" in field):
            reqf = field[5:]
        elif ("trif=" in field):
            trif = field[5:]
        elif ("country=" in field):
            country = field[8:]

    return date, hour, pla, style, reqf, trif, country


if __name__ == '__main__':
    parse_sspinvalid_log()

"""
{
    'date':20191109,
    'hour': 09,
    '1003':{
        '2':{
            'count':32,
            'reqf':{
                '86':123,
                '90': 33
            },
            'trif':{
                '11':123,
                '13':55
            },
            'country':{
                'usa':123,
                'mex':44
            }
        }
    }
}
"""


def invalid_dict_to_list(invalid_dict):
    argList = []
    if isinstance(invalid_dict, dict):
        items = invalid_dict.items()
        for (pla, dict_style) in items:
            if isinstance(dict_style, dict):
                styleItems = dict_style.items()
                for (style, info) in styleItems:
                    argList.append(
                        (info['date'],
                         info['hour'],
                         pla,
                         style,
                         info['count'],
                         str(info['reqf']),
                         str(info['trif']),
                         str(info['country'])
                         )
                    )

    return argList


#####################
# invalid end
#####################

#################### start
adx_file_name = "adx.log"

'''
{
    'date': 20191109,
    'hour': 10,
    '1003':{
        '1':{
            'bidf': 123,
            'tobid':2323,
            'wbid':8768
        }
    }
}
'''


# 解析日志，返回字段 字典类型
def build_new_dict_pla_style_adx(date, hour, pla, style, bidf, tobid, wbid, dspWin):
    return {
        pla: {
            style: {
                'date': date,
                'hour': hour,
                'bidf': bidf,
                'tobid': tobid,
                'wbid': wbid,
                'dspWin': dspWin,
                'count': 1
            }
        }
    }


def build_new_dict_style_adx(date, hour, pla, style, bidf, tobid, wbid, dspWin):
    return {
        style: {
            'date': date,
            'hour': hour,
            'bidf': bidf,
            'tobid': tobid,
            'wbid': wbid,
            'dspWin': dspWin,
            'count': 1
        }
    }


def parse_adx_log():
    # filePath = "D:\\doc\\MEX\\adx.log"
    file_ = file_path + adx_file_name + "." + last_hour2()
    dict = {}
    try:
        f = open(file_, 'r')
        # 按照pla的维度进行聚合
        for line in f:
            if "logt=" in line:
                # 解析字段
                date, hour, pla, style, bidf, tobid, wbid, dspWin = parse_adx_field(line)

                # 判断 下游id
                if pla in dict:

                    dict_pla = dict[pla]

                    # 判断 style
                    if style in dict_pla:
                        dict_pla_style = dict_pla[style]

                        dict_pla_style['bidf'] += bidf
                        dict_pla_style['tobid'] += tobid
                        dict_pla_style['wbid'] += wbid
                        dict_pla_style['count'] += 1
                        dict_pla_style['dspWin'] += dspWin

                        # dict[pla][style].update(dict_pla_style)

                    else:
                        # create new style
                        dict_style = build_new_dict_style_adx(date, hour, pla, style, bidf, tobid, wbid, dspWin)
                        dict_pla.update(dict_style)

                else:
                    # 下游id 不在dict中
                    dict_pla_style = build_new_dict_pla_style_adx(date, hour, pla, style, bidf, tobid, wbid, dspWin)
                    dict.update(dict_pla_style)

        print(dict)
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
    date, hour = formatDate(date, hour)

    arr = post_line.split()
    pla = ""
    bidf = ""
    tobid = ""
    wbid = ""
    style = ""
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

    # 转换金额类型
    bidf, tobid, wbid = tranfor_bid_to_float(bidf, tobid, wbid)
    return date, hour, pla, style, bidf, tobid, wbid, dspWin


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


def adx_dict_to_list(dict_info):
    argList = []
    if isinstance(dict_info, dict):
        items = dict_info.items()
        for (pla, dict_style) in items:
            if isinstance(dict_style, dict):
                styleItems = dict_style.items()
                for (style, info) in styleItems:
                    argList.append(
                        (info['date'],
                         info['hour'],
                         pla,
                         style,
                         info['count'],
                         info['dspWin'],
                         round(info['bidf'], 6),
                         round(info['tobid'], 6),
                         round(info['wbid'], 6))
                    )

    return argList


###################### end


# 将日志参数转化为sql的参数
def parse_adx_log_to_db_args():
    adx_dict = parse_adx_log()
    adx_list = adx_dict_to_list(adx_dict)
    return adx_list


def parse_ssp_invalid_log_to_db_args():
    invalid_dict = parse_sspinvalid_log()
    invalid_list = invalid_dict_to_list(invalid_dict)
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
    print("ok")
