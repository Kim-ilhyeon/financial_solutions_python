"""
세 개 표를 읽어 오는 함수를 한자리에 모아 두었다.
여기서는 '읽기' 만 한다.
"""

import pandas as pd

from _config import path, ENCODING


def load_prices():
    """
    일별 시세 90,000행.

    parse_dates=["date"] 를 주면 '2023-09-25' 라는 글자가 아니라
    날짜 타입(datetime64)으로 읽힌다. 이게 없으면 x축이 문자열로 취급되어
    750개의 눈금이 그대로 늘어서고 정렬도 사전순이 된다. (교안 15 에서 본 그 이야기)
    """
    return pd.read_csv(path("prices.csv"), encoding=ENCODING, parse_dates=["date"])


def load_companies():
    """종목 마스터 120행. code · name · sectorCode · market 이 들어 있다. 결측 0."""
    return pd.read_csv(path("companies.csv"), encoding=ENCODING)


def load_sectors():
    """섹터 마스터 10행. code(S01...) 와 name(금융...) 이 들어 있다."""
    return pd.read_csv(path("sectors.csv"), encoding=ENCODING)
