import util.constant as constant
from datetime import *

def move_paste_insert(data):
    res = []
    pastes = []
    inserts = []
    gap = 5
    delta = timedelta(seconds = gap)

    for item in data:
        if item[constant.OperatorType.NAME] == constant.OperatorType.TEXT_PASTE:
            pastes.append(item)

    for item in data:
        is_paste_insert = 0;
        for paste in pastes:
            if item['time'] >= (paste['time'] - delta) and item['time'] <= (paste['time'] + delta):
                if item[constant.OperatorType.NAME] == constant.OperatorType.CONTENT_INSERT or item[constant.OperatorType.NAME] == constant.OperatorType.CONTENT_REPLACE:
                    if item['textto'].strip() == paste['content'].strip():
                        is_paste_insert = 1
                        inserts.append(item)
                        break;
        if is_paste_insert == 0:
            res.append(item)

    return res


def merge_fixed_delete(data, delete_threshhold=20):
    '''
    This method is used to merge the delete insert to fix the type error.
    :param data: a dict list
    :param delete_threshhold: the delete max number
    :return: a changed dict list
    '''

    import copy
    data = copy.deepcopy(data)

    def merge_last_two(delete_threshhold, merge, moved_data, pre_delete, pre_insert):
        if len(pre_delete['textfrom']) <= len(pre_insert['textto']) \
                and len(pre_delete['textfrom']) < delete_threshhold:
            moved_data = moved_data[:-2]
            moved_data.append(merge(pre_insert, pre_delete))
        return moved_data

    def merge(insert_action, delete_action):
        print('merge {} and {}'.format(insert_action, delete_action))
        insert_action['textto'] = insert_action['tex tto'][:-len(delete_action['textfrom'])]
        return insert_action
    moved_data = []
    cached_action = []
    for item in data:
        item_type = item[constant.OperatorType.NAME]
        # print("id :{}, type:{} ".format(item['id'], item_type))
        if item_type == constant.OperatorType.CONTENT_DELETE:
            cached_action.append(item)
        elif item_type == constant.OperatorType.CONTENT_INSERT:
            if len(cached_action) >= 2:
                pre_insert = cached_action[-2]
                pre_delete = cached_action[-1]
                insert_end_position = pre_insert['lineoffset'] + len(pre_insert['textto'])
                delete_begin_position = pre_delete['lineoffset'] + len(pre_delete['textfrom'])
                # print("id {}, insert line: {}, offset {}, textto {}, offset end: {}".
                #       format(pre_insert['id'],
                #              pre_insert['line'],
                #              pre_insert['lineoffset'],
                #              pre_insert['textto'],
                #              insert_end_position))
                # print("id {}, delete line: {}, offset {}, textfrom {},  delete position {}".
                #       format(pre_delete['id'],
                #              pre_delete['line'],
                #              pre_delete['lineoffset'],
                #              pre_delete['textfrom'],
                #              delete_begin_position))
                if pre_delete[constant.OperatorType.NAME] == \
                        constant.OperatorType.CONTENT_DELETE \
                        and pre_insert[constant.OperatorType.NAME] == \
                                constant.OperatorType.CONTENT_INSERT:
                    if pre_insert['line'] == pre_delete['line'] \
                            and insert_end_position == delete_begin_position:
                        moved_data = merge_last_two(delete_threshhold, merge, moved_data, pre_delete, pre_insert)
                    elif pre_delete['line'] == pre_insert['line'] + 1 and pre_delete['lineoffset'] == 0:
                        moved_data = merge_last_two(delete_threshhold, merge, moved_data, pre_delete, pre_insert)
            cached_action.append(item)
        else:
            moved_data.extend(cached_action)
            moved_data.append(item)
            cached_action.clear()
    return moved_data
