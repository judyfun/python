# -*- coding: UTF-8 -*-
import datetime
import sys


def os_file_path():
    file_path = ""
    if "win" in sys.platform:
        file_path = "D:\\mexdoc\\adx_new\\"
    else:
        file_path = "/data/adbin/ad_adx/log/"

    return file_path


def formatDate(date, hour):
    date = date.replace('-', '')
    hour = hour[:2]
    return date, hour


# 2019-11-12-18
def last_hour2():
    last = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d-%H")
    return last
