#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sxp_summary.py
@Time    :   2019/08/09 21:35:18
@Author  :   gajanlee 
@Version :   1.0
@Contact :   lee_jiazh@163.com
@Desc    :   孙老师的摘要结果
'''


from pathlib import Path
from lxml import etree


def get_sxp_summary(filename: str, summ_type: str):
    file_path = Path(f"sxp_summary_result/acl_exc_withoutstop_topk/{filename}.html.{summ_type}")

    paper = etree.HTML(file_path.read_text())
    abstracts = paper.xpath("//a[contains(@href, '#')]/text()")
    abstract_text = " ".join(abstracts) + "."

    return abstract_text