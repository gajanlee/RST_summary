#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2019/07/22 21:09:50
@Author  :   gajanlee 
@Version :   1.0
@Contact :   lee_jiazh@163.com
@Desc    :   None
'''

import logging

# level: DEBUG / INFO / WARNING / ERROR / CRITICAL
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


info_log = logging.info

error_log = logging.error

def is_null_line(line):
    return (line == "\n") or (not line)