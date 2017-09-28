from util.constant import OperatorType
from learning.feature.lexical_analysis import get_token_list

class ContentBehaviorType:
    ADD = 1
    DELETE = 2
    MODIFY = 3

files = []

def get_file_name(path):
    folders = path.split('\\')
    return folders[len(folders) - 1]

old_item = None


def convert_token_behavior(item):
    global old_item
    if OperatorType.NAME not in item:
        return ''
    if item[OperatorType.NAME] != OperatorType.CONTENT_INSERT and item[OperatorType.NAME] != OperatorType.CONTENT_DELETE and item[OperatorType.NAME] != OperatorType.CONTENT_REPLACE:
        return ''

    print(item)

    if old_item != None and item['textto'] == old_item['textto'] and item['textfrom'] == old_item['textfrom'] and item['line'] == old_item['line'] and item['lineoffset'] == old_item['lineoffset']:
        print('skip')
        return ''

    if (item['id']%50) == 0:
        a = 1
        pass

    old_item = item
    file_name = ''
    file_content = ''

    item_name = get_file_name(item['fullpath'])

    for fi in files:
        if fi['name'] == item_name:
            file_content = fi['content']
            file_name = fi['name']

    if file_name == '':
        f = {'name': item_name, 'content': ''}
        files.append(f)
        file_content = ''
        file_name = item_name

    point_line = item['line']
    point_lineoffset = item['lineoffset']
    textfrom = item['textfrom'].replace('\r\n', '\n')
    textto = item['textto'].replace('\r\n', '\n')

    offset = 0
    linehead_offset = 0
    lines = file_content.split('\n')

    assert len(lines) >= point_line

    #print(lines[point_line-1])

    for i in range(1, point_line):
        linehead_offset += len(lines[i-1])
        linehead_offset += 1

    #print(len(lines[point_line-1]), point_lineoffset)

    assert len(lines[point_line-1]) >= point_lineoffset
    offset = linehead_offset + point_lineoffset
    offset_tail = offset + len(textfrom)

    offset_line_tail = offset_tail
    while offset_line_tail < len(file_content):
        if file_content[offset_line_tail] == '\n':
            break
        offset_line_tail += 1

    new_file_content = file_content[0:offset] + textto + file_content[offset_tail:]
    #print(new_file_content)

    for fi in files:
        if fi['name'] == file_name:
            fi['content'] = new_file_content


    offset_new_tail = offset+len(textto)
    offset_new_line_tail = offset_new_tail
    while offset_new_line_tail < len(new_file_content):
        if new_file_content[offset_new_line_tail] == '\n':
            break
        offset_new_line_tail += 1

    before_text = file_content[linehead_offset: offset_line_tail]
    after_text = new_file_content[linehead_offset:offset_new_line_tail]

    before_token = get_token_list(before_text)
    after_token = get_token_list(after_text)

    (before_token, after_token) = clear_common_tokens(before_token, after_token)

    token_change_list = get_token_behavior_list(before_token, after_token, point_lineoffset)

    return token_change_list


def get_token_behavior_list(before_token, after_token, point_offset):
    left, right = get_token_bound(before_token, 0, 0)
    token_change_list = []

    if point_offset < left or point_offset > right or len(before_token) == 0 or len(after_token) == 0:
        for to in before_token:
            to['type'] = ContentBehaviorType.DELETE
            token_change_list.append(to)
        for to in after_token:
            to['type'] = ContentBehaviorType.ADD
            token_change_list.append(to)

    if left <= point_offset <= right and len(before_token) != 0 and len(after_token) != 0:
        hasLeft = 0
        hasRight = 0

        if len(before_token) > 0 and len(after_token) > 0:
            after_token[0]['type'] = ContentBehaviorType.MODIFY
            after_token[0]['old_id'] = before_token[0]['id']
            after_token[0]['old_value'] = before_token[0]['value']
            token_change_list.append(after_token[0])
            hasLeft = 1

        if len(before_token) > 1 and len(after_token) > 1:
            after_token[-1]['type'] = ContentBehaviorType.MODIFY
            after_token[-1]['old_id'] = before_token[-1]['id']
            after_token[-1]['old_value'] = before_token[-1]['value']
            token_change_list.append(after_token[-1])
            hasRight = 1
        i = 0
        for i in range(hasLeft, len(before_token)-hasRight):
            before_token[i]['type'] = ContentBehaviorType.DELETE
            token_change_list.append(before_token[i])
        i = 0
        for i in range(hasLeft, len(after_token)-hasRight):
            after_token[i]['type'] = ContentBehaviorType.ADD
            token_change_list.append(after_token[i])

    return token_change_list


def get_token_bound(tokens, left_i, right_i):
    left = -1
    right = -1
    i = 0
    while i < len(tokens):
        if i == left_i:
            left = tokens[i]['left_offset']
        if i == right_i:
            right = tokens[i]['right_offset']
        i += 1
    return left, right


def clear_common_tokens(before_token, after_token):
    i = 0
    while i < min(len(before_token), len(after_token)):
        if before_token[i]['id'] == after_token[i]['id'] and before_token[i]['value'] == after_token[i]['value']:
            del before_token[i]
            del after_token[i]
            i -= 1
        else:
            break
        i += 1

    i = 1
    while i < (min(len(before_token), len(after_token))+1):
        if before_token[-i]['id'] == after_token[-i]['id'] and before_token[-i]['value'] == after_token[-i]['value']:
            del before_token[-i]
            del after_token[-i]
            i -= 1
        else:
            break
        i += 1
    return before_token, after_token
