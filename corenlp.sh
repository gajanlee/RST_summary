#!/bin/sh
# -*- encoding: utf-8 -*-
#@File    :   corenlp.sh
#@Time    :   2019/07/22 10:10:08
#@Author  :   gajanlee 
#@Version :   1.0
#@Contact :   lee_jiazh@163.com
#@Desc    :   None


help() {
    echo "sh corenlp.sh JAVA_BIN CORENLP_DIR DATA_PATH"
    echo "Please check your parameters: $@"
}

if [ $# != 3 ]; then
    help $@
    exit 1
fi

JAVA_BIN=$1
CORENLP_DIR=$2
DATA_PATH=$3

for FNAME in $DATA_PATH/*
do
    echo $FNAME
    $JAVA_BIN -cp "$CORENLP_DIR/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -file $FNAME
    /bin/mv $(/usr/bin/basename $FNAME.xml) $DATA_PATH/
done