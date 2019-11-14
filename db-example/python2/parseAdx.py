# -*- coding: UTF-8 -*-

import traceback
import Common


file_path = "D:\\mexdoc\\adx_new\\"
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
    file_ = file_path + adx_file_name + "." + Common.last_hour2()
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
    date, hour = Common.formatDate(date, hour)

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

if __name__ == '__main__':
    parse_adx_log()
