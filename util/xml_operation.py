from util.db_action import get_all_information_from_table_as_pd_dataframe, do_sql
import pandas as pd
import lxml
from lxml import etree

from util.utility import string_to_datetime


class Data(object):
    def __init__(self, dict_list):
        root = etree.Element('root')
        for t in dict_list:
            action = etree.SubElement(root, 'action')
            for k, v in t.items():
                action.attrib[k] = str(v)
        self._xml_root = root
        self._dict_list = dict_list

    @property
    def xml_data(self):
        return self._xml_root

    @property
    def dict_list(self):
        return self._dict_list


def combine_database(con):
    '''
    This method get a database connection and merge the database to get a Data object
    ** The command file part and the debug sub table is not merged into the Data object. **
    :param con: a database connection
    :return: a Data object
    '''
    from util import constant
    res = []
    OPERATOR = constant.OperatorType.NAME
    TIME = 'time'

    def _check_series(s):
        if not isinstance(s, pd.Series):
            raise ValueError("should be a pd.Series object")

    def identity_transform(x):
        _check_series(x)
        return dict(x)

    def transform_df(df, transform_action=identity_transform):
        '''
        :param df:
        :param transform_action:
        :return: a map list
        '''
        if not isinstance(df, pd.DataFrame):
            raise ValueError("should be a pd.DataFrame object")
        return [transform_action(r[1]) for r in df.iterrows()]

    # transform the command_text table
    command_text_df = get_all_information_from_table_as_pd_dataframe(con, constant.COMMAND_TEXT)

    def command_text_transformer(element):
        if not isinstance(element, pd.Series):
            raise ValueError("should be a pd.Series object")
        keys = element.index
        assert 'time' in element
        r = {}
        for k in keys:
            if k == 'time':
                r[TIME] = string_to_datetime(element[k])
            elif k == 'action':
                action_map = {'Save': constant.OperatorType.TEXT_SAVE,
                              'Cut': constant.OperatorType.TEXT_CUT,
                              'Paste': constant.OperatorType.TEXT_PASTE,
                              'Copy': constant.OperatorType.TEXT_COPY}
                r[OPERATOR] = action_map[element[k]]
            else:
                r[k] = element[k]
        return r

    res.extend(transform_df(command_text_df, command_text_transformer))

    # transform the command_file table
    # this command file is not implement
    command_file_df = get_all_information_from_table_as_pd_dataframe(con, constant.COMMAND_FILE)

    def command_file_transformer(element):
        _check_series(element)
        raise NotImplementedError

    # transform content_info table
    content_file_df = get_all_information_from_table_as_pd_dataframe(con, constant.CONTENT_INFO)

    def content_file_transform(element):
        _check_series(element)
        action_map = {
            'Delete': constant.OperatorType.CONTENT_DELETE,
            'Insert': constant.OperatorType.CONTENT_INSERT,
            'Replace': constant.OperatorType.CONTENT_REPLACE,
            'Save': constant.OperatorType.CONTENT_SAVE,
        }
        r = {}
        assert 'time' in element
        for k in element.index:
            if k == 'time':
                r[TIME] = string_to_datetime(element[k])
            elif k == 'operation':
                r[OPERATOR] = action_map[element[k]]
            else:
                r[k] = element[k]
        return r

    res.extend(transform_df(content_file_df, content_file_transform))

    # transform build
    # build part is not implement
    build_info_df = get_all_information_from_table_as_pd_dataframe(con, 'build_info')
    build_project_info_df = get_all_information_from_table_as_pd_dataframe(con, "build_project_info")
    buid_joined_df = pd.merge(build_info_df, build_project_info_df,
                              left_on='buildstarttime', right_on='buildid',
                              suffixes=('_build_info', '_build_project_info'))

    def build_transform(element):
        _check_series(element)
        r = {}
        # print(element)
        assert 'time_build_info' in element
        for k in element.index:
            if k == 'time_build_info':
                r[TIME] = string_to_datetime(element[k])
            else:
                r[k] = element[k]

        r[OPERATOR] = constant.OperatorType.BUILD
        return r
    res.extend(transform_df(buid_joined_df, build_transform))

    # transform debug
    # debug part is not implement
    debug_info_df = get_all_information_from_table_as_pd_dataframe(con, 'debug_info')
    debug_break_df = get_all_information_from_table_as_pd_dataframe(con, 'debug_break')
    debug_run_df = get_all_information_from_table_as_pd_dataframe(con, 'debug_run')

    def debug_transform(element):
        _check_series(element)
        r = {}
        assert 'timestamp' in element
        for k in element.index:
            if k == 'type':
                r[OPERATOR] = {'run': constant.OperatorType.DEBUG_TUN,
                               'break': constant.OperatorType.DEBUG_BREAK,
                               'exception_not_handled': constant.OperatorType.DEBUG_EXCEPTION_NOT_HANDLED}[element[k]]
            elif k == 'timestamp':
                r[TIME] = string_to_datetime(element[k])
            else:
                r[k] = element[k]
        return r
    res.extend(transform_df(debug_info_df, debug_transform))

    res = sorted(res, key=lambda x: x[TIME])

    return Data(res)