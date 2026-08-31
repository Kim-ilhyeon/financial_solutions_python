"""
    csv데이터를 읽어오는 함수
"""

import pandas as pd

from _config import path, ENCODING

def load_prices():
    return pd.read_csv(path("prices.csv"), encoding=ENCODING, parse_dates=["date"])

def load_companies(raw=False):
    # companies.csv -> 정제본, 결측0
    # raw-companies.csv -> 오염본(공백, 전각, 대소문자, 중복) 조금 있음

    if  raw:
        # raw가 True면 오염본이 전달되도록 -> 읽어올 때 적힌 그대로 읽어올 수 있도록
        # dtype=str : 모든 값을 문자열로 반환
        # keep_default_na=False : 빈칸을 NaN으로 변경하지 말고, ''로 그대로 둬
        return pd.read_csv(
            path("raw-companies.csv"),
            encoding=ENCODING,
            dtype=str,
            keep_default_na=False
        )
    return pd.read_csv(path("companies.csv"), encoding=ENCODING)

def load_sectors():
    """ 종목 섹터데이터(10행) """
    return pd.read_csv(path("sectors.csv"), encoding=ENCODING)

def load_financial():
    """ 분기 재무 데이터 종목(120)당 12분기 = 1440행 """
    return pd.read_csv(path("financial.csv"), encoding=ENCODING)


def load_merged():
    prices = load_prices()
    companies = load_companies()
    sectors = load_sectors().rename(columns={"code": "sectorCode", "name": "sector"})
    full = (
        prices
        .merge(companies[["code", "name", "sectorCode", "market"]]
               , on="code", how="left", validate="many_to_one")
        # sectors의 code/name은 companies의 code/name과 겹친다.
        .merge(sectors[["sectorCode", "sector"]]
               , on="sectorCode", how="left", validate="many_to_one")
    )

    return full.sort_values(["code", "date"]).reset_index(drop=True)
