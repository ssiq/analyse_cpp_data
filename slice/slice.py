from util.constant import OperatorType as OperatorType
import re
import datetime


def filter_build(data):
    """
    filter build data by build action. [build,next_build)
    :param data: a dictlist of data
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


def filter_build_with_point(data):
    """
    filter build data by build action with left and right build action. [build, next_build]
    :param data: a dictlist of data
    :return: a list consist of build operation list. Each operation is a dict.
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
                pick.append(data[i].copy())
                res.append(pick)
            pick = []
        if inpick:
            act = data[i].copy()
            pick.append(act)
    return res


def filter_build_with_more_time(data, freq=5):
    """
    filter build data by build action. It will filter actions before build start of after build end in freq minute.
    :param data: a dictlist of data
    :param freq: action which freq minute before build action or after build action
    :return: a list with build slice info with actions.
    """
    if freq<0:
        freq = 5

    filter_list = []
    build1 = None
    build_action = None
    build2 = None

    pick_id = ""
    pick_project = ""

    for item in data:
        if item[OperatorType.NAME] == OperatorType.BUILD and pick_id == item['buildid'] and pick_project == item['projectname']:
            continue
        if item[OperatorType.NAME] == OperatorType.BUILD:
            build1 = build2
            build2 = item['time']
            if build1 is not None and build2 is not None:
                filter_action = {}
                filter_action['buildid'] = pick_id
                filter_action['projectname'] = pick_project
                filter_action['buildstart'] = build1
                filter_action['buildend'] = build2
                filter_action['buildstartaction'] = build_action.copy()
                filter_action['buildendaction'] = item.copy()
                filter_action['start'] = build1 - datetime.timedelta(minutes=freq)
                filter_action['end'] = build2 + datetime.timedelta(minutes=freq)
                filter_action['actions'] = []
                filter_list.append(filter_action)

            build_action = item
            pick_id = item['buildid']
            pick_project = item['projectname']

    for item in data:
        time = item['time']
        for info in filter_list:
            if info['start'] <= time <= info['end']:
                info['actions'].append(item.copy())

    return filter_list


def filter_build_testcase(data):
    """
    filter build data by build action which before a testcase action.
    :param data:
    :return:
    """
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

