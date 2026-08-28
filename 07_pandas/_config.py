"""
    실습 공통 설정, 경로
"""

import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ENCODING = "utf-8-sig"

def path(name):
    """ data/안의 파일 경로. """
    return os.path.join(DATA_DIR, name)



