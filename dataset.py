#!/usr/bin/python3
#-*- coding:utf8 -*-
###############################
# Author: GajanLee
# Mail: lee_jiazh@163.com
# Created Time: 2019-04-03 19:58:14
###############################

"""
Adaptive the summary dataset to alogrithms required.
"""

import gzip
import os
import sys
from _pickle import load
from discoseg import buildedu
from dplp.evalparser import evalparser
from xmlreader import reader, writer, combine

class CoreNlpDataset:

    def __init__(self, base_path="data"):
        self.java_path = "/home/lee/Programs/jdk1.8.0_161/bin/java"
        self.corenlp_path = "/home/lee/Programs/stanford-corenlp-full-2018-10-05"
        self.base_path = base_path
    
    def build(self):
        #self.generate_features()
        #self.convert_conll()
        #self.segment()
        self.rst_parsing()

    def generate_features(self):
        # use java corenlp to generate xml features file
        cmd = f"/bin/sh corenlp.sh {self.java_path} {self.corenlp_path} {self.base_path}"
        print(cmd) 
        os.system(cmd)
    
    def convert_conll(self):
        # generate conll file
        def extract_content(xml_file):
            sentlist, constlist = reader(xml_file)
            sentlist = combine(sentlist, constlist)
            conll_file = xml_file.replace(".xml", ".conll")
            writer(sentlist, conll_file)
        
        xml_files = [os.path.join(self.base_path, name) 
            for name in os.listdir(self.base_path) if name.endswith(".xml")]
        list(map(extract_content, xml_files))

    def segment(self):
        # generate merge file
        model_file = "discoseg/pretrained/model.pickle.gz"
        vocab_file = "discoseg/pretrained/vocab.pickle.gz"
        buildedu.main(model_file, vocab_file, self.base_path, self.base_path)

    def rst_parsing(self):
        # generate brackets file
        model_file = "dplp/resources/bc3200.pickle.gz"
        with gzip.open(model_file) as fin:
            print('Load Brown clusters for creating features ...')
            bcvocab = load(fin, encoding='iso-8859-1')
        evalparser(path=self.base_path, report=False, draw=True,
                bcvocab=bcvocab, withdp=False)


CoreNlpDataset().build()