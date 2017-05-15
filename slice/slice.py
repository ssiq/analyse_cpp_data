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
    for i in range(len(data)):
        if data[i][OperatorType.NAME] == '9':
            if inpick == 1 and len(pick) > 0 and pick_id == data[i]['buildid'] and pick_project == data[i]['projectname']:
                continue
            inpick = 1
            pick_id = data[i]['buildid']
            pick_project = data[i]['projectname']
            if len(pick) != 0:
                res.append(pick)
            pick = []
        if inpick:
            act = data[i].copy()
            pick.append(act)
    if len(pick) != 0:
        res.append(pick)
    return res


def filter_build_testcase(data):
    i = 0
    res = []
    pick = []
    before = []
    has_testcase = 0
    pick_id = ""
    pick_project = ""
    inpick = 1
    for i in range(len(data)):
        if data[i][OperatorType.NAME] == '9':
            if inpick == 1 and len(pick) > 0 and pick_id == data[i]['buildid'] and pick_project == \
                    data[i]['projectname']:
                continue
            inpick = 1
            pick_id = data[i]['buildid']
            pick_project = data[i]['projectname']
            if len(pick) != 0:
                act = data[i].copy()
                pick.append(act)
                if has_testcase == 1:
                    if len(before) != 0:
                        res.append(before)
                    before = pick
                    has_testcase = 0
                elif has_testcase == 0:
                    before.extend(pick)
            pick = []
        elif data[i][OperatorType.NAME] == '18' and inpick:
            has_testcase = 1
            act = data[i].copy()
            pick.append(act)
        elif inpick:
            act = data[i].copy()
            pick.append(act)

    if has_testcase == 1:
        if len(before) != 0:
            res.append(before)

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
    for i in range(len(data)):
        if data[i][OperatorType.NAME] == '2' or data[i][OperatorType.NAME] == '4' or data[i][OperatorType.NAME] == '15' or data[i][OperatorType.NAME] == '17':
            inpick = 1
            if len(pick) != 0:
                res.append(pick)
            pick = []
            temp = []
            pick.append(data[i].copy())
        elif (data[i][OperatorType.NAME] == '3' or data[i][OperatorType.NAME] == '16' )and inpick:
            temp.append(data[i].copy())
            pick.extend(temp)
            temp = []
        elif inpick:
            temp.append(data[i].copy())
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
    for i in range(len(data)):
        if data[i][OperatorType.NAME] == '10' and data[i]['debug_action'] == 'start':
            inpick = 1
            if len(pick) != 0:
                res.append(pick)
            pick = []
            pick.append(data[i].copy())
        elif data[i][OperatorType.NAME] == '11' and ( data[i]['debug_action'] == 'dbgEventReasonStopDebugging' or data[i]['debug_action'] == 'dbgEventReasonEndProgram') and inpick:
            pick.append(data[i].copy())
            res.append(pick)
            pick = []
            inpick = 0
        elif inpick:
            pick.append(data[i].copy())
    return res

