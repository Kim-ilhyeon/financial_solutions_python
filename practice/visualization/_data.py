"""
실습데이터 불러오기

표 세 장을 읽어 하나로 붙여 돌려준다.
이번 실습의 주제는 '그리는 것' 이라, 데이터를 만드는 부분은 여기서 끝내 두었다.

  sectors.csv        10행    섹터 마스터   code(S01~S10) · name
  companies.csv     120행    종목 마스터   code · name · sectorCode · market
  prices.csv     90,000행    일별 시세     120종목 x 750거래일
"""

import os

import pandas as pd


# 이 파일 기준으로 잡아 두면 어느 폴더에서 실행하든 data 를 찾아낸다.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

ENCODING = "utf-8-sig"

USE_REMOTE = False


def path(name):
    """data/ 안의 파일 경로"""
    return os.path.join(DATA_DIR, name)


def _read(name):
    """data/ 의 CSV 한 장을 읽는다. 없으면 어디를 찾았는지 알려 주고 멈춘다."""
    p = path(name)
    if not os.path.exists(p):
        raise SystemExit(f"실습데이터를 찾을 수 없습니다: {p}")
    return pd.read_csv(p, encoding=ENCODING)



def load_prices():
    """
    일별 시세 90,000행.
    """
    return pd.read_csv(path("prices.csv"), encoding=ENCODING, parse_dates=["date"])


def load_companies():
    """종목 마스터 120행. code · name · sectorCode · market. 결측 0."""
    return _read("companies.csv")


def load_sectors():
    """섹터 마스터 10행. code(S01...) 와 name(금융...)."""
    return _read("sectors.csv")


def load_merged():
    """
    세 장을 붙이고 일간 수익률까지 만들어 둔 90,000행짜리 표.

    Returns:
        DataFrame : 시세 9열 + name · market · sectorCode · sector + ret
    """
    prices = load_prices()
    companies = load_companies()
    # sectors 의 code/name 은 companies 의 code/name 과 이름이 겹친다.
    # 그대로 붙이면 code_x / code_y 가 되므로 미리 이름을 바꿔 둔다.
    sectors = load_sectors().rename(columns={"code": "sectorCode", "name": "sector"})

    df = (
        prices
        .merge(companies[["code", "name", "sectorCode", "market"]],
               on="code", how="left", validate="many_to_one")
        .merge(sectors[["sectorCode", "sector"]],
               on="sectorCode", how="left", validate="many_to_one")
        # 시계열 계산은 전부 '바로 위 행' 을 본다.
        # 종목별·날짜순으로 정렬해 두지 않으면 결과가 조용히 틀어진다.
        .sort_values(["code", "date"])
        .reset_index(drop=True)
    )

    # 일간 수익률(%). groupby 를 빼면 종목이 바뀌는 자리에서 값이 튄다.
    #   transform : 그룹별로 계산하되 원래 행 수 그대로 돌려준다.
    #   첫날은 비교 대상이 없어 NaN 이다. -> 종목당 1건씩 120건
    df["ret"] = df.groupby("code")["close"].transform(lambda s: s.pct_change() * 100)
    return df


def sector_order(df):
    """
    히트맵의 열을 세울 순서. 같은 섹터 종목이 이웃하게 놓인다.
    """
    # (code, sector) 쌍이 750번씩 반복되므로 종목당 한 줄로 줄인 뒤 정렬한다.
    return (df[["code", "sector"]].drop_duplicates()
            .sort_values(["sector", "code"])["code"].tolist())


def corr_pairs(corr, df):
    """
    상관 행렬을 '종목 쌍 하나 = 한 행' 짜리 표로 펴서 돌려준다.

    120 x 120 = 14,400칸이지만 쓸 수 있는 것은 7,140개뿐이다.
      · 대각선 120칸은 '자기 자신과의 상관' 이라 언제나 1.0 이다
      · 상관 행렬은 대칭이라 (A,B) 와 (B,A) 가 같은 값이다
    그래서 대각선을 빼고 한쪽 삼각형만 남긴다. 120 x 119 / 2 = 7,140.
    """
    
    # 종목코드 -> 섹터 를 찾는 Series. sector_of["G0001"] 처럼 꺼내 쓴다.
    sector_of = df[["code", "sector"]].drop_duplicates().set_index("code")["sector"]

    pairs = (corr.rename_axis(index="a", columns="b")
             .stack().rename("corr").reset_index())

    # a < b 인 것만 남기면 대각선(a == b)과 뒤집힌 쌍이 한 번에 걸러진다.
    pairs = pairs[pairs["a"] < pairs["b"]].reset_index(drop=True)

    #   여기서는 종목코드를 섹터 이름으로 바꾼다.
    pairs["same_sector"] = (pairs["a"].map(sector_of) == pairs["b"].map(sector_of))
    return pairs