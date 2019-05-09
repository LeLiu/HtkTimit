#!/usr/bin/env bash

exp=exp
data=data
log=log

if [ ! -d $exp ]; then mkdir -p $exp || exit 1; fi
if [ ! -d $log ]; then mkdir -p $log || exit 1; fi


# create transcription file for training set.
python gen_trans.py $data/train $exp/train_trans || exit 1

# extract wordlist from training transcriptions.
python extract_words.py $exp/train_trans $exp/train_wlist || exit 1

# make timit dict to htk format.
python format_dict.py $data/doc/timitdic.txt $exp/timit_dic || exit 1

# check dict and make monophones. 
if [ ! -d $exp/ded ]; then mkdir -p $exp/ded || exit 1; fi
echo IR > $exp/ded/timit_dic.ded

HDMan -m -e $exp/ded -w $exp/train_wlist -n $exp/monophones -l $log/dlog $exp/dict $exp/timit_dic || exit 1

# create mlf file.
python trans2mlf.py $exp/train_trans $exp/train_mlf || exit 1

if [! -d $exp/feat ]; then mkdir -p $exp/feat || exit 1; fi


