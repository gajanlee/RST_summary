#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2019/07/29 11:07:49
@Author  :   gajanlee 
@Version :   1.0
@Contact :   lee_jiazh@163.com
@Desc    :   None
'''

from cmy_summary import get_cmy_summary
from sxp_summary import get_sxp_summary
from functools import partial
from pathlib import Path
from prettytable import PrettyTable
from summarys import textrank_summary
from metrics import rouge_1_score, rouge_2_score, rouge_l_score,  bleu_score, flesch_reading_score, word_count


def test():
    test_doc = DocRst("data/test/rst/1.P14-2016.xhtml.txt.merge", "data/test/rst/1.P14-2016.xhtml.txt.brackets")

    rst_result_summary = summary(test_doc)
    paper_abstract = Path("data/test/abstract/1.P14-2016.xhtml.txt").read_text()
    paper_content = Path("data/test/content/1.P14-2016.xhtml.txt").read_text()

    tr_result_summary = textrank_summary(paper_content)

    #print(tr_result_summary)
    #print(rst_result_summary)

    print(f"rst bleu score is {bleu_score(paper_abstract, rst_result_summary)}")
    print(f"tr bleu score is {bleu_score(paper_abstract, tr_result_summary)}")

    print(f"rst flesc score is {flesch_reading_score(rst_result_summary)}")
    print(f"tr flesc score is {flesch_reading_score(tr_result_summary)}")

    print(f"origin abstract flesc score is {flesch_reading_score(paper_abstract)}")
    print(f"origin paper flesc score is {flesch_reading_score(paper_content)}")


def get_paper_name_from_rst(rst_path_name):
    *name, txt, rst = rst_path_name.split(".")

    return ".".join(name)

def get_full_text(paper_name):
    return list(Path(f"data/acl2014/content").glob(f"*.{paper_name}.txt"))[0].read_text()
    

def get_truth_abstract(paper_name):
    return list(Path(f"data/acl2014/abstract").glob(f"*.{paper_name}.txt"))[0].read_text()

def main():
    #truth_len = rst_len = tr_len = cmy_len = sxp_len = 0
    #truth_len_count = rst_len_count = tr_len_count = cmy_len_count = sxp_len_count = 0
    #rst_rouge_score = tr_rouge_score = cmy_rouge_score = sxp_rouge_score = 0
    #rst_rouge_2_score = tr_rouge_2_score = cmy_rouge_2_score = sxp_rouge_2_score = 0
    #rst_rouge_l_score = tr_rouge_l_score = cmy_rouge_l_score = sxp_rouge_l_score = 0
    #rst_bleu_score = tr_bleu_score = cmy_bleu_score = sxp_bleu_score = 0


    paper_counts = []
    abstract_counts = []
    rst_counts = []
    rst_rates = []

    rst_lens, tr_lens, cmy_lens, sxp_lens = [[] for _ in range(4)]
    text_rouge1s, rst_rouge1s, tr_rouge1s, cmy_rouge1s, sxp_rouge1s = [[] for _ in range(5)]
    text_rouge2s, rst_rouge2s, tr_rouge2s, cmy_rouge2s, sxp_rouge2s = [[] for _ in range(5)]
    text_rougels, rst_rougels, tr_rougels, cmy_rougels, sxp_rougels = [[] for _ in range(5)]



    '''min_paper_count = max_paper_count = mean_paper_count = 0
    min_abstract_count = max_abstract_count = mean_abstract_count = 0
    min_rst_count = max_rst_count = mean_rst_count = 0
    min_rst_rate = max_rst_rate = mean_rst_rate = 0'''


    for i, rst_summary_path in enumerate(Path("data/acl2014/summary").glob("*")):
        
        #if i == 10: break

        paper_name = get_paper_name_from_rst(rst_summary_path.name)

        paper_content = get_full_text(paper_name)

        truth_summary = get_truth_abstract(paper_name)
        rst_summary = rst_summary_path.read_text()
        tr_summary = textrank_summary(rst_summary)
        cmy_summary = get_cmy_summary(paper_name, 78)
        sxp_summary = get_sxp_summary(paper_name, "01")

        paper_word_count = word_count(paper_content)
        paper_abstract_count = word_count(truth_summary)
        rst_summary_word_count = word_count(rst_summary)
        rst_rate = rst_summary_word_count / paper_word_count

        paper_counts.append(paper_word_count)
        abstract_counts.append(paper_abstract_count)
        rst_counts.append(rst_summary_word_count)
        rst_rates.append(rst_rate)

        rst_lens.append(rst_summary_word_count)
        tr_lens.append(word_count(tr_summary))
        cmy_lens.append(word_count(cmy_summary))
        sxp_lens.append(word_count(sxp_summary))

        text_rouge1s.append(rouge_1_score(truth_summary, paper_content))
        rst_rouge1s.append(rouge_1_score(truth_summary, rst_summary))
        tr_rouge1s.append(rouge_1_score(truth_summary, tr_summary))
        cmy_rouge1s.append(rouge_1_score(truth_summary, cmy_summary))
        sxp_rouge1s.append(rouge_1_score(truth_summary, sxp_summary))

        text_rouge2s.append(rouge_2_score(truth_summary, paper_content))
        rst_rouge2s.append(rouge_2_score(truth_summary, rst_summary))
        tr_rouge2s.append(rouge_2_score(truth_summary, tr_summary))
        cmy_rouge2s.append(rouge_2_score(truth_summary, cmy_summary))
        sxp_rouge2s.append(rouge_2_score(truth_summary, sxp_summary))

        text_rougels.append(rouge_l_score(truth_summary, paper_content))
        rst_rougels.append(rouge_l_score(truth_summary, rst_summary))
        tr_rougels.append(rouge_l_score(truth_summary, tr_summary))
        cmy_rougels.append(rouge_l_score(truth_summary, cmy_summary))
        sxp_rougels.append(rouge_l_score(truth_summary, sxp_summary))

        '''min_paper_count = paper_word_count if min_paper_count == 0 or paper_word_count < min_paper_count else min_paper_count
        max_paper_count = max(max_paper_count, paper_word_count)
        mean_paper_count += paper_word_count

        min_abstract_count = paper_abstract_count if min_abstract_count == 0 or paper_abstract_count < min_abstract_count else min_abstract_count
        max_abstract_count = max(max_abstract_count, paper_abstract_count)
        mean_abstract_count += paper_abstract_count

        min_rst_count = rst_summary_word_count if min_rst_count == 0 or rst_summary_word_count < min_rst_count else min_rst_count
        max_rst_count = max(max_rst_count, rst_summary_word_count)
        mean_rst_count += rst_summary_word_count

        min_rst_rate = rst_rate if min_rst_rate == 0 or rst_rate < min_rst_rate else rst_rate
        max_rst_rate = max(max_rst_rate, rst_rate)
        mean_rst_rate += rst_rate'''


        '''truth_len += len(truth_summary)
        rst_len += len(rst_summary)
        tr_len += len(tr_summary)
        cmy_len += len(cmy_summary)
        sxp_len += len(sxp_summary)

        truth_len_count += word_count(truth_summary)
        rst_len_count += word_count(rst_summary)
        tr_len_count += word_count(tr_summary)
        cmy_len_count += word_count(cmy_summary)
        sxp_len_count += word_count(sxp_summary)'''

        '''#print(sxp_len, tr_len)
        print(rouge_1_score(truth_summary, rst_summary))
        print(rouge_1_score(truth_summary, tr_summary))
        print(rouge_1_score(truth_summary, cmy_summary))
        print(rouge_1_score(truth_summary, sxp_summary))

        print(rst_summary)
        print(truth_summary)


        if i == 2: exit()'''
        
        '''rst_rouge_score += rouge_1_score(truth_summary, rst_summary)
        tr_rouge_score += rouge_1_score(truth_summary, tr_summary)
        cmy_rouge_score += rouge_1_score(truth_summary, cmy_summary)
        sxp_rouge_score += rouge_1_score(truth_summary, sxp_summary)

        rst_rouge_2_score += rouge_2_score(truth_summary, rst_summary)
        tr_rouge_2_score += rouge_2_score(truth_summary, tr_summary)
        cmy_rouge_2_score += rouge_2_score(truth_summary, cmy_summary)
        sxp_rouge_2_score += rouge_2_score(truth_summary, sxp_summary)

        rst_rouge_l_score += rouge_l_score(truth_summary, rst_summary)
        tr_rouge_l_score += rouge_l_score(truth_summary, tr_summary)
        cmy_rouge_l_score += rouge_l_score(truth_summary, cmy_summary)
        sxp_rouge_l_score += rouge_l_score(truth_summary, sxp_summary)

        bleu_scores = list(map(partial(bleu_score, truth_summary), [rst_summary, tr_summary, cmy_summary, sxp_summary]))
        
        rst_bleu_score += bleu_scores[0]
        tr_bleu_score += bleu_scores[1]
        cmy_bleu_score += bleu_scores[2]
        sxp_bleu_score += bleu_scores[3]'''

        #rst_bleu_score, tr_bleu_score, cmy_bleu_score, sxp_bleu_score = map(lambda s1: print(s1), zip([rst_bleu_score, tr_bleu_score, cmy_bleu_score, sxp_bleu_score], bleu_scores))

        if i % 5 == 0: print(f"{i} / 173"); #break
        
        if i == 300: 
            print(rst_summary_path)
            print("truth summary: ========================")
            print(truth_summary)
            print(" summary: ========================")
            print(tr_summary)
            print("cmy summary: =======================")
            print(cmy_summary)
            print("sxp summary: =======================")
            print(sxp_summary)
            exit()


    mean = lambda data: round(sum(data) / len(data), 4)
    stat = lambda data: (round(min(data), 4), round(max(data), 4), round(mean(data), 4))

    t = PrettyTable(['name', 'min', 'max', 'mean'])
    t.add_row(['truth_len', *stat(paper_counts)])
    t.add_row(['abstract_count', *stat(abstract_counts)])
    t.add_row(['rst_len', *stat(rst_lens)])
    t.add_row(['rst_rate', *stat(rst_rates)])
    t.add_row(['tr_len', *stat(tr_lens)])
    t.add_row(['cmy_len', *stat(cmy_lens)])
    t.add_row(['sxp_len', *stat(sxp_lens)])

    '''t.add_row(['truth_word_count', *stat(paper_counts)])
    t.add_row(['rst_word_count', rst_len_count / 173])
    t.add_row(['tr_word_count', tr_len_count / 173])
    t.add_row(['cmy_word_count', cmy_len_count / 173])
    t.add_row(['sxp_word_count', sxp_len_count / 173])'''

    t.add_row(['text_rouge1', *stat(text_rouge1s)])
    t.add_row(['rst_rouge1', *stat(rst_rouge1s)])
    t.add_row(['tr_rouge1', *stat(tr_rouge1s)])
    t.add_row(['cmy_rouge1', *stat(cmy_rouge1s)])
    t.add_row(['sxp_rouge1', *stat(sxp_rouge1s)])

    t.add_row(['text_rouge2', *stat(text_rouge2s)])
    t.add_row(['rst_rouge2', *stat(rst_rouge2s)])
    t.add_row(['tr_rouge2', *stat(tr_rouge2s)])
    t.add_row(['cmy_rouge2', *stat(cmy_rouge2s)])
    t.add_row(['sxp_rouge2', *stat(sxp_rouge2s)])

    t.add_row(['text_rougel', *stat(text_rougels)])
    t.add_row(['rst_rougel', *stat(rst_rougels)])
    t.add_row(['tr_rougel', *stat(tr_rougels)])
    t.add_row(['cmy_rougel', *stat(cmy_rougels)])
    t.add_row(['sxp_rougel', *stat(sxp_rougels)])


    '''t.add_row(['rst_bleu', rst_bleu_score / 173])
    t.add_row(['tr_bleu', tr_bleu_score / 173])
    t.add_row(['cmy_bleu', cmy_bleu_score / 173])
    t.add_row(['sxp_bleu', sxp_bleu_score / 173])'''
    


    print(t)




main()

