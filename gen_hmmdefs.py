#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
import logging
import util

def read_hmm_proto(proto_file):
    with open(proto_file, 'r') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if line.startswith('~h'):
                macros = lines[:idx]
                proto = lines[idx:]
    return macros, proto

def clone_hmmdef(proto, hmm_name):
    hmmdef = proto[:]
    hmmdef[0] = '~h "{}"\n'.format(hmm_name)
    return hmmdef

def gen_hmmdefs(proto_file, name_list, def_file):
    macros, proto = read_hmm_proto(proto_file)
    names = util.read_list(name_list)
    hmmdefs = macros
    hmmdefs.append('\n')
    for name in names:
        hmmdef = clone_hmmdef(proto, name)
        hmmdefs.extend(hmmdef)
        hmmdefs.append('\n')
    with open(def_file, 'w') as f:
        f.writelines(hmmdefs)
    return len(names)

def _parse_args():
    parser = argparse.ArgumentParser(
        description='generate hmm definations from a hmm proto file')

    parser.add_argument('proto_file', type=str, help='the hmm proto file path')
    parser.add_argument('name_list', type=str, help='the hmm name list path')
    parser.add_argument('def_file', type=str, help='the hmm defination file path')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    hmm_num = gen_hmmdefs(args.proto_file, args.name_list, args.def_file)

    logging.info('{} hmmdefs generated.'.format(hmm_num))
    return 0

if __name__ == '__main__':
    _main()
