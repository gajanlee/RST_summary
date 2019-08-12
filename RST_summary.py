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
from pathlib import Path
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

        self.edus = edus
        self.contents = contents
        self.relations = relations



def rst_summary(doc_rst : DocRst):
    nucleus_drop_relations = ["elaboration", "list", "same_unit", "textualorganization", "attribution","restatement", "means"]
    satellite_keep_relations = ["cause", "purpose", "contrast", "topic"]
    summary = []
    drop_texts = []

    # TODO: consider the relations
    relations = set()
    for i, content in enumerate(doc_rst.contents):
        edu_type, edu_relation = content

        ### --- 
        relations.add(edu_relation)

        ### ---

        if (edu_type == "Nucleus" and edu_relation in nucleus_drop_relations) or (edu_type == "Satellite" and edu_relation not in satellite_keep_relations):
            drop_texts.append(doc_rst.edus[i])
            continue
        summary.append(doc_rst.edus[i])

    result_summary = ". ".join(map(lambda words: " ".join(words), summary))+"."

    print(relations)
    return result_summary
        

def write_rst_summary():
    for merge_path in Path("data/acl2014/rst").glob("*.merge"):
        _, *paper_name, _ = merge_path.name.split(".")
        paper_name = ".".join(paper_name)

        merge_path = str(merge_path)
        bracket_path = merge_path.replace(".merge", ".brackets")

        doc = DocRst(merge_path, bracket_path)
        Path(f"data/acl2014/summary/{paper_name}.rst").write_text(rst_summary(doc))


if __name__ == "__main__":
    write_rst_summary()