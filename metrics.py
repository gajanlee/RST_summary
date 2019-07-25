#!/usr/bin/python3
#-*- coding:utf8 -*-
###############################
# Author: GajanLee
# Mail: lee_jiazh@163.com
# Created Time: 2019-04-03 19:57:29
###############################

"""
Evaluation Metrics:
    1. BLEU
    2. Rouge-L
    3. Human-readable
    4. Flesch Readability Score
"""


from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu

import textstat

def tokenize_and_normalize(sentence : str):
    sentence = word_tokenize(sentence)
    # TODO: Remove the punctuations
    return sentence

def belu_score(reference : str, candidate : str):
    reference = tokenize_and_normalize(reference)
    candidate = tokenize_and_normalize(candidate)

    return sentence_bleu([reference], candidate)
    

def flesch_reading_score(sentence : str):
    """
    Score:
    90-100, easily understood by an average 11-year old student
    60-70 , easily understood by 13-15-year-old students
    0 -30 , best understood by university graduates

    Punctuations:
    It could influence the count of sentences.
    `sentences = re.split(r' *[\.\?!][\'"\)\]]*[ |\n](?=[A-Z])', text)`
    """
    return textstat.flesch_reading_ease(sentence)