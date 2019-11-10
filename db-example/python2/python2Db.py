# -*- coding: UTF-8 -*-

import MySQLdb

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


def insertToDb():
    date, hour, pla, bidf, tobid, wbid = parseField()
    print(date, hour, pla, bidf, tobid, wbid)


'''
{
    'date': 20191109,
    'hour': 10,
    '1003':{
        'bidf': 123,
        'tobid':2323,
        'wbid':8768
    }
}
'''


def parseAdxLog():
    filePath = "D:\\doc\\MEX\\adx.log"
    dict = {}
    try:
        f = open(filePath, 'r')
        # 按照pla的维度进行聚合
        for line in f:
            date, hour, pla, bidf, tobid, wbid = parseField(line)
            if (pla in dict):
                dict_pla = dict[pla]
                bidf, tobid, wbid = tranforBidToFloat(bidf, tobid, wbid)
                dict_pla['bidf'] += bidf
                dict_pla['tobid'] += tobid
                dict_pla['wbid'] += wbid
                dict_pla['count'] += 1

                dict.update(dict_pla)

            else:
                bidf, tobid, wbid = tranforBidToFloat(bidf, tobid, wbid)
                dict_pla = {pla: {'date': date, 'hour': hour, 'bidf': bidf, 'tobid': tobid, 'wbid': wbid, 'count': 1}}
                dict.update(dict_pla)

        print  dict

    except:
        print("error: read file error")

    finally:
        f.close()


def tranforBidToFloat(bidf, tobid, wbid):
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


def parseField(line):
    # line = "2019-11-08 06:00:00 INFO :  logt=1 tk=738f3bd56df90c55 tmax=420 code=0 reqf=0 os=1 pla=1003 make=apple model=iphone net=2 aid= ifa=24b52f77-5d26-4a27-8aa4-baa34cf61aa3 mac= imei= country=usa gps=40.102700,-111.644900 reqid=511-c5be30172a709b8-795 comp=13 pub=103 sname= app=1037_341232718 pos=204274c6165ee15c3d7f044d70695e93 bidf=0.220600 bud=341232718 pubn= size=300_250 win=1003 dbid=0.245028 tobid=0.220600 wbid=0.245817 crid=115C4TI2369_123669 adid= dsp=1000,1003 style=2,2 sts=4,1 respf=1,0 fl=0.242660,0.242660 vbid=,0.245817 pkg=, adomain=,internetalerts.org;urbanoutfitters.com dname="
    date, hour, post_line = line.split(" ", 2)

    arr = post_line.split()
    pla = ""
    bidf = ""
    tobid = ""
    wbid = ""
    for li in arr:
        if ("pla=" in li):
            pla = li[4:]
        elif ("bidf=" in li):
            bidf = li[5:]
        elif ("tobid=" in li):
            tobid = li[6:]
        elif ("wbid=" in li):
            wbid = li[5:]

    return date, hour, pla, bidf, tobid, wbid


if __name__ == '__main__':
    # selectData()
    # parseField()
    # insertToDb()
    parseAdxLog()
