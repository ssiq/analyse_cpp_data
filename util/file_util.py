#coding=utf-8
import codecs
import os


def savefile(path, content, filecoding):
    (filepath, tempfilename) = os.path.split(path)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    file = codecs.open(path, 'w', encoding = filecoding)
    file.write(content)
    file.flush()
    file.close()


def savebytesfile(path, content):
    (filepath, tempfilename) = os.path.split(path)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    file = codecs.open(path, 'wb')
    file.write(content)
    file.flush()
    file.close()
