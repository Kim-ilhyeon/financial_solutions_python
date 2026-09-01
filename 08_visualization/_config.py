"""
실습 공통 설정.
  sectors.csv        10행     섹터 마스터            (S01 ~ S10)
  companies.csv     120행     종목 마스터 (정제본)    결측 0
  prices.csv     90,000행     일별 시세 (정제본)      120종목 x 750일

"""

import os

# __file__ 은 '지금 이 파일(_config.py)의 경로' 다.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def path(name):
    """data/ 안의 파일 경로. 작은 파일 두 개는 항상 로컬에서 읽는다."""
    return os.path.join(DATA_DIR, name)


# read_csv 공통 옵션
#   encoding="utf-8-sig" : 세 파일 모두 맨 앞에 BOM 이 붙어 있다.
ENCODING = "utf-8-sig"
