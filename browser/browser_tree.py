import util.browser_data_transform as bro
import util.constant as constant
import datetime

def get_browser_action(data):
    res = []
    for item in data:
        if constant.OperatorType.id_to_category(item[constant.OperatorType.NAME]) == 'browser':
            if item['type'] == 'url' and item['url'] == 'chrome://newtab/':
                item['openerTabId'] = -1
            res.append(item)
    return res

def find_by_id(data, tabId):
    for item in data:
        if 'tabId' not in item:
            continue
        if item['tabId'] == tabId:
            return item
        if 'children' in item:
            res = find_by_id(item['children'], tabId)
            if res is not None:
                return res
    return None

def find_by_childrenid(data, tabId):
    for item in data:
        if 'tabId' not in item:
            continue
        if item['tabId'] == tabId:
            return data
        if 'children' in item:
            res = find_by_childrenid(item['children'], tabId)
            if res is not None:
                return res
    return None

def data_append(data, item, key):
    if key not in data:
        data[key] = []
    data[key].append(item)
    return

def addDirty(res, dirty):
    for item in dirty:
        temp = {}
        if item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_URL:
            temp['name'] = item['type'] + '_' + str(item['tabId']) + '_' + item['title'] +'_'+item['url']
            temp['isParent'] = 'true'
            temp['icon'] = 'test.png'
            sam = find_by_id(res, item['tabId'])
            if sam is not None:
                sam2 = find_by_childrenid(res, item['tabId'])
                sam['tabId'] = -1
                temp['tabId'] = item['tabId']
                sam2.append(temp)
                dirty.remove(item)
            elif sam is None:
                sam = find_by_id(res, item['openerTabId'])
                if sam is not None:
                    temp['tabId'] = item['tabId']
                    data_append(sam, temp, 'children')
                    dirty.remove(item)
                elif sam is None:
                    temp['tabId'] = item['tabId']
                    res.append(temp)
                    dirty.remove(item)
        elif item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_URL_CLOSE:
            sam = find_by_id(res, item['tabId'])
            if sam is not None:
                data_append(sam, {'name': 'tab closed'}, 'children')
                dirty.remove(item)
        elif item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_COPY or item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_CUT or item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_PASTE:
            sam = find_by_id(res, item['tabId'])
            if sam is None:
                continue
            t = item['type'] + '_' + item['content']
            data_append(sam, {'name': t}, 'children')
            dirty.remove(item)



def get_show_struct(data):
    res = []
    dirty = []
    for item in data:
        temp = {}
        if item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_URL:
            temp['name'] = item['type'] + '_' + str(item['tabId']) + '_' +str(item['time'])+'_'+item['title']+'_'+item['url']
            temp['isParent'] = 'true'
            temp['icon'] = r'js/test.png'
            sam = find_by_id(res, item['tabId'])
            if sam is not None:
                sam2 = find_by_childrenid(res, item['tabId'])
                sam['tabId'] = -1
                temp['tabId'] = item['tabId']
                sam2.append(temp)
            elif sam is None:
                sam = find_by_id(res, item['openerTabId'])
                if sam is not None:
                    temp['tabId'] = item['tabId']
                    data_append(sam, temp, 'children')
                elif sam is None:
                    temp['tabId'] = item['tabId']
                    res.append(temp)
            addDirty(res, dirty)
        elif item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_URL_CLOSE:
            sam = find_by_id(res, item['tabId'])
            if sam is not None:
                data_append(sam, {'name': 'tab closed_'+str(item['time'])}, 'children')
        elif item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_COPY or item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_CUT or item[constant.OperatorType.NAME] == constant.OperatorType.BROWSER_PASTE:
            #(item)
            sam = find_by_id(res, item['tabId'])
            if sam == None:
                dirty.append(item)
                print(item)
                continue
            t = item['type']+'_'+str(item['time'])+'_'+item['content']
            data_append(sam, {'name': t}, 'children')
    return res
