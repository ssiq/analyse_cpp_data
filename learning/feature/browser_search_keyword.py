import re
import urllib
from util.constant import OperatorType

def get_keyword_from_url(url):
    search_url = [
        {'website': 'www.baidu.com', 'uri': '/s', 'param': 'wd'},
        {'website': 'www.google.com', 'uri': '/search', 'param': 'q'},
        {'website': 'cn.bing.com', 'uri': '/search', 'param': 'q'}
                  ]
    mat = re.compile(r'^((?:https|http|chrome):\/\/)?([^\/]+)(\/[\/\w]*\.?[\w]*)?(\?[\w=%*&-_]*)?(#[\w\/=%*&-_!]*)?$')
    res = mat.search(url)
    is_search = 0
    if res:
        #print(res.group(1), res.group(2), res.group(3), res.group(4), res.group(5))
        for sea in search_url:
            if res.group(2) == sea['website'] and res.group(3) == sea['uri']:
                if res.group(4):
                    is_search = 1
                    #print(res.group(1), res.group(2), res.group(3), res.group(4), res.group(5))
                    params = res.group(4)
                    if params[0] == '?':
                        params = params[1:]
                    para_list = params.split('&')
                    for para in para_list:
                        pa = para.split('=')
                        if pa[0] == sea['param']:
                            #print(urllib.parse.unquote(pa[1]))
                            return urllib.parse.unquote(pa[1])
        #print(res.group(1), res.group(2), res.group(3), res.group(4), res.group(5))
    if is_search:
        return ''
    return None

