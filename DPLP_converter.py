#!/usr/bin/python3
#-*- coding:utf8 -*-
###############################
# Author: GajanLee
# Mail: lee_jiazh@163.com
# Created Time: 2019-04-03 19:48:22
###############################

class Parser:
    parseModel = ParsingModel(withdp=False, fdpvocab=None, fprojmat=None)
    parseModel.loadmodel("model/parsing-model.pickle.gz")
    with gzip.open("resources/bc3200.pickle.gz") as fin:
        bcvocab = load(fin)
    
    @classmethod
    def convert_rst(cls, reader):
        return cls.parseModel.sr_parse(reader, cls.bcvocab)

# convert edu_ids to edu_text
def extract_edu_text(words, edu_ids):
    return [" ".join([words[id] for id in edu_id]) for edu_id in edu_ids]

class DocRst:
    def __init__(self, doc_path):
        assert doc.endswith(".merge")
        reader = DocReader().read(doc_path)
        self.rst = Parser.convert_rst(reader)
        
        self.words = [token.word for token in reader.tokendict.values()]
        self.edu_texts = extract_edu_text(self.words, self.rst.getedutext())
        self.bracketing = self.rst.bracketing()
        
        self.construct_edu_property()
        
    def construct_edu_property(self):
        self.edu_props = {}; 
        self.combinations = {}
        for bracket in self.bracketing:
            # e.g.: ((1, 1), 'Nucleus', 'span')
            (nucleus, satellite), role, relation = bracket
            if nucleus == satellite:
                self.edu_props[nucleus] = (nucleus, self.edu_texts[nucleus-1], role, relation)
            else:
                self.combinations[nucleus] = (nucleus, satellite, " ".join(self.edu_texts[nucleus], self.edu_texts[satellite]), relation)
    
    def print_rst(self):
        pass


