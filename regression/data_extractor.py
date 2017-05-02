from present.plot_insert_delete import extract_freq_df
from util import constant


def extract_features_and_score(data):
    '''
    :param data: a dict list
    :return:
    '''
    build_count = 0
    debug_count = 0
    browser_count = 0
    start_time = data[0]['time']
    end_time = ''
    for d in data:
        if d['operator'] == '9':
            build_count += 1
        if d['operator'] == '10':
            debug_count += 1
        if d['operator'] == '13':
            browser_count += 1
        if constant.OperatorType.id_to_category(d['operator']) != 'browser':
            end_time = d['time']

    insert_delete_df = extract_freq_df(data, '1Min')
    laplace_smoothing = 10
    insert_delete_df['add'] += laplace_smoothing
    insert_delete_df['delete'] += laplace_smoothing
    insert_delete_ratio = (insert_delete_df['add'] / insert_delete_df['delete']).mean()

    insert_sum = 0
    insert_times = 0
    score = 0.0
    for item in data:
        if item[constant.OperatorType.NAME] == constant.OperatorType.CONTENT_INSERT:
            insert_sum += len(item['textto'])
            insert_times += 1
        if item[constant.OperatorType.NAME] == constant.OperatorType.TEST:
            message = item['message']
            score = max(score, (len(message['AC']))/
                        float(len(message['TIE'])+len(message['WA'])+len(message['AC'])))

    return [(end_time-start_time).total_seconds(),
            float(insert_sum)/insert_times, build_count, debug_count, browser_count, insert_delete_ratio], score
