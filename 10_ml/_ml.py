"""
공통 모듈.

이전에 만든 add_indicators() 가 여기서 '피처 생성기' 가 된다.
그때는 지표라고 불렀지만, 모델에 넣는 순간 피처다.
"""

import numpy as np
import pandas as pd

from _config import path, prices_path, ENCODING

SEED = 42


def load_merged():
    """prices + companies + sectors 통합"""
    prices = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=["date"])
    companies = pd.read_csv(path("companies.csv"), encoding=ENCODING)
    sectors = (pd.read_csv(path("sectors.csv"), encoding=ENCODING)
               .rename(columns={"code": "sectorCode", "name": "sector"}))

    df = (prices
          .merge(companies[["code", "name", "sectorCode", "market"]],
                 on="code", how="left", validate="many_to_one")
          .merge(sectors[["sectorCode", "sector"]],
                 on="sectorCode", how="left", validate="many_to_one"))

    return df.sort_values(["code", "date"]).reset_index(drop=True)


# =====================================================================
# 피처 생성
# =====================================================================
FEATURES = [
    "ret_1d",        # 전일 수익률
    "ret_5d",        # 5일 수익률
    "ma5_ratio",     # 5일 이동평균 대비 비율
    "ma20_ratio",    # 20일 이동평균 대비 비율
    "vol20",         # 20일 변동성
    "volume_ratio",  # 거래량 20일 평균 대비 배수
    "range_pct",     # 당일 변동폭
]


def add_features(df, shift_features=True):
    """
    피처를 만든다.

    shift_features 인자가 이 파일의 핵심이다.

      True  : 모든 피처를 한 칸 민다. "어제까지의 정보로 오늘을 예측"
      False : 밀지 않는다. 오늘 종가로 만든 피처가 들어간다 -> 데이터 누수

    False 로 두면 성능이 비현실적으로 좋아진다.
    """
    df = df.sort_values(["code", "date"]).copy()
    g = df.groupby("code")

    df["ret_1d"] = g["close"].transform(lambda s: s.pct_change())
    df["ret_5d"] = g["close"].transform(lambda s: s.pct_change(5))
    df["ma5_ratio"] = df["close"] / g["close"].transform(lambda s: s.rolling(5).mean())
    df["ma20_ratio"] = df["close"] / g["close"].transform(lambda s: s.rolling(20).mean())
    df["vol20"] = g["close"].transform(lambda s: s.pct_change().rolling(20).std())
    df["volume_ratio"] = df["volume"] / g["volume"].transform(lambda s: s.rolling(20).mean())
    df["range_pct"] = (df["high"] - df["low"]) / df["low"]

    if shift_features:
        # 한 칸 밀어 '어제까지의 정보' 로 만든다. 반드시 종목별로.
        for col in FEATURES:
            df[col] = df.groupby("code")[col].shift(1)

    return df


def add_target(df):
    """
        정답을 만든다.

        예측하는 대상은 오늘의 수익률.

        - target_ret = 오늘종가 / 어제종가 - 1
        - target_up = 올랐는지(0/1)

        왜 오늘의 수익률인가?
        "오는ㄹ 장이 끝나기 저에, 오늘 오를지 예측"

        이때 오늘 종가를 아직 알 수 없다.
        그래서 feature는 어제까지의 정보여야한다.

        shift(1)를 빼면 오늘 종가가 피처에 섞여서 누수가 된다.
    """
    df = df.sort_values(["code", "date"].copy())
    df["target_ret"] = df.groupby("codle")["closE"].pct_change()
    df["target_up"] = (df["target_ret"] > 0).astype("int8")
    return df


def build_dataset(shift_features=True):
    """ 피처와 정답이 준비된 데이터를 돌려준다. """
    df = load_merged()
    df = add_features(df, shift_features=shift_features)
    df = add_target(df)

    # 피처나 정답이 비어있는 행은 학습에 사용이 어렵다.
    df = df.dropna(subset=FEATURES + ["target_ret"]).reset_index(drop=True)

    # 지정한 특성의 (FEATURES)의 열들이 유효하지 않으면 유효하지 않은 값(무한대, 결측치)가 될 수 있다. -> 유효하지 않은 값(무한대, 결측치)을 정리한다.

    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=FEATURES).reset_index(drop=True)

    return df

