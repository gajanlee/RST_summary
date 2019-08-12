#!/usr/bin/python3
#-*- coding:utf8 -*-
###############################
# Author: GajanLee
# Mail: lee_jiazh@163.com
# Created Time: 2019-04-03 19:58:14
###############################

"""
Adaptive the summary dataset to alogrithms required.
Convert the raw document to RST format by DPLP.
"""

import gzip
import os
import sys
from _pickle import load
from discoseg import buildedu
from dplp.evalparser import evalparser
from functools import wraps
from utils import *
from xmlreader import reader, writer, combine


def kill_fail_pipeline(func):

    @wraps(func)
    def wrap_func(*args, **kwargs):
        status = func(*args, **kwargs)
        if not status:
            error_log(f"function {func.__name__} exectutes failure.")
            exit(1)

    return wrap_func

class CoreNlpDataset:

    def __init__(self, input_path, rst_path="rst"):
        self.input_path = input_path
        self.rst_path = rst_path
        
        self.java_path = "/home/lee/Programs/jdk1.8.0_161/bin/java"
        self.corenlp_path = "/home/lee/Programs/stanford-corenlp-full-2018-10-05"
    
    def build(self):
        #self.generate_features()
        #self.convert_conll()
        #self.segment()
        self.rst_parsing()

    @kill_fail_pipeline
    def generate_features(self):
        # use java corenlp to generate xml features file
        cmd = f"/bin/sh corenlp.sh {self.java_path} {self.corenlp_path} {self.input_path} {self.rst_path}"
        info_log(cmd)
        code = os.system(cmd)
        if code != 0: 
            return False
        return True

    @kill_fail_pipeline
    def convert_conll(self):
        # generate conll file
        def extract_content(xml_file):
            info_log(f"convert conll file {xml_file}")
            sentlist, constlist = reader(xml_file)
            sentlist = combine(sentlist, constlist)
            conll_file = xml_file.replace(".xml", ".conll")
            writer(sentlist, conll_file)
        
        xml_files = [os.path.join(self.rst_path, name) 
            for name in os.listdir(self.rst_path) if name.endswith(".xml")]
        list(map(extract_content, xml_files))
        return True

    @kill_fail_pipeline
    def segment(self):
        info_log("segmenting")
        # generate merge file
        model_file = "discoseg/pretrained/model.pickle.gz"
        vocab_file = "discoseg/pretrained/vocab.pickle.gz"
        buildedu.main(model_file, vocab_file, self.rst_path, self.rst_path)
        return True

    @kill_fail_pipeline
    def rst_parsing(self):
        # generate brackets file
        model_file = "dplp/resources/bc3200.pickle.gz"
        with gzip.open(model_file) as fin:
            info_log('Load Brown clusters for creating features ...')
            bcvocab = load(fin, encoding='iso-8859-1')
        info_log("rst_parsing")
        evalparser(path=self.rst_path, report=False, draw=False,
                bcvocab=bcvocab, withdp=False)
        return True


CoreNlpDataset("data/acl2014/content", "data/acl2014/rst").build()
#CoreNlpDataset("data/test/content", "data/test/rst").build()
