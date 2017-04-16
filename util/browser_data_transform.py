from util.db_action import get_all_information_from_table_as_pd_dataframe, do_sql
from util import constant
from util.utility import string_to_datetime
import pandas as pd
import json

def map_bytes_to_utf(byt):
    return byt.decode('utf-16')


def combine_broswer_data(con):
    df = get_all_information_from_table_as_pd_dataframe(con, constant.ITEMTABLE)

    if not isinstance(df, pd.DataFrame):
        raise ValueError("should be a pd.DataFrame object")

    df['value'] = df['value'].map(map_bytes_to_utf)
    dict_list = []
    for r in df.iterrows():
        if r[1]['key'] != 'count':
            dict_list.append(transform_browser(r[1]))
    return dict_list


def transform_browser(ds):
    if not isinstance(ds, pd.Series):
        raise ValueError("should be a pd.Series object")
    assert 'value' in ds
    js = ds['value']
    obj = transform_jsonstr_to_ele(js)
    obj['id'] = ds['key']
    return obj


def transform_jsonstr_to_ele(jsonstr):
    ele = json.loads(jsonstr)
    assert 'time' in ele
    ele['time'] = string_to_datetime(ele['time'])
    if ele['type'] == 'url':
        ele[constant.OperatorType.NAME] = constant.OperatorType.BROWSER_URL
    elif ele['type'] == 'copy':
        ele[constant.OperatorType.NAME] = constant.OperatorType.BROWSER_COPY
    elif ele['type'] == 'paste':
        ele[constant.OperatorType.NAME] = constant.OperatorType.BROWSER_PASTE
    elif ele['type'] == 'cut':
        ele[constant.OperatorType.NAME] = constant.OperatorType.BROWSER_CUT
    return ele

