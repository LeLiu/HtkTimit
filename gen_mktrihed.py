#!/usr/bin/env python

import argparse
import logging

def gen_mktri_hed(monolist, trilist, mktrihed):    
    hedf = open(mktrihed, 'w')
    mp_num = 0
    hedf.write('CL {}\n'.format(trilist))
    with open(monolist) as mf:
        for mp in mf:
            mp = mp.strip()
            if not mp:
                continue
            hedf.write('TI T_{0} {{(*-{0}+*,{0}+*, *-{0}).transP}}\n'.format(mp))
            mp_num += 1
    hedf.close()
    return mp_num
            

def _parse_args():
    parser = argparse.ArgumentParser(description=
        'generate the mktri (make triphone list from monophone list) hed file')

    parser.add_argument('monolist', type=str, help='the monophone list file path (relative to the output "maketrihed" path)')
    parser.add_argument('trilist', type=str, help='the triphone list file path')
    parser.add_argument('mktrihed', type=str, help='the output "mktrihed" file path')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    mp_num = gen_mktri_hed(args.monolist, args.trilist, args.mktrihed)

    logging.info('{} monophones found.'.format(mp_num))
    return 0

if __name__ == '__main__':
    _main()