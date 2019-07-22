#!/usr/bin/env bash

exp=exp
data=data
log=log

if [ ! -d $exp ]; then mkdir -p $exp || exit 1; fi
if [ ! -d $log ]; then mkdir -p $log || exit 1; fi
<< COMMENT
# Step 2. the Dictionary
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

# Step 4. Creating the Transcription Files
# create mlf file.
python trans2mlf.py $exp/train_trans $exp/train_mlf || exit 1

# create phone level mlf file.
HLEd -D -A -T 1 -l '*' -d $exp/dict -i $exp/train_phone_mlf ded/mkphone.led $exp/train_mlf || exit 1

# Setp 5. Coding the Data
if [ ! -d $exp/feat ]; then mkdir -p $exp/feat || exit 1; fi
python gen_feat_scp.py $data/train $exp/feat $exp/train_feat_scp || exit 1

HCopy -D -A -T 1 -C config/hcopy.conf -S exp/train_feat_scp

# Step 6 Create Flat Start Monophones
awk '{print $2}' $exp/train_feat_scp > $exp/train_scp
HCompV -D -A -T 1 -C config/hcompv.conf -f 0.01 -m -S $exp/train_scp -M hmm/0 hmm/proto

python gen_hmmdefs.py hmm/0/proto $exp/monophones hmm/0/hmmdefs

mkdir hmm/2
mkdir hmm/3
HERest -D -A -T 1 -C config/hcompv.conf -I exp/train_phone_mlf -t 250 150 1000 -S exp/train_scp -H hmm/0/macros -H hmm/0/hmmdefs  -M hmm/1 exp/monophones
HERest -D -A -T 1 -C config/hcompv.conf -I exp/train_phone_mlf -t 250 150 1000 -S exp/train_scp -H hmm/1/macros -H hmm/1/hmmdefs  -M hmm/2 exp/monophones
HERest -D -A -T 1 -C config/hcompv.conf -I exp/train_phone_mlf -t 250 150 1000 -S exp/train_scp -H hmm/2/macros -H hmm/2/hmmdefs  -M hmm/3 exp/monophones


# Step 7. Fixing the Silence Models
mkdir hmm/4
python sil2sp.py hmm/3/hmmdefs hmm/4/sp
cat hmm/3/hmmdefs hmm/4/sp > hmm/4/hmmdefs
cp hmm/3/macros hmm/4/macros

cp $exp/monophones $exp/monophones_sp
echo sp >> $exp/monophones_sp
mkdir hmm/5
HHEd -D -A -T 1 -H hmm/4/macros -H hmm/4/hmmdefs -M hmm/5 ded/sil.hed $exp/monophones_sp

mkdir hmm/6
mkdir hmm/7
HERest -D -A -T 1 -C config/hcompv.conf -I exp/train_phone_mlf -t 250 150 1000 -S exp/train_scp -H hmm/5/macros -H hmm/5/hmmdefs  -M hmm/6 exp/monophones_sp
HERest -D -A -T 1 -C config/hcompv.conf -I exp/train_phone_mlf -t 250 150 1000 -S exp/train_scp -H hmm/6/macros -H hmm/6/hmmdefs  -M hmm/7 exp/monophones_sp

# Step 8. Realing the Training Data
echo '<SIL> sil' | cat - exp/timit_dic > exp/timit_dict_sil
HVite -l '*' -o SWT -b '<SIL>' -C config/hcompv.conf -a -H hmm/7/macros -H hmm/7/hmmdefs -i exp/aligned_mlf -m -t 250 150 1000 -y lab -I exp/train_mlf -S exp/train_scp exp/timit_dict_sil exp/monophones_sp
mkdir hmm/8
mkdir hmm/9
HERest -D -A -T 1 -C config/hcompv.conf -I exp/aligned_mlf -t 250 150 1000 -S exp/train_scp -H hmm/7/macros -H hmm/7/hmmdefs  -M hmm/8 exp/monophones_sp
HERest -D -A -T 1 -C config/hcompv.conf -I exp/aligned_mlf -t 250 150 1000 -S exp/train_scp -H hmm/8/macros -H hmm/8/hmmdefs  -M hmm/9 exp/monophones_sp

COMMENT
# Step 9 Make Triphone frome Monophones

HLEd -n triphones1 -l '*' -i exp/wintri_mlf ded/mktri.led exp/aligned_mlf

# Step 10. Making Tied-State Triphones

# Step 11. Recognising the Test Data
