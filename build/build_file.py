import os
from util.constant import OperatorType
from util.file_util import savefile
from util.file_util import savebytesfile
import re
from lxml import etree


def output_build_files(data, targetpath):
    if not os.path.exists(targetpath):
        os.makedirs(targetpath)
    os.removedirs(targetpath)

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
            save_project(projects[projectname], tmppath)
            errs = deal_error(item['buildlogcontent'])
            err_xml = convert_to_xml(errs)
            output_errors_xml(tmppath, err_xml)


def save_project(project, targetpath):
    if not os.path.exists(targetpath):
        os.makedirs(targetpath)
    if 'files' not in project:
        return
    files = project['files']
    for (key, value) in files.items():
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


def deal_error(content):
    errs = []
    lines=content.split("\n")
    for temp in lines:
        temp=temp.strip()
        temps=temp.split(">")
        if len(temps)>1:
            line=temp[2:]
        else:
            line=temp
        pattern=re.compile(r"^(.*): (fatal |)error (\w*): (.*)$")
        match=pattern.search(line)
        if match:
            position=match.group(1)
            code=match.group(3)
            message=match.group(4)
            err = {'line': line, 'position': position, 'code': code, 'message': message}
            errs.append(err)
            print(position+"\t"+code+"\t"+message)
    return errs


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
