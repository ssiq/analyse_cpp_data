import pandas as pd
from util.constant import OperatorType as OperatorType
import matplotlib.pyplot as plt
import matplotlib
import datetime
import slice.stat_slice as stat
import numpy as np
from matplotlib.lines import Line2D

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
        if item[OperatorType.NAME] == '5':
            for i in range(period):
                delta = datetime.timedelta(seconds=i)
                time = item['time'] - delta
                if time not in dict_from:
                    dict_from[time] = 0
                dict_from[time] += (len(item['textfrom']) / period)
                if time not in dict_to:
                    dict_to[time] = 0
                dict_to[time] += (len(item['textto']) / period)
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
    print(pic)

    pic.plot()
    plt.legend(loc='best')
    plt.show()
