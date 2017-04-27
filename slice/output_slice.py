def output_stat(output, title_list, stat):
    output.write('||')
    for key_title in title_list:
        output.write(str(key_title).replace('\n', ' ')+ '|')
    output.write("\n")
    output.write('|-|')
    for key_title in title_list:
        output.write('-|')
    output.write('\n')
    i = 0
    for item in stat:
        i += 1
        output.write('|'+str(i).replace('\n', '')+'|')
        for key_title in title_list:
            if key_title == "":
                output.write("|")
                continue
            key_list = key_title.split('.')
            val = item
            for key_item in key_list:
                val = val[key_item]
            output.write(str(val).replace('&', '&amp;').replace('<','&lt;').replace('\r\n', '<br />').replace('|', '-') + '|')
        output.write('\n')