#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
import logging
import util

def read_hmmdef(def_file, hmm_name):
    hmmdef = []
    with open(def_file, 'r') as f:
        for line in f:
            pure_line = line.strip()
            if not pure_line:
                continue
            if pure_line == '<ENDHMM>' and len(hmmdef) > 0:
                hmmdef.append(line)
                break
            elif pure_line == '~h "{}"'.format(hmm_name) or len(hmmdef) > 0:
                hmmdef.append(line)
            
    if len(hmmdef) == 0 or hmmdef[-1].strip() != '<ENDHMM>':
        return None
    return hmmdef

def clone_hmmdef(src_file, dst_file, src_name, dst_name):
    hmmdef = read_hmmdef(src_file, src_name)
    if hmmdef is None:
        return 0
    hmmdef[0] = '~h "{}"\n'.format(dst_name)
    with open(dst_file, 'w') as f:
        f.writelines(hmmdef)
    return len(hmmdef)

def _parse_args():
    parser = argparse.ArgumentParser(
        description='clone a hmm defination ')

    parser.add_argument('src_file', type=str, help='path of the source hmm defination file')
    parser.add_argument('dst_file', type=str, help='path of the dstination hmm definationn file')
    parser.add_argument('src_name', type=str, help='name of the source hmm')
    parser.add_argument('dst_name', type=str, help='name of the dstination hmm')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    line_num = clone_hmmdef(args.src_file, args.dst_file, args.src_name, args.dst_name)

    logging.info('{} lines copied.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()