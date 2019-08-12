#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cmy_summary.py
@Time    :   2019/07/30 19:03:32
@Author  :   gajanlee 
@Version :   1.0
@Contact :   lee_jiazh@163.com
@Desc    :   Cao Mengyun's summary getter
'''

from pathlib import Path
from lxml import etree


def get_cmy_summary(filename: str, summ_type: str):
    file_path = Path(f"cmy_plosone_system_html/{filename}.html.{summ_type}")

    paper = etree.HTML(file_path.read_text())
    abstracts = paper.xpath("//a[contains(@href, '#')]/text()")
    abstract_text = ". ".join(abstracts) + "."

    return abstract_text



    