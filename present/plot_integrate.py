import pandas as pd
from util.constant import OperatorType as OperatorType
import matplotlib.pyplot as plt
import matplotlib
import datetime
import slice.stat_slice as stat
import numpy as np
from matplotlib.lines import Line2D
import plotly
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools
import scipy.stats as stats


def show_insert(data):
    leg=['text', 'build', 'debug']
    period = 1
    first = data[0]
    last = data[len(data) - 1]
    rng = pd.date_range(first['time']-datetime.timedelta(seconds=period-1), last['time'], freq='s')
    dict_from = {}
    dict_to = {}
    dict_build_success = {}
    dict_build_failed = {}
    dict_debug_run = {}
    dict_debug_end = {}
    for item in data:
        if item[OperatorType.NAME] == OperatorType.CONTENT_INSERT \
                or item[OperatorType.NAME] == OperatorType.CONTENT_DELETE:
            for i in range(period):
                delta = datetime.timedelta(seconds=i)
                time = item['time'] - delta
                if time not in dict_from:
                    dict_from[time] = 0
                dict_from[time] += ((len(item['textfrom']) - 2) / period)
                if time not in dict_to:
                    dict_to[time] = 0
                dict_to[time] += ((len(item['textto']) - 2) / period)
            if item['time'] not in dict_from:
                dict_from[item['time']] = 0
            #dict_from[item['time']] += len(item['textfrom'])
            if item['time'] not in dict_to:
                dict_to[item['time']] = 0
                #dict_to[item['time']] += len(item['textto'])
        if item[OperatorType.NAME] == '9':
            if stat.deal_result(item['buildlogcontent']):
                dict_build_success[item['time']] = -5
            else:
                dict_build_failed[item['time']] = -5
        if item[OperatorType.NAME] == '10':
            dict_debug_run[item['time']] = -5
        if item[OperatorType.NAME] == '11':
            dict_debug_end[item['time']] = -5
    pic_data = {}
    if 'text' in leg:
        pic_data['add'] = dict_to
        pic_data['delete'] = dict_from
    if 'build' in leg:
        pic_data['build_success'] = dict_build_success
        pic_data['build_failed'] = dict_build_failed
    if 'debug' in leg:
        pic_data['debug_run'] = dict_debug_run
        pic_data['debug_end'] = dict_debug_end
    pic = pd.DataFrame(pic_data, index=rng)
    pic = pic.fillna(value=0)

    fig = tools.make_subplots(rows=4, cols=1, shared_xaxes=True)

    fig.append_trace(go.Scatter(x=pic.index, y=pic['add'], name='add'), 1, 1)
    fig.append_trace(go.Scatter(x=pic.index, y=pic['delete'], name='delete'), 2, 1)

    debug_list = []
    pre_run = None
    for t in pic.index:
        if pic.loc[t, 'debug_run'] != 0:
            pre_run = t
        if pic.loc[t, 'debug_end'] != 0:
            if pre_run is None:
                continue
            debug_list.append([pre_run, t])
            pre_run = None

    if len(debug_list) != 0:
        y_begin = int(-len(debug_list)/2)
        x = [debug_list[0][0], debug_list[0][1]]
        y = [y_begin, y_begin]
        pre_end = debug_list[0][1]
        for tx, ty in zip(debug_list[1:], range(y_begin+1, y_begin+len(debug_list))):
            x.append(pre_end+(tx[0]-pre_end)/2)
            y.append(None)
            x.extend(tx)
            y.extend([ty, ty])
            pre_end = tx[1]
        fig.append_trace(go.Scatter(x=x, y=y, name='debug', line={'width': 10}), 3, 1)

    build_success_x = []
    build_failed_x = []
    for t in pic.index:
        if pic.loc[t, 'build_success'] != 0:
            build_success_x.append(t)
        if pic.loc[t, 'build_failed'] != 0:
            build_failed_x.append(t)
    fig.append_trace(go.Scatter(x=build_success_x, y=['success']*len(build_success_x),
                                name='build_success', mode='markers'), 4, 1)
    fig.append_trace(go.Scatter(x=build_failed_x, y=['failed']*len(build_failed_x), name='build_failed', mode='markers')
                     , 4, 1)

    py.iplot(fig)

    fig = tools.make_subplots(rows=4, cols=1, shared_xaxes=True)
    is_begin = True
    insert_count = 0
    ratio_list = []
    insert_list = []
    delete_list = []
    for item in data:
        if item[OperatorType.NAME] == OperatorType.CONTENT_INSERT:
            num = len(item['textto']) - 2
            insert_count += num
            insert_list.append(num)
        elif item[OperatorType.NAME] == OperatorType.CONTENT_DELETE:
            num = len(item['textfrom'])-2
            ratio_list.append(insert_count/num)
            delete_list.append(num)
            insert_count = 0

    fig.append_trace(go.Histogram(x=ratio_list, name='number of insert characters/number of delete characters'), 1, 1)
    fig.append_trace(go.Histogram(x=insert_list, name='insert'), 2, 1)
    fig.append_trace(go.Histogram(x=delete_list, name='delete'), 3, 1)

    paste_first = True
    paste_list = []
    paste_count = 0
    for item in data:
        if item[OperatorType.NAME] == OperatorType.TEXT_COPY \
                or item[OperatorType.NAME] == OperatorType.TEXT_CUT:
            if not paste_first:
                paste_list.append(paste_count)
                paste_count = 0
            else:
                paste_count = 0
            paste_first = False
        elif item[OperatorType.NAME] == OperatorType.TEXT_PASTE:
            paste_count += 1

    paste_list.append(paste_count)
    fig.append_trace(go.Histogram(x=paste_list, name='paste count per copy/cut'), 4, 1)

    py.iplot(fig)
