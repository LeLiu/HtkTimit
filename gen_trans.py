#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
import logging
import util

def format_word(word):
    word = word.split('~')[0]
    chrs =  list(filter(lambda c : c.isalpha() or c == "'" or c == "-", word))
    word = ''.join(chrs)
    word = word.replace("'", '_')
    word = word.upper()

    word_temp = word.replace('-', '').replace('_', '')
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

    trans_file_list = util.gen_path_list(args.data_path, ext='.txt')
    trans_dict = trans_files_to_dict(trans_file_list)
    line_num = util.write_dict(trans_dict, args.trans_path)

    logging.info('{} transcriptions processed.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()

            



