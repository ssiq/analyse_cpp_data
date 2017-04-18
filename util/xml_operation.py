from util.db_action import get_all_information_from_table_as_pd_dataframe, do_sql
import pandas as pd
import lxml
from lxml import etree
import util.browser_data_transform as bro_transform
import util.monitor_data_transform as mon_transform
from util.test_score_log_transform import transform_test_log

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


def combine_database(con_mon=None, con_bro=None, test_log_handler=None):
    '''
    :param con_mon: a db connect object of codding
    :param con_bro: a db connect object of browser
    :param test_log_handler: a file like object of test log
    :return: a Data object
    '''
    res = []
    if con_mon:
        res.extend(mon_transform.combine_database(con_mon))
    if con_bro:
        res.extend(bro_transform.combine_broswer_data(con_bro))
    if test_log_handler:
        res.extend(transform_test_log(test_log_handler))

    res = sorted(res, key=lambda x: x['time'])
    return Data(res)
