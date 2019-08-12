#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   process_xhtml.py
@Time    :   2019/07/23 15:56:36
@Author  :   gajanlee 
@Version :   1.0
@Contact :   lee_jiazh@163.com
@Desc    :   Convert the acl2014 dataset from xhtml to raw text.
'''

import re
from collections import namedtuple
from lxml import etree
from pathlib import Path

Paper = namedtuple("Paper", ["origin_name", "title", "abstract", "introduction", "sections", "conclusion"])
Section = namedtuple("Section", ["title", "content"])

def normalize_xpath_result(result):
    assert type(result) is list

    def drop_chars(string):
        if string in "[]()\n*" or string.isdigit():
            return False
        return True
    return "".join(filter(drop_chars, result)).replace("\n", " ")


def extract_doc(xhtml : str, fname : str):
    text_tree = etree.HTML(xhtml.encode())

    paper_title = normalize_xpath_result(text_tree.xpath("//h1[@class='ltx_title ltx_title_document']//text()"))
    abstract = normalize_xpath_result(text_tree.xpath("//div[@class='ltx_abstract']//p//text()"))
    section_titles = text_tree.xpath("//div[@class='ltx_section']//h2[contains(@class, 'ltx_title_section')]/text()")
    # print(section_titles)
    section_contents = []

    for i, title in enumerate(section_titles, 1):
        content = normalize_xpath_result(text_tree.xpath(f"//div[@id='S{i}']//div//text()"))
        if re.match(".*(introduction|motivation).*", title.lower()):
            introduction = Section(title, content)
        elif re.match(".*(conclusion|looking ahead|discussion|summary).*", title.lower()):
            conclusion = Section(title, content)
        elif "acknowledge" in title.lower() or "reference" in title.lower():
            continue
        else:
            section_contents.append(Section(title, content))
    
    # For ACL2014, it's testing ok.
    if "conclusion" not in locals():
        conclusion = Section("Conclusion", "")
    if "introduction" not in locals():
        introduction = Section("Introduction", "")
    
    return Paper(fname, paper_title, abstract, introduction, section_contents, conclusion)


def get_all_papers(base_path="acl2014"):
    return list(map(
        lambda fpath: extract_doc(fpath.read_text(), fpath.name),
        Path(base_path).glob("*.xhtml")))


def create_dataset(xhtml_path="acl2014"):
    def mkdir(path : Path):
        path.mkdir(parents=True, exist_ok=True)
    # create dir
    path = Path(f"data/{xhtml_path}")
    mkdir(path)

    abstract_path = path / "abstract"
    content_path = path / "content"
    rst_path = path / "rst"
    list(map(mkdir, (abstract_path, content_path, rst_path)))
    
    for i, paper in enumerate(get_all_papers(xhtml_path), 1):
        paper_content_path = content_path / f"{i}.{paper.origin_name}.txt"
        paper_abstract_path = abstract_path / f"{i}.{paper.origin_name}.txt"

        paper_content = (paper.introduction.content + "\n" + 
                        "\n".join(section.content for section in paper.sections) + "\n" + 
                        paper.conclusion.content)

        paper_content_path.write_text(paper_content)
        paper_abstract_path.write_text(paper.abstract)

        print(f"{i} {paper.title} {paper.origin_name} process done")

create_dataset("acl2014")

#get_all_papers()
#print(extract_doc("acl2014/P14-2133.xhtml"))