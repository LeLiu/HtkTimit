#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os
import argparse
import logging
import util

def make_feat_dirs(feat_path_list):
    feat_dirs = map(lambda x: os.path.dirname(x), feat_path_list)
    feat_dirs = set(feat_dirs)
    for fd in feat_dirs:
        os.makedirs(fd, exist_ok=True)
    return len(feat_dirs)

def gen_feat_scp(wave_dir, feat_dir, feat_scp):
    wave_list = util.gen_path_list(wave_dir, ext='.wav')
    feat_list = list(map(lambda x : x.replace(wave_dir, feat_dir, 1).replace('.wav', '.feat'), wave_list))
    make_feat_dirs(feat_list)
    wave_feat_dict = dict(zip(wave_list, feat_list))

    return util.write_dict(wave_feat_dict, feat_scp)

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