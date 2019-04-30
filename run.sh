#!/usr/bin/env bash

. env.sh

exp = $TIMIT_WORK_ROOT/exp 
if [ ! -d $exp ]; then
    mkdir -p $exp
fi

