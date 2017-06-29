import re
import numpy as np
from learning.feature.data_extractor import extract_score
from slice.stat_slice import deal_result
from learning.feature.lexical_analysis import get_token_list
from util.constant import OperatorType
from learning.feature.browser_search_keyword import get_keyword_from_url


class ActionType:

    COUNT = 36

    TEXT_SAVE = 1
    TEXT_CUT = 2
    TEXT_CUT_CONDITION = 3
    TEXT_CUT_LOOP = 4
    TEXT_CUT_LOGIC = 5
    TEXT_PASTE = 6
    TEXT_PASTE_CONDITION = 7
    TEXT_PASTE_LOOP = 8
    TEXT_PASTE_LOGIC = 9
    TEXT_COPY = 10
    TEXT_COPY_CONDITION = 11
    TEXT_COPY_LOOP = 12
    TEXT_COPY_LOGIC = 13
    CONTENT_INSERT = 14
    CONTENT_INSERT_CONDITION = 15
    CONTENT_INSERT_LOOP = 16
    CONTENT_INSERT_KEYWORD = 17
    CONTENT_INSERT_FUNCTION = 18
    CONTENT_INSERT_COMPARE = 19
    CONTENT_INSERT_ASSIGN = 20
    CONTENT_INSERT_CALCULATE = 21
    CONTENT_REPLACE = 22
    CONTENT_DELETE = 23
    BUILD_SUCCESS = 24
    BUILD_FAILED = 25
    DEBUG_RUN = 26
    DEBUG_BREAK = 27
    DEBUG_EXCEPTION_NOT_HANDLED = 28
    BROWSER_URL = 29
    BROWSER_URL_CLOSE = 30
    BROWSER_COPY = 31
    BROWSER_PASTE = 32
    BROWSER_CUT = 33
    TEST = 34
    TEXT_UNDO = 35
    TEXT_REDO = 36

    @staticmethod
    def name_to_feature(name):
        res = {
            'text_save': ActionType.TEXT_SAVE,
            'text_cut': ActionType.TEXT_CUT,
            'text_cut_condition': ActionType.TEXT_CUT_CONDITION,
            'text_cut_loop': ActionType.TEXT_CUT_LOOP,
            'text_cut_logic': ActionType.TEXT_CUT_LOGIC,
            'text_paste': ActionType.TEXT_PASTE,
            'text_paste_condition': ActionType.TEXT_PASTE_CONDITION,
            'text_paste_loop': ActionType.TEXT_PASTE_LOOP,
            'text_paste_logic': ActionType.TEXT_PASTE_LOGIC,
            'text_copy': ActionType.TEXT_COPY,
            'text_copy_condition': ActionType.TEXT_COPY_CONDITION,
            'text_copy_loop': ActionType.TEXT_COPY_LOOP,
            'text_copy_logic': ActionType.TEXT_COPY_LOGIC,
            'content_insert': ActionType.CONTENT_INSERT,
            'content_insert_condition': ActionType.CONTENT_INSERT_CONDITION,
            'content_insert_loop': ActionType.CONTENT_INSERT_LOOP,
            'content_insert_function': ActionType.CONTENT_INSERT_FUNCTION,
            'content_insert_keyword': ActionType.CONTENT_INSERT_KEYWORD,
            'content_insert_compare': ActionType.CONTENT_INSERT_COMPARE,
            'content_insert_assign': ActionType.CONTENT_INSERT_ASSIGN,
            'content_insert_calculate': ActionType.CONTENT_INSERT_CALCULATE,
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
        '''
        Get the vector form about the action name
        :param name: action name
        :return: vector
        '''

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
        if 'url' in item:
            content = item['url']
        command_content = ActionType.check_command_content(content, item['operator'])
        insert_content = ActionType.check_insert_content(content, item['operator'])
        search_content = ActionType.get_url_feature(content, item['operator'])
        res = {
            '1': 'text_save',
            '2': command_content,
            '3': command_content,
            '4': command_content,
            '5': insert_content,
            '6': 'content_replace',
            '7': 'content_delete',
            '8': '',
            '9': 'build_success' if id != '10' or deal_result(content) == 1 else 'build_failed',
            '10': 'debug_run',
            '11': 'debug_break',
            '12': 'debug_exception_not_handled',
            '13': search_content,
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
        if item['operator'] == OperatorType.CONTENT_INSERT:
            #print(res[id]+' | '+content)
            pass
        return res[id]

    @staticmethod
    def check_insert_content(content, item_operator):
        '''
        check the key word in input string.
        :param content: input string
        :return: key dict which record whether input has key word
        '''
        if item_operator != OperatorType.CONTENT_INSERT:
            return 'content_insert'

        res = 'content_insert'
        pattern_loop = re.compile('while|for')
        if pattern_loop.search(content):
            return res+'_loop'
        pattern_con = re.compile('(if|switch)\W+')
        if pattern_con.search(content):
            return res+'_condition'
        pattern_compare = re.compile('<[^<>]?|<=|!=|[^<>]?>|>=')
        if pattern_compare.search(content):
            pat_com = re.compile('<<|>>|<.*>')
            if not pat_com.search(content):
                pat_comp = re.compile('([^a-zA-Z0-9\s])[a-zA-Z0-9]*<[^<>]?|<=|!=|[^<>]?>|>=')
                if not pat_comp.search(content):
                    return res+'_compare'
        pattern_calculate = re.compile('\+|-|(\w)\*(\w)|(\w)/(\w)|->|<<|>>')
        if pattern_calculate.search(content):
            return res+'_calculate'
        pattern_assign = re.compile('=')
        if pattern_assign.search(content):
            return res+'_assign'
        pattern_function = re.compile('\S+\(')
        if pattern_function.search(content):
            pat_fun = re.compile('(if|switch|for|while)\(')
            if not pat_fun.search(content):
                return res+'_function'
        pattern_keyword = re.compile('(\W|^)(char|void|int|double|vector|string|set|const|include)(\W|$)')
        if pattern_keyword.search(content):
            return res+'_keyword'
        return res

    @staticmethod
    def check_command_content(content, item_operator):
        res = 'text'
        if item_operator != OperatorType.TEXT_SAVE and item_operator != OperatorType.TEXT_CUT and item_operator != OperatorType.TEXT_PASTE and item_operator != OperatorType.TEXT_COPY:
            return res
        elif item_operator == OperatorType.TEXT_CUT:
            res += '_cut'
        elif item_operator == OperatorType.TEXT_PASTE:
            res += '_paste'
        elif item_operator == OperatorType.TEXT_COPY:
            res += '_copy'

        pattern_loop = re.compile('while|for')
        if pattern_loop.search(content):
            return res+'_loop'
        pattern_con = re.compile('if|switch')
        if pattern_con.search(content):
            return res+'_condition'
        pattern_logic = re.compile('[+\-*/<>=;]')
        if pattern_logic.search(content):
            return res+'_logic'
        return res

    @staticmethod
    def get_url_feature(item, item_operator):
        if item_operator == OperatorType.BROWSER_URL:
            res = get_keyword_from_url(item['url'])
            if res:
                return 'browser_url'
        return 'browser_url'


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


def convert_insert_data_to_feature_seq(data):
    fea_list = []
    bound = [20, 30, 50, 60, 80, 90, 120, 130, 150, 160, 170]
    for item in data:
        if item['operator'] == OperatorType.CONTENT_INSERT:
            content = item['textto']
            tokens = get_token_list(content)
            for tok in tokens:
                keyid = tok['id']
                i = 0
                for b in bound:
                    if keyid > b:
                        i += 1
                li = [(1 if keyid == (n+1) else 0) for n in range(172)]
                arr = np.array(li).T
                fea_list.append(arr)
    return (fea_list, extract_score(data))







