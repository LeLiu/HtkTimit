#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os
import argparse
import logging

def dir_to_path_list(dir_path, path_list, ext_name):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isdir(file_path):
            dir_to_path_list(file_path, path_list, ext_name)
        elif os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            if ext.lower() == ext_name.lower() or ext_name == '.*':
                path_list.append(file_path)
    return path_list

def gen_wave_list(dir_path):
    wave_list = []
    return dir_to_path_list(dir_path, wave_list, '.wav')

def write_dict(dic, file_path):
    line_num = 0
    with open(file_path, 'w') as f:
        for key in dic:
            f.write('{0} {1}\n'.format(key, dic[key]))
            line_num += 1
    return line_num

def gen_feat_scp(wave_dir, feat_dir, feat_scp):
    wave_list = gen_wave_list(wave_dir)
    feat_list = list(map(lambda x : x.replace(wave_dir, feat_dir, 1), wave_list))
    wave_feat_dict = dict(zip(wave_list, feat_list))
    return write_dict(wave_feat_dict, feat_scp)

def _parse_args():

    parser = argparse.ArgumentParser(
        description='generate a feature extration script file')

    parser.add_argument('wave_dir', type=str, help='the wave data root directory')
    parser.add_argument('feat_dir', type=str, help='the feature data root directory')
    parser.add_argument('feat_scp', type=str, help='the feat extration scp file path')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    line_num = gen_feat_scp(args.wave_dir, args.feat_dir, args.feat_scp)

    logging.info('{} items processed.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()