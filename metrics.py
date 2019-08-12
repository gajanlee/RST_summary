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
    2. Rouge-*
    3. Human-readable
    4. Flesch Readability Score
"""

import textstat
import re
import string

from functools import partial
from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

def tokenize_and_normalize(sentence : str):
    sentence = word_tokenize(sentence)
    # Remove the punctuations will influence Flesch score and textrank algorithm.
    return sentence

def bleu_score(reference : str, candidate : str):
    reference = tokenize_and_normalize(reference)
    candidate = tokenize_and_normalize(candidate)

    return sentence_bleu([reference], candidate)


def rouge_score(reference, hypothesis, rouge_type : str):
    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference)

    # rouge-1, rouge-2, rouge-l
    # "r", "p", "f"
    #print(scores)
    return scores[0][f"rouge-{rouge_type}"]["r"]

rouge_1_score = partial(rouge_score, rouge_type="1")
rouge_2_score = partial(rouge_score, rouge_type="2")
rouge_l_score = partial(rouge_score, rouge_type="l")

def word_count(sentence : str):
    sentence = re.sub(f"[{string.punctuation}]+", " ", sentence)
    return len(list(filter(lambda x: x != "", sentence.split(" "))))


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