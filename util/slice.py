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
        if data.dict_list[i]['operator'] == '10' and data.dict_list[i]['action'] == 'start':
            inpick = 1
            if len(pick) != 0:
                res.append(pick)
            pick = []
            pick.append(data.dict_list[i].copy())
        elif data.dict_list[i]['operator'] == '11' and ( data.dict_list[i]['action'] == 'dbgEventReasonStopDebugging' or data.dict_list[i]['action'] == 'dbgEventReasonEndProgram') and inpick:
            pick.append(data.dict_list[i].copy())
            res.append(pick)
            pick = []
            inpick = 0
        elif inpick:
            pick.append(data.dict_list[i].copy())
    return res

