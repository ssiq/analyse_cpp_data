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
