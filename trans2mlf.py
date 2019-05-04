#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
import logging

def trans_line_to_mlf_lines(trans_line):
    lab_name, *words = trans_line.split()
    pattern = os.path.join(lab_name, '.lab')
    mlf_lines = [pattern]
    mlf_lines.extend(words)
    mlf_lines.extend(['.'])
    lines_str = '\n'.join([mlf_lines])
    return lines_str

def trans_to_mlf(trans_path, mlf_path):
    line_num = 0
    with open(mlf_path, 'w') as mlf_f:
        mlf_f.write('#!MLF!#\n') # MLF header
        with open(trans_path, 'r') as trans_f:
            for trans_line in trans_f:
                mlf_lines = trans_line_to_mlf_lines(trans_line)
                mlf_f.write('{}\n'.format(mlf_lines))
                line_num += 1
    return line_num

def _parse_args():
    parser = argparse.ArgumentParser(
        description='transform a global transcriptions file to MLF format')

    parser.add_argument('trans_path', type=str, help='path of the input global transcription file file')
    parser.add_argument('mlf_path', type=str, help='path of the output MLF file')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    line_num = trans_to_mlf(args.trans_path, args.mlf_path)

    logging.info('{} transcriptions processed.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()

    

        