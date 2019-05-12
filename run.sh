#!/usr/bin/env bash

exp=exp
data=data
log=log

if [ ! -d $exp ]; then mkdir -p $exp || exit 1; fi
if [ ! -d $log ]; then mkdir -p $log || exit 1; fi
#<< COMMENT
# create transcription file for training set.
python gen_trans.py $data/train $exp/train_trans || exit 1

# extract wordlist from training transcriptions.
python extract_words.py $exp/train_trans $exp/train_wlist || exit 1

# make timit dict to htk format.
python format_dict.py timitdic.txt $exp/timit_dic || exit 1


# check dict and make monophones. 
#if [ ! -d $exp/ded ]; then mkdir -p $exp/ded || exit 1; fi
#$echo IR > $exp/ded/timit_dic.ded

HDMan -D -A -T 1 -m -e ded -w $exp/train_wlist -n $exp/monophones -l $log/dlog $exp/dict $exp/timit_dic || exit 1

echo sil >> $exp/monophones

# create mlf file.
python trans2mlf.py $exp/train_trans $exp/train_mlf || exit 1

HLEd -D -A -T 1 -l '*' -d $exp/dict -i $exp/train_phone_mlf ded/mkphone.led $exp/train_mlf || exit 1

if [ ! -d $exp/feat ]; then mkdir -p $exp/feat || exit 1; fi
python gen_feat_scp.py $data/train $exp/feat $exp/train_feat_scp || exit 1

HCopy -D -A -T 1 -C config/hcopy.conf -S exp/train_feat_scp

awk '{print $2}' $exp/train_feat_scp > $exp/train_scp
HCompV -D -A -T 1 -C config/hcompv.conf -f 0.01 -m -S $exp/train_scp -M hmm/0 hmm/proto
#COMMENT
python gen_hmmdefs.py hmm/0/proto $exp/monophones hmm/0/hmmdefs

HERest -D -A -T 1 -C config/hcompv.conf -I exp/train_phone_mlf -t 250 150 1000 -S exp/train_scp -H hmm/0/macros -H hmm/0/hmmdefs  -M hmm/1 exp/monophones


