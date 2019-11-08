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


def parseAdxLog():
    filePath = "D:\\mexdoc\\adx_new\\adx.log"

    try:
        f = open(filePath, 'r')
        for line in f:
            print line
    except:
        print("error: read file error")


def parseField():
    line = "2019-11-08 06:00:02 INFO :  logt=1 tk=bf2a8ef608d91834 tmax=270 code=0 reqf=0 os=1 pla=1021 make=apple model=iphone net=2 aid= ifa=D2156FB3-2467-4461-8FCC-0BD1B22841BE mac= imei= country=usa gps=32.735700,-97.108100 reqid=2d03a8ea275d4122 comp=26 pub=116 sname= app=661033 pos=661033 bidf=0.231000 bud=1407852246 pubn= size=320_50 win= dbid= tobid= wbid= crid= adid= dsp=1008,1013,1015 style=2,2,2 sts=4,4,4 respf=1,1,1 fl=0.231000,0.231000,0.231000 vbid=,, pkg=,, adomain=,, dname="
    date, hour, post_line = line.split(" ", 2)

    print(date,hour)

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

    print(pla, bidf, tobid, wbid)
    return date,hour,pla,bidf,tobid,wbid


if __name__ == '__main__':
    #selectData()
    parseField()
