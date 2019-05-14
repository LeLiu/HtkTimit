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

def remove_state(hmmdef, sid):
    start, end = None, None
    for idx, line in enumerate(hmmdef):
        pure_line = line.strip()
        if not pure_line:
            continue
        
        if pure_line == '<STATE> {}'.format(str(sid)):
            start = idx
        elif start is not None and (pure_line.startswith('<STATE>') or pure_line.startswith('<TRANSP>')):
            end = idx
            break
        elif pure_line.startswith('<NUMSTATES>'):
            _, num_states = pure_line.split()
            num_states = int(num_states) - 1
            hmmdef[idx] = '<NUMSTATES> {}\n'.format(str(num_states))

    if start is None or end is None:
        return None
    new_hmmdef = hmmdef[0:start]
    new_hmmdef.extend(hmmdef[end:])
    return new_hmmdef

def rename_state(hmmdef, src, dst):
    for idx, line in enumerate(hmmdef):
        pure_line = line.strip()
        if not pure_line:
            continue
        if pure_line == '<STATE> {}'.format(str(src)):
            hmmdef[idx] = '<STATE> {}\n'.format(str(dst))
    return hmmdef

def remove_transp(hmmdef, sid):
    start, end, size, transp = None, None, None, []
    for idx, line in enumerate(hmmdef):
        pure_line = line.strip()
        if not pure_line:
            continue

        if start is None and pure_line.startswith('<TRANSP>'):
            start = idx
            _, size = pure_line.split()
            size = int(size)
        elif pure_line == '<ENDHMM>':
            end = idx
            break
        elif start is not None:
            transp.append(list(pure_line.split()))
            
    if len(transp) == 0 or len(transp) != size:
        return None
    
    del(transp[sid-1])
    for row_id in range(len(transp)):
        del[transp[row_id][sid-1]]
        transp[row_id] = ' '.join(transp[row_id]) + '\n'
    
    new_hmmdef = hmmdef[0:start]
    new_hmmdef.append('<TRANSP> {}\n'.format(str(size - 1)))
    new_hmmdef.extend(transp)
    new_hmmdef.append('<ENDHMM>\n')
    return new_hmmdef

def modify_transp(hmmdef):
    start, end = None, None
    for idx, line in enumerate(hmmdef):
        pure_line = line.strip()
        if not pure_line:
            continue
        if start is None and pure_line.startswith('<TRANSP>'):
            start = idx
        elif pure_line == '<ENDHMM>':
            end = idx
            break
            
    if start is None or end is None:
        return None
    
    new_hmmdef = hmmdef[0:start]
    new_hmmdef.append('<TRANSP> {}\n'.format(str(3)))
    new_hmmdef.append('0.0 1.0 0.0\n0.0 0.7 0.3\n0.0 0.0 0.0')
    new_hmmdef.append('<ENDHMM>\n')
    return new_hmmdef

def sil2sp(src_file, dst_file):
    hmmdef = read_hmmdef(src_file, 'sil')
    if hmmdef is None:
        return 0
    hmmdef[0] = '~h "sp"\n'
    hmmdef = remove_state(hmmdef, 2)
    hmmdef = remove_state(hmmdef, 4)
    #hmmdef = remove_transp(hmmdef, 2)
    #hmmdef = remove_transp(hmmdef, 4-1)
    hmmdef = modify_transp(hmmdef)
    hmmdef = rename_state(hmmdef, 3, 2)
    with open(dst_file, 'w') as f:
        f.writelines(hmmdef)
    return len(hmmdef)

def _parse_args():
    parser = argparse.ArgumentParser(
        description='clone a hmm defination ')

    parser.add_argument('src_file', type=str, help='path of the source hmm defination file')
    parser.add_argument('dst_file', type=str, help='path of the dstination hmm definationn file')

    args = parser.parse_args()
    return args

def _main():
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO)

    line_num = sil2sp(args.src_file, args.dst_file)

    logging.info('{} lines copied.'.format(line_num))
    return 0

if __name__ == '__main__':
    _main()