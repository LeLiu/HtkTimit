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
    return word

def format_phones(phones):
    phones = phones.replace('/', '')
    phones = ' '.join(list(phones.split()))
    phones = phones.lower()
    return phones

def format_dict(src_file, dst_file):
    src_dict = util.read_dict(src_file, comment=';')
    dst_dict = {}
    for word, phones in src_dict.items():
        word = format_word(word)
        phones = format_phones(phones)
        dst_dict[word] = phones
    dst_dict = util.sort_dict(dst_dict)
    return util.write_dict(dst_dict, dst_file)

def _parse_args():
    parser = argparse.ArgumentParser(
        description='use the TIMIT dict to generate a dict conform HTK format specifications')

    parser.add_argument('timit_dict', type=str, help='timit dict (input) path')
    parser.add_argument('htk_dict', type=str, help='htk dict (output) path')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    line_num = format_dict(args.timit_dict, args.htk_dict)

    logging.info('{} lines formated.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()
    