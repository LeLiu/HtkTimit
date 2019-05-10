#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

def read_dict(file_path, comment='#'):
    dic = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line[0] == comment:
                continue
            key, *value = line.split()
            dic[key] = ' '.join(list(value))
    return dic

def write_dict(dic, file_path):
    line_num = 0
    with open(file_path, 'w') as f:
        for key in dic:
            f.write('{0} {1}\n'.format(key, dic[key]))
            line_num += 1
    return line_num

def sort_dict(dic):
    sorted_dict = {}
    for key in sorted(dic.keys()):
        sorted_dict[key] = dic[key]
    return sorted_dict

def read_list(file_path, comment='#'):
    lis = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line[0] == comment:
                continue
            lis.append(line)
    return lis

def write_list(lis, file_path):
    line_num = 0
    with open(file_path, 'w') as f:
        for line in lis:
            f.write('{0}\n'.format(line))
            line_num += 1
    return line_num

def _extract_paths(dir_path, path_list, ext_name):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isdir(file_path):
            _extract_paths(file_path, path_list, ext_name)
        elif os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            if ext.lower() == ext_name.lower() or ext_name == '.*':
                path_list.append(file_path)
    return path_list

def gen_path_list(dir_path, ext='.*'):
    trans_list = []
    return _extract_paths(dir_path, trans_list, ext)

    
        

    