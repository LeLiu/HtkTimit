#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
import logging
import util

def extract_words(trans_path):
    words_set = set()
    with open(trans_path, 'r') as tf:
        for line in tf:
            _, *words = line.split()
            words = list(words)
            words_set.update(words)
    words_list = list(words_set)
    words_list.sort()
    return words_list

def _parse_args():
    parser = argparse.ArgumentParser(
        description='extract words list from the global transcriptions file')

    parser.add_argument('trans_path', type=str, help='path of the input transcriptions file')
    parser.add_argument('words_path', type=str, help='path of the output words list file')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    words_list = extract_words(args.trans_path)
    line_num = util.write_list(words_list, args.words_path)

    logging.info('{} words extracted.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()

