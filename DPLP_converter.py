#!/usr/bin/python3
#-*- coding:utf8 -*-
###############################
# Author: GajanLee
# Mail: lee_jiazh@163.com
# Created Time: 2019-04-03 19:48:22
###############################

import gzip
import re

from dplp.evalparser import *
from utils import *

class DataConstructor:

    def __init__(self, base_path):
        self.preprocess_data()
        self.segement_and_parsing()

# convert edu_ids to edu_text
def extract_edu_text(words, edu_ids):
    return [" ".join([words[id] for id in edu_id]) for edu_id in edu_ids]


from collections import namedtuple
Relation = namedtuple("EDU", ["nucleus_content", "nucleus_relation", 
                            "satellite_content", "satellite_relation",
                            "relation"])


class DocRst:
    def __init__(self, merge_path, brackets_path):
        assert merge_path.endswith(".merge")
        assert brackets_path.endswith(".brackets")

        edus = []
        with open(merge_path) as merge_file:
            for line in filter(lambda line: not is_null_line(line), merge_file):
                _, _, token, *_, edu_id = line.strip().split("\t")
                edu_id = int(edu_id) - 1
                if edu_id >= len(edus):
                    edus.append([])
                edus[edu_id].append(token)

        contents = [None]*len(edus); relations = []
        with open(brackets_path) as brackets_file:
            for line in filter(lambda line: not is_null_line(line), brackets_file):
                result = re.match(r"\(\((.*), (.*)\), '(.*)', '(.*)'\)\n", line)
                edu_nucleus_id, edu_satellite_id, attribution, relation = result.groups()
                edu_nucleus_id, edu_satellite_id = int(edu_nucleus_id)-1, int(edu_satellite_id)-1

                # TODO: construct edu tree
                if edu_nucleus_id == edu_satellite_id:
                    contents[int(edu_nucleus_id)] = (attribution, relation)
                else:
                    relations.append((edu_nucleus_id, edu_satellite_id, relation))
        
        print(contents)
        print(relations)

        keep_relations = ["cause"]
        summary = []
        drop_texts = []

        for i, content in enumerate(contents):
            edu_type, edu_relation = content
            if edu_type == "Satellite" and edu_relation not in keep_relations:
                drop_texts.append(edus[i])
                continue
            summary.append(edus[i])
        print(summary)
        
        


DocRst("data/test.txt.merge", "data/test.txt.brackets")
