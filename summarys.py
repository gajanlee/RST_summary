#!/usr/bin/python3
#-*- coding:utf8 -*-
###############################
# Author: GajanLee
# Mail: lee_jiazh@163.com
# Created Time: 2019-04-03 19:57:07
###############################

"""
Textrank Summary, it is used to compare with RST result.
"""

from summa import summarizer

def textrank_summary(text : str):
    return summarizer.summarize(text, ratio=0.05)


def textrank_summary_test():
    text = """Automatic summarization is the process of reducing a text document with a \
    computer program in order to create a summary that retains the most important points \
    of the original document. As the problem of information overload has grown, and as \
    the quantity of data has increased, so has interest in automatic summarization. \
    Technologies that can make a coherent summary take into account variables such as \
    length, writing style and syntax. An example of the use of summarization technology \
    is search engines such as Google. Document summarization is another."""


    from metrics import flesch_reading_score
    print(flesch_reading_score(text))
    print(flesch_reading_score(textrank_summary(text)))

if __name__ == "__main__":
    textrank_summary_test()