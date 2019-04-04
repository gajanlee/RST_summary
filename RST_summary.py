#!/usr/bin/python3
#-*- coding:utf8 -*-
###############################
# Author: GajanLee
# Mail: lee_jiazh@163.com
# Created Time: 2019-04-03 19:54:33
###############################

from DPLP_converter import DocRst

def summary(doc_path):
    rst = DocRst(doc_path)
    
    for combination in rst.combinations:
        nuc, sat, edu_text, relation = combination
        
        operation = judge_relation(relation)


def judge_relation(relation):
    pass


class Operations:
    UNKNOWN = -1
    NUCLEUS = 0
    MERGE = 1

{
    # Satellite provides additional details about the nucleus
    "elaboration": Operations.NUCLEUS,
    # No specific hierachy between EDUS
    "joint": Operations.MERGE,
    # Links parts of one EDU to another
    "sameunit": Operations.UNKNOWN
    # Satellite contains reporting verbs or cognitive predicates for nucleus
    
}
