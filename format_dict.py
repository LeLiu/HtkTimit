#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
#import logging

def format_dict_line(line):
    line = line.replace('/', '')
    word, *phones = line.split()
    word = word.upper()
    line = ' '.join([word] + list(phones))
    return line

def format_dict_file(raw_file, formated_file):
    with open(formated_file, 'w') as wf:
        with open(raw_file, 'r') as rf:
            for line in rf:
                if line and line[0] != ';':
                    line = format_dict_line(line)
                    wf.write('{}\n'.format(line))
    return 0

def _parse_args():
    parser = argparse.ArgumentParser(
        description='use the TIMIT dict to generate a dict conform HTK format specifications')

    parser.add_argument('timit_dict', type=str, help='timit dict (input) path')
    parser.add_argument('htk_dict', type=str, help='htk dict (output) path')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    #logging.getLogger().setLevel(logging.INFO)

    format_dict_file(args.timit_dict, args.htk_dict)

    #logging.info('{} lines formated.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()
    