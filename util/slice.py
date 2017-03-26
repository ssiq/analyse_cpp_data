from util.constant import OperatorType as OperatorType
import time

def filter_build(data):
    """
    :param data: Data Object get from xml_operation.py
    :return: a List consist of build operation list. Each operation is a Dictionary.
    """
    i = 0
    res = []
    pick = []
    inpick = 0
    for i in range(len(data.dict_list)):
        if data.dict_list[i]['operator'] == '9':
            inpick = 1
            if len(pick) != 0:
                res.append(pick)
            pick = []
        if inpick:
            act = data.dict_list[i].copy()
            pick.append(act)
    if len(pick) != 0:
        res.append(pick)
    return res


def filter_copy(data):
    """
    :param data: Data Object get from xml_operation.py
    :return: a List consist of copy/paste operation list. Each operation is a Dictionary.
    """
    i = 0
    res = []
    pick = []
    inpick = 0
    temp = []
    for i in range(len(data.dict_list)):
        if data.dict_list[i]['operator'] == '2' or data.dict_list[i]['operator'] == '4':
            inpick=1
            if len(pick) != 0:
                res.append(pick)
            pick=[]
            pick.append(data.dict_list[i].copy())
        elif data.dict_list[i]['operator'] == '3' and inpick:
            temp.append(data.dict_list[i].copy())
            pick.extend(temp)
        elif inpick:
            temp.append(data.dict_list[i].copy())
    if len(pick) != 0:
        res.append(pick)
    return res


def filter_debug(data):
    """
    :param data: Data Object get from xml_operation.py
    :return: a List consist of debug operation list. Each operation is a Dictionary.
    """
    i = 0
    res = []
    pick = []
    inpick = 0
    for i in range(len(data.dict_list)):
        if data.dict_list[i]['operator'] == '10' and data.dict_list[i]['debug_action'] == 'start':
            inpick = 1
            if len(pick) != 0:
                res.append(pick)
            pick = []
            pick.append(data.dict_list[i].copy())
        elif data.dict_list[i]['operator'] == '11' and ( data.dict_list[i]['debug_action'] == 'dbgEventReasonStopDebugging' or data.dict_list[i]['debug_action'] == 'dbgEventReasonEndProgram') and inpick:
            pick.append(data.dict_list[i].copy())
            res.append(pick)
            pick = []
            inpick = 0
        elif inpick:
            pick.append(data.dict_list[i].copy())
    return res


def count_operator(data):
    """
    :param data: one slice, a list of action
    :return: a dict about operator count in one slice
    """
    ope = OperatorType()
    res = {
        '0': 0,
        ope.TEXT_SAVE: 0,
        ope.TEXT_CUT: 0,
        ope.TEXT_PASTE: 0,
        ope.TEXT_COPY: 0,
        ope.CONTENT_INSERT: 0,
        ope.CONTENT_REPLACE: 0,
        ope.CONTENT_DELETE: 0,
        ope.CONTENT_SAVE: 0,
        ope.BUILD: 0,
        ope.DEBUG_TUN: 0,
        ope.DEBUG_BREAK: 0,
        ope.DEBUG_EXCEPTION_NOT_HANDLED: 0
    }
    for elem in data:
        res['0'] += 1
        if 'operator' in elem:
            res[elem['operator']] += 1
    return res


def stat_util(data):
    res = {'count': count_operator(data)}
    first = data[0]
    last = data[len(data)-1]
    all_time = (last['time'] - first['time']).total_seconds()
    res['time'] = round(all_time/60, 2)
    res['action_number'] = len(data)
    return res


def stat_build(data):
    res = stat_util(data)
    return res


def stat_debug(data):
    res = stat_util(data)
    return res


def stat_copy(data):
    res = stat_util(data)
    return res
