# -*- coding: UTF-8 -*-

def build_new_dict_pla_invalid(date, hour, pla, style, code, bud):
    return {
        pla: {
            style: {
                code: {
                    bud: {
                        'date': date,
                        'hour': hour,
                        'count': 1
                    }
                }
            }
        }
    }


def build_new_dict_style_invalid(date, hour, style, code, bud):
    return {
        style: {
            code: {
                bud: {
                    'date': date,
                    'hour': hour,
                    'count': 1
                }
            }
        }
    }


def build_new_dict_code_invalid(date, hour, code, bud):
    return {
        code: {
            bud: {
                'date': date,
                'hour': hour,
                'count': 1
            }
        }
    }


def build_new_bud_invalid(date, hour, bud):
    return {
        bud: {
            'date': date,
            'hour': hour,
            'count': 1
        }
    }


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


def invalid_dict_to_list(invalid_dict):
    argList = []
    if isinstance(invalid_dict, dict):
        item_list = invalid_dict.items()
        for (pla, dict_style) in item_list:
            styleItems = dict_style.items()
            for (style, dict_code) in styleItems:
                codeItems = dict_code.items()
                for (code, dict_bud) in codeItems:
                    budItems = dict_bud.items()
                    for (bud, info) in budItems:
                        argList.append(
                            #date`, `hour`, `req_num`, `pla`, `style`, `scode`, `bud`
                            (info['date'],
                             info['hour'],
                             info['count'],
                             pla,
                             style,
                             code,
                             bud
                             )
                        )

    return argList
