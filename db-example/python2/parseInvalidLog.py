# -*- coding: UTF-8 -*-
import traceback

import Common as Common

file_path = "D:\\mexdoc\\adx_new\\"
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
    if (country in dict_reqf):
        # 有reqf
        dict_reqf[country] += 1
    else:
        # 没有reqf
        dict_reqf[country] = 1


def parse_sspinvalid_log():
    file_ = file_path + invalid_file_name + "." + Common.last_hour2()
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
    print(line)
    date, hour, post_line = line.split(" ", 2)
    date, hour = Common.formatDate(date, hour)

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


if __name__ == '__main__':
    parse_sspinvalid_log()
    file_ = file_path + invalid_file_name + "." + Common.last_hour2()
    print(file_)
