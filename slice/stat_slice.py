from util.constant import OperatorType as OperatorType
import re


def count_operator(data):
    """
    :param data: one slice, a list of action
    :return: a dict about operator count in one slice
    """
    res = {
        '0': 0,
        OperatorType.TEXT_SAVE: 0,
        OperatorType.TEXT_CUT: 0,
        OperatorType.TEXT_PASTE: 0,
        OperatorType.TEXT_COPY: 0,
        OperatorType.CONTENT_INSERT: 0,
        OperatorType.CONTENT_REPLACE: 0,
        OperatorType.CONTENT_DELETE: 0,
        OperatorType.CONTENT_SAVE: 0,
        OperatorType.BUILD: 0,
        OperatorType.DEBUG_TUN: 0,
        OperatorType.DEBUG_BREAK: 0,
        OperatorType.DEBUG_EXCEPTION_NOT_HANDLED: 0,
        OperatorType.BROWSER_URL: 0,
        OperatorType.BROWSER_URL_CLOSE: 0,
        OperatorType.BROWSER_COPY: 0,
        OperatorType.BROWSER_PASTE: 0,
        OperatorType.BROWSER_CUT: 0,
        OperatorType.TEST: 0,
        OperatorType.TEXT_STARTUNDO: 0,
        OperatorType.TEXT_UNDOEND: 0,
        OperatorType.TEXT_STARTREDO: 0,
        OperatorType.TEXT_REDOEND: 0
    }
    for elem in data:
        res['0'] += 1
        if OperatorType.NAME in elem:
            res[elem[OperatorType.NAME]] += 1
    return res


def stat_util(data):
    res = {'count': count_operator(data)}
    first = data[0]
    last = data[len(data)-1]
    all_time = (last['time'] - first['time']).total_seconds()
    res['time'] = round(all_time/60, 2)
    res['action_count'] = len(data)
    return res


def stat_build(data):
    res = stat_util(data)
    res['slice_type'] = 'build'
    res['slice_id'] = data[0]['buildid']
    error_list = deal_error(data[0]['buildlogcontent'])
    result = deal_result(data[0]['buildlogcontent'])
    res['build_result'] = result
    res['error_count'] = len(error_list)
    res['error'] = error_list
    return res


def stat_build_testcase(data):
    res = stat_util(data)
    len_data = len(data)
    res['slice_type'] = 'build_testcase'
    res['slice_id'] = data[len_data-1]['buildid']
    error_list = deal_error(data[len_data-1]['buildlogcontent'])
    result = deal_result(data[len_data-1]['buildlogcontent'])
    res['build_result'] = result
    res['error_count'] = len(error_list)
    res['error'] = error_list
    return res


def stat_debug(data):
    res = stat_util(data)
    res['slice_type'] = 'debug'
    res['slice_id'] = data[0]['id']
    res['start_time'] = data[0]['time']
    return res


def stat_copy(data):
    res = stat_util(data)
    paste_count = 0
    res['slice_type'] = 'copy'
    res['paste_files'] = []
    if 'name' not in data[0]:
        data[0]['name'] = data[0]['title']
    #("content:{}|||{}".format(data[0]['name'], data[0]['content']))
    for action in data:
        if action[OperatorType.NAME] == OperatorType.TEXT_PASTE:
            paste_count += 1
            if action['name'] not in res['paste_files']:
                res['paste_files'].append(action['name'])
                #print("    paste_file:{}|||{}".format(action['name'], action['content']))
        elif action[OperatorType.NAME] == OperatorType.BROWSER_PASTE:
            paste_count += 1
            if action['title'] not in res['paste_files']:
                res['paste_files'].append(action['title'])
                #print("    paste_file:{}|{}".format(action['title'], action['content']))
    res['paste_count'] = paste_count
    res['copy_length'] = len(data[len(data)-1]['content'])
    if data[0][OperatorType.NAME] == OperatorType.TEXT_COPY or data[0][OperatorType.NAME] == OperatorType.TEXT_CUT:
        res['copy_file'] = data[0]['name']
    elif data[0][OperatorType.NAME] == OperatorType.BROWSER_COPY or data[0][OperatorType.NAME] == OperatorType.BROWSER_CUT:
        res['copy_file'] = data[0]['title']
    res['slice_id'] = data[0]['time']
    res['content'] = data[len(data)-1]['content']
    #print("paste_files:{}".format(res['paste_files']))
    return res


def deal_error(content):
    res = []
    lines=content.split("\n")
    for temp in lines:
        temp=temp.strip()
        temps=temp.split(">")
        if len(temps)>1:
            line=temp[2:]
        else:
            line=temp
        pattern=re.compile(r"^(.*): (fatal |)error (\w*): (.*)$")
        match=pattern.search(line)
        if match:
            position=match.group(1)
            code=match.group(3)
            message=match.group(4)
            err = {'position': position, 'error_code': code, 'error_message': message}
            res.append(err)
    return res


def deal_result(content):
    lines=content.split("\n")
    for temp in lines:
        temp=temp.strip()
        temps=temp.split(">")
        if len(temps)>1:
            line=temp[2:]
        else:
            line=temp
        pattern = re.compile(r"^(Build succeeded|生成成功).*")
        match = pattern.search(line)
        if match:
            return 1
        pattern = re.compile(r"^(Build FAILED|生成失败).*")
        match = pattern.search(line)
        if match:
            return 0
    return 0


def stat(data, types):
    res = []
    one = {}
    for item in data:
        if types == "build":
            one = stat_build(item)
        elif types == "copy":
            one = stat_copy(item)
        elif types == "debug":
            one = stat_debug(item)
        elif types == "build_testcase":
            one = stat_build_testcase(item)
        res.append(one)
    return res
