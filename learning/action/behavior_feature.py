import re
import numpy as np
from learning.action.data_extractor import extract_score
from slice.stat_slice import deal_result


class ActionType:

    COUNT = 22

    TEXT_SAVE = 1
    TEXT_CUT = 2
    TEXT_PASTE = 3
    TEXT_COPY = 4
    CONTENT_INSERT = 5
    CONTENT_INSERT_CONDITION = 6
    CONTENT_INSERT_LOOP = 7
    CONTENT_REPLACE = 8
    CONTENT_DELETE = 9
    BUILD_SUCCESS = 10
    BUILD_FAILED = 11
    DEBUG_RUN = 12
    DEBUG_BREAK = 13
    DEBUG_EXCEPTION_NOT_HANDLED = 14
    BROWSER_URL = 15
    BROWSER_URL_CLOSE = 16
    BROWSER_COPY = 17
    BROWSER_PASTE = 18
    BROWSER_CUT = 19
    TEST = 20
    TEXT_UNDO = 21
    TEXT_REDO = 22

    @staticmethod
    def name_to_feature(name):
        '''
        Get the vector form about the action name
        :param name: action name
        :return: vector
        '''
        res = {
            'text_save': ActionType.TEXT_SAVE,
            'text_cut': ActionType.TEXT_CUT,
            'text_paste': ActionType.TEXT_PASTE,
            'text_copy': ActionType.TEXT_COPY,
            'content_insert': ActionType.CONTENT_INSERT,
            'content_insert_condition': ActionType.CONTENT_INSERT_CONDITION,
            'content_insert_loop': ActionType.CONTENT_INSERT_LOOP,
            'content_replace': ActionType.CONTENT_REPLACE,
            'content_delete': ActionType.CONTENT_DELETE,
            'build_success': ActionType.BUILD_SUCCESS,
            'build_failed': ActionType.BUILD_FAILED,
            'debug_run': ActionType.DEBUG_RUN,
            'debug_break': ActionType.DEBUG_BREAK,
            'debug_exception_not_handled': ActionType.DEBUG_EXCEPTION_NOT_HANDLED,
            'browser_url': ActionType.BROWSER_URL,
            'browser_url_close': ActionType.BROWSER_URL_CLOSE,
            'browser_copy': ActionType.BROWSER_COPY,
            'browser_paste': ActionType.BROWSER_PASTE,
            'browser_cut': ActionType.BROWSER_CUT,
            'test': ActionType.TEST,
            'text_undo': ActionType.TEXT_UNDO,
            'text_redo': ActionType.TEXT_REDO,
        }

        acid = res[name]
        li = [(1 if (n+1) == acid else 0) for n in range(ActionType.COUNT)]
        arr = np.array(li).T
        return arr

    @staticmethod
    def item_to_name(item):
        '''
        Get the feature name of the data item base on operator id
        :param item: data item
        :return: feature name
        '''
        id = item['operator']
        content = ''
        if 'buildlogcontent' in item:
            content = item['buildlogcontent']
        if 'textto' in item:
            content = item['textto']
        res = {
            '1': 'text_save',
            '2': 'text_cut',
            '3': 'text_paste',
            '4': 'text_copy',
            '5': 'content_insert' if (id != '5' or (ActionType.check_key_content(content)['condition'] == 0 and
                                      ActionType.check_key_content(content)['loop'] == 0)) else (
                'content_insert_loop' if ActionType.check_key_content(content)[
                                                  'loop'] == 1 else 'content_insert_condition'),
            '6': 'content_replace',
            '7': 'content_delete',
            '8': '',
            '9': 'build_success' if id != '10' or deal_result(content) == 1 else 'build_failed',
            '10': 'debug_run',
            '11': 'debug_break',
            '12': 'debug_exception_not_handled',
            '13': 'browser_url',
            '14': 'browser_url_close',
            '15': 'browser_copy',
            '16': 'browser_paste',
            '17': 'browser_cut',
            '18': 'test',
            '19': 'text_undo',
            '20': '',
            '21': 'text_redo',
            '22': ''
        }
        return res[id]

    @staticmethod
    def check_key_content(content):
        '''
        check the key word in input string.
        :param content: input string
        :return: key dict which record whether input has key word
        '''
        res = {'condition': 0, 'loop': 0}
        pattern_loop = re.compile('while|for')
        pattern_con = re.compile('if|switch')
        if pattern_con.search(content):
            res['condition'] = 1
        if pattern_loop.search(content):
            res['loop'] = 1
        return res


def convert_to_action_seq(data):
    '''
    convert data list to action feature name list
    :param data: data list
    :return: action feature name list
    '''
    res = []
    for item in data:
        str = ActionType.item_to_name(item)
        if str !=None and str != '':
            res.append(str)
    return res


def convert_to_feature_seq(namelist):
    '''
    convert action feature name list to vector list
    :param namelist: action feature name list
    :return: vector list
    '''
    res = []
    for name in namelist:
        arr = ActionType.name_to_feature(name)
        res.append(arr)
    return res


def convert_data_to_feature_seq(data):
    '''
    convert data list to vector list directly
    :param data: data list
    :return: vector list, score
    '''
    return (convert_to_feature_seq(convert_to_action_seq(data)), extract_score(data))



