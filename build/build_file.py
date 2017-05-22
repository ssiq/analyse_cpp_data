import os
from util.constant import OperatorType
from util.file_util import savefile
from util.file_util import savebytesfile
from build.error_util import deal_error as deal_error
import re
from lxml import etree


def output_build_files(data, targetpath):
    if not os.path.exists(targetpath):
        os.makedirs(targetpath)
    import shutil
    shutil.rmtree(targetpath)

    projects = {}
    for item in data:
        if item[OperatorType.NAME] == OperatorType.TEXT_SAVE:
            filename = item['name']
            projectname = 'default'
            if projectname not in projects:
                projects[projectname] = {'name': projectname, 'files': {}, 'build_count': 0}
            files = projects[projectname]['files']
            if filename not in files:
                files[filename] = {'name': filename, 'content': item['content']}
            else:
                files[filename]['content'] = item['content']
        elif item[OperatorType.NAME] == OperatorType.BUILD:
            #projectname = item['projectname']
            projectname = 'default'
            if projectname not in projects:
                projects[projectname] = {'name': projectname, 'files': {}, 'build_count': 0}
            projects[projectname]['build_count'] += 1
            tmppath = os.path.join(targetpath, projectname, str(projects[projectname]['build_count']))
            filelist = deal_files(item['buildlogcontent'])
            save_project(projects[projectname], tmppath, filelist)
            errs = deal_error(item['buildlogcontent'])
            err_xml = convert_to_xml(errs)
            output_errors_xml(tmppath, err_xml)


def save_project(project, targetpath, filelist=[]):
    if not os.path.exists(targetpath):
        os.makedirs(targetpath)
    if 'files' not in project:
        return
    files = project['files']
    for (key, value) in files.items():
        if value['name'] not in filelist and filelist is not [] and value['name'][len(value['name'])-4:len(value['name'])] == '.cpp':
            continue

        path = os.path.join(targetpath, value['name'])
        encoding = 'utf-8'
        savefile(path, value['content'], encoding)


def save_all_projects(projects, targetpath):
    for (key, value) in projects.items():
        #projectname = value['name']
        projectname = 'default'
        projects[projectname]['build_count'] += 1
        tmppath = os.path.join(targetpath, projectname, str(projects[projectname]['build_count']))
        save_project(value, tmppath)


def deal_files(content):
    files = []
    lines = content.split("\n")
    for temp in lines:
        temp = temp.strip()
        temps = temp.split(">")
        if len(temps) > 1:
            line = temp[2:]
        else:
            line = temp
        pattern = re.compile(r"^cl(.*)\.cpp\"?$")
        match = pattern.search(line)
        if match:
            keylist = match.group(0).split(" ")
            for keyname in keylist:
                if keyname[0:1] == '"':
                    keyname = keyname[1:len(keyname)-1]
                    #print(keyname)
                if keyname[len(keyname)-4:len(keyname)] != '.cpp':
                    continue
                files.append(keyname)
    return files


def convert_to_xml(errs):
    root = etree.Element("errors")
    key_list = ['line', 'position', 'code', 'message']
    for item in errs:
        error = etree.SubElement(root, 'error')
        for keyt in key_list:
            tmp = etree.SubElement(error, keyt)
            tmp.text = item[keyt]
    return root


def output_errors_xml(targetpath, xml_ele):
    str = etree.tostring(xml_ele, pretty_print=True, encoding='utf-8')
    path = os.path.join(targetpath, 'error_list.xml')
    savebytesfile(path, str)
