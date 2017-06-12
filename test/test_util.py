import sqlite3
import os
from util import xml_operation as xml_ope


def clean_data(data):
    pick_id = ''
    pick_project = ''
    i = 0
    while i < len(data.dict_list):
        item = data.dict_list[i]
        if item['operator'] == '9':
            if item['projectname'] == pick_project and item['buildid'] == pick_id:
                del data.dict_list[i]
                i -= 1
                #print(item)
            else:
                pick_id = item['buildid']
                pick_project = item['projectname']
        i += 1
    return data

def read_data(path):
    print('Read data from {}'.format(path))
    db_path = os.path.join(path, 'monitor', 'Dao', 'log.db')
    bro_path = os.path.join(path, 'chrome', 'chrome-extension_gnodhpdneljjpjdoiadhmigdcblneeoa_0.localstorage')
    file_path = os.path.join(path, 'plugin')
    con = sqlite3.connect(db_path)
    con_bro = sqlite3.connect(bro_path)
    data = xml_ope.combine_database(con, con_bro, file_path)
    data = clean_data(data)
    con.close()
    con_bro.close()
    return data.dict_list


def read_group_data(fpath):
    all = []
    files = os.listdir(fpath)
    for f in files:
        path = os.path.join(fpath, f)
        if os.path.isdir(path):
            all.append(read_data(path))
    return all


def read_all_data():
    all = []
    data_path = r'..\data'
    dirs = os.listdir(data_path)
    print(dirs)
    for d in dirs:
        pa = os.path.join(data_path, d)
        if os.path.isdir(pa):
            all.extend(read_group_data(pa))
    return all
