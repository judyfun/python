# -*- coding: UTF-8 -*-
import datetime


def formatDate(date, hour):
    date = date.replace('-', '')
    hour = hour[:2]
    return date, hour


# 2019-11-12-18
def last_hour2():
    last = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d-%H")
    print(last)
    return last


def last_hour():
    hour = datetime.datetime.now().hour
    last_hour = (datetime.datetime.now() - datetime.timedelta(minutes=60)).hour

    print(last_hour)


if __name__ == '__main__':
    last_hour2()
