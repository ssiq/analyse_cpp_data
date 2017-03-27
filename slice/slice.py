from util.constant import OperatorType as OperatorType
import re


def filter_build(data):
    """
    :param data: Data Object get from xml_operation.py
    :return: a List consist of build operation list. Each operation is a Dictionary.
    """
    i = 0
    res = []
    pick = []
    pick_id = ""
    pick_project = ""
    inpick = 0
    for i in range(len(data.dict_list)):
        if data.dict_list[i][OperatorType.NAME] == '9':
            if inpick == 1 and len(pick) > 0 and pick_id == data.dict_list[i]['buildid'] and pick_project == data.dict_list[i]['projectname']:
                continue
            inpick = 1
            pick_id = data.dict_list[i]['buildid']
            pick_project = data.dict_list[i]['projectname']
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
        if data.dict_list[i][OperatorType.NAME] == '2' or data.dict_list[i][OperatorType.NAME] == '4':
            inpick=1
            if len(pick) != 0:
                res.append(pick)
            pick=[]
            temp = []
            pick.append(data.dict_list[i].copy())
        elif data.dict_list[i][OperatorType.NAME] == '3' and inpick:
            temp.append(data.dict_list[i].copy())
            pick.extend(temp)
            temp = []
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
        if data.dict_list[i][OperatorType.NAME] == '10' and data.dict_list[i]['debug_action'] == 'start':
            inpick = 1
            if len(pick) != 0:
                res.append(pick)
            pick = []
            pick.append(data.dict_list[i].copy())
        elif data.dict_list[i][OperatorType.NAME] == '11' and ( data.dict_list[i]['debug_action'] == 'dbgEventReasonStopDebugging' or data.dict_list[i]['debug_action'] == 'dbgEventReasonEndProgram') and inpick:
            pick.append(data.dict_list[i].copy())
            res.append(pick)
            pick = []
            inpick = 0
        elif inpick:
            pick.append(data.dict_list[i].copy())
    return res

