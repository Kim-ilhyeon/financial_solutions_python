"""
실습 공통 설정.

  sectors.csv        10행     섹터 마스터            (S01 ~ S10)
  companies.csv     120행     종목 마스터 (정제본)    결측 0
  prices.csv     90,000행     일별 시세 (정제본)      120종목 x 750일

"""

import os

USE_REMOTE = False

BASE = "https://khlab.oneground.ai.kr"

# __file__ 은 '지금 이 파일(_config.py)의 경로' 다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")


def path(name):
    """data/ 안의 파일 경로. 작은 파일 두 개는 항상 로컬에서 읽는다."""
    return os.path.join(DATA_DIR, name)


def prices_path():
    """
    일별 시세 90,000행의 경로 또는 URL.
    """
    local = path("prices.csv")
    if not USE_REMOTE and os.path.exists(local):
        return local
    return f"{BASE}/datasets/prices.csv"


def model_path(name="model_bundle.pkl"):
    """
    models/ 안의 저장 경로. 폴더가 없으면 만든다.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    return os.path.join(MODEL_DIR, name)


# read_csv 공통 옵션
ENCODING = "utf-8-sig"
