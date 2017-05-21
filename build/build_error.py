from build.error_util import deal_error as deal_error
from util.constant import OperatorType


def output_error_info(data):
    err_list = []
    build_count = 0
    for item in data:
        if item[OperatorType.NAME] == OperatorType.BUILD:
            build_count += 1
            build_info = {}
            build_info['time'] = item['time']
            build_info['id'] = build_count
            build_info['projectname'] = item['projectname']
            errs = deal_error(item['buildlogcontent'])
            build_info['errors'] = errs
            err_list.append(build_info)
    return err_list

