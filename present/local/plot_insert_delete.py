from present.plot_insert_delete import extract_freq_df

def insert_delete_box_trace(alldata, namelist=None, sizex=8, sizey=6, title='盒状图'):
    from present.local.plot_util import show_box
    scas = []
    if namelist == None:
        namelist = []
    for i in range(1, len(alldata)+1):
        namelist.append("User"+str(i))

    for data in alldata:
        from util.data_filter import move_paste_insert
        moved_data = move_paste_insert(data)
        insert_delete_df = extract_freq_df(moved_data, freq='1Min')
        ratio = []
        for item in insert_delete_df.iterrows():
            item_add = item[1]['add']
            item_delete = item[1]['delete']
            if item_delete == 0:
                item_delete = 1
            #print('insert:{}| delete:{}| {}'.format(str(item_add), str(item_delete), str(item_add / item_delete)))
            if item_add/item_delete>150:
                continue
            ratio.append(item_add / item_delete)
        scas.append(ratio)
    show_box(scas, namelist, sizex, sizey, title)
