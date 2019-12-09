# -*- coding: UTF-8 -*-

# 解析日志，返回字段 字典类型
def build_new_dict_pla_adx(date, hour, pla, style, bidf, tobid, wbid, dspWin, bud):
    return {
        pla: {
            style: {
                bud: {
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
    }


def build_new_dict_style_adx(date, hour, style, bidf, tobid, wbid, dspWin, bud):
    return {
        style: {
            bud: {
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


def build_new_bud_adx(date, hour, bidf, tobid, wbid, dspWin, bud):
    return {
        bud: {
            'date': date,
            'hour': hour,
            'bidf': bidf,
            'tobid': tobid,
            'wbid': wbid,
            'dspWin': dspWin,
            'count': 1
        }
    }


def adx_dict_to_list(dict_info):
    argList = []
    if isinstance(dict_info, dict):
        item_list = dict_info.items()
        for (pla, dict_style) in item_list:
            if isinstance(dict_style, dict):
                style_items = dict_style.items()
                for (style, dict_bud) in style_items:
                    if isinstance(dict_bud, dict):
                        bud_items = dict_bud.items()
                        for (bud, info) in bud_items:
                            argList.append(
                                (info['date'],
                                 info['hour'],
                                 pla,
                                 style,
                                 bud,
                                 info['count'],
                                 info['dspWin'],
                                 round(info['bidf'], 6),
                                 round(info['tobid'], 6),
                                 round(info['wbid'], 6))
                            )

    return argList

