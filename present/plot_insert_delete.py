import pandas as pd
from util.constant import OperatorType as OperatorType
import plotly.graph_objs as go


def _extract_freq_df(data, freq):
    insert_delete_dict = {}
    for item in data:
        if item[OperatorType.NAME] == OperatorType.CONTENT_INSERT \
                or item[OperatorType.NAME] == OperatorType.CONTENT_DELETE:
            insert_delete_dict['time'] = item['item']
            insert_delete_dict['delete'] = len(item['textfrom'])
            insert_delete_dict['add'] = len(item['textto'])
    insert_delete_df = pd.DataFrame(insert_delete_dict)
    insert_delete_df = insert_delete_df.groupby(pd.Grouper(key='time', freq=freq)).sum()
    return insert_delete_df


def insert_delete_scatter_trace(data, freq):
    '''
    :param data: a data dict list
    :param freq: a pandas time freq string
    :return: a plotly trace object x is insert, y is delete
    '''
    insert_delete_df = _extract_freq_df(data, freq)
    x = []
    y = []
    for item in insert_delete_df.iterrows():
        x.append(item[1]['add'])
        y.append(item[1]['delete'])
    return go.Scatter(x=x, y=y, name='insert delete', mode='markers')


def insert_delete_scatter_trace_3d(data, freq):
    '''
    :param data:  a data dict list
    :param freq: a pandas time freq string
    :return: a plotly trace object x is insert, y is delete, z is time
    '''
    insert_delete_df = _extract_freq_df(data, freq)
    x = []
    y = []
    z = []
    for item in insert_delete_df.iterrows():
        x.append(item[1]['add'])
        y.append(item[1]['delete'])
        z.append(item[0])
    return go.Scatter3d(x=x, y=y, z=z, mode='markers')


def insert_delete_ratio_trace(data, freq, laplace_smoothing=10):
    '''
    :param data:  a data dict list
    :param freq: a pandas time freq string
    :param laplace_smoothing: laplace_smoothing parameter used to (x+laplace_smoothing)/(y+laplace_smoothing)
    :return: a plotly trace object x is time, y is the ratio of insert and delete
    '''
    insert_delete_df = _extract_freq_df(data, freq)
    insert_delete_df['add'] += laplace_smoothing
    insert_delete_df['delete'] += laplace_smoothing
    x = insert_delete_df.index
    y = insert_delete_df['add']/insert_delete_df['delete']
    return go.Bar(x=x, y=y, name='insert_delete_ratio')

