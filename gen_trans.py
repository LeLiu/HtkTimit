#!/usr/bin/env python
#-*- coding:utf-8 -*-

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


def gen_trans_file_list(dir_path):
    trans_list = []
    return dir_to_path_list(dir_path, trans_list, '.txt')

def write_dict(dic, file_path):
    line_num = 0
    with open(file_path, 'w') as f:
        for key in dic:
            f.write('{0} {1}\n'.format(key, dic[key]))
            line_num += 1
    return line_num

def format_word(word):
    word = word.upper()
    chrs =  list(filter(lambda c : c.isalpha() or c == "'" or c == "-", word))
    word = ''.join(chrs)
    word_temp = word.replace('-', '').replace("'", '')
    if len(word_temp) > 0:
        return word
    else:
        return None

def trans_files_to_dict(trans_list):
    dic = {}
    for tf_path in trans_list:
        with open(tf_path, 'r') as tf:
            line = tf.readline()
            _, _, *words = line.split()
            words = map(lambda w : format_word(w), words)
            words = list(filter(lambda w : w is not None, words))
            line = ' '.join(words)
            tf_name, _ = os.path.splitext(tf_path)
            dic[tf_name] = line
    return dic

def _parse_args():
    parser = argparse.ArgumentParser(
        description='generate a global transcriptions file')

    parser.add_argument('data_path', type=str, help='a data dir that store the per wav transcription files')
    parser.add_argument('trans_path', type=str, help='path of the output global transcription file file')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    trans_file_list = gen_trans_file_list(args.data_path)
    trans_dict = trans_files_to_dict(trans_file_list)
    line_num = write_dict(trans_dict, args.trans_path)

    logging.info('{} transcriptions processed.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()

            



