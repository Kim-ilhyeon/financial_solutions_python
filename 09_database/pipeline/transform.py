"""
Transform - 정제·계산·검증. 저장은 하지 않는다.
"""

import pandas as pd

NUM_COLS = ["open", "high", "low", "close", "volume", "change", "changeRate"]
OHLC = ["open", "high", "low", "close"]


def clean_prices(records, logger):
    """
    정제 함수. 단계마다 건수를 로그로 남긴다.
    """

    # Extract 가 준 list[dict] 를 표로 세운다. dict 의 키가 그대로 열 이름이 된다.
    df = pd.DataFrame(records)
    logger.info(f"  입력          {len(df):>8,}행")

    # 타입 정제 : 콤마를 먼저 지우고 변환
    for col in NUM_COLS:
        if col in df.columns:          # API 응답에 없는 열이 있을 수 있어 먼저 확인한다
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "", regex=False), errors="coerce"
            )

    # format="mixed" : 행마다 날짜 형식이 다를 수 있다고 알려 준다. 
    df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")

    # 종목 코드는 결합·중복 판정의 기준이므로 대소문자와 앞뒤 공백을 먼저 통일한다.
    df["code"] = df["code"].astype(str).str.upper().str.strip()
    logger.info(f"  타입 정제     {len(df):>8,}행   (종가 결측 {df['close'].isna().sum():,})")

    # 중복 제거 : 타입 정제 후에 해야 한다
    before = len(df)
    df = df.drop_duplicates(subset=["code", "date"], keep="first")
    logger.info(f"  중복 제거     {len(df):>8,}행   ({len(df) - before:+,})")

    # 이상치 표시 : 종목별 IQR + 논리 검사
    df = df.sort_values(["code", "date"]).reset_index(drop=True)

    def is_outlier(s):
        """한 종목의 종가 Series 를 받아 IQR 밖인지를 행마다 True/False 로 돌려준다. """
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1                        
        
        return (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)

    # groupby("code") 없이 전체에 IQR 을 걸면 안 된다.
    stat = df.groupby("code")["close"].transform(is_outlier)

    # 통계적 이상치와 별개로, 종가가 고가보다 높은 것은 그냥 틀린 값이다.
    logic = (df["close"] > df["high"]) | (df["close"] < df["low"])

    # bool 은 True=1 로 취급되므로 sum() 이 곧 개수다. 
    n_out = int((stat | logic).sum())

    df.loc[stat | logic, "close"] = pd.NA
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df.loc[df["volume"] < 0, "volume"] = pd.NA
    logger.info(f"  이상치 표시   {len(df):>8,}행   ({n_out:,}건 -> NaN)")

    # 결측 보간 : 반드시 종목별로  
    for col in OHLC:
        df[col] = df.groupby("code")[col].transform(
            lambda s: s.interpolate().ffill().bfill()
        )

    # 보간한 종가가 그날의 고가·저가 범위를 벗어날 수 있다.
    df["close"] = df["close"].clip(lower=df["low"], upper=df["high"])
    logger.info(f"  결측 보간     {len(df):>8,}행   (종가 결측 {df['close'].isna().sum():,})")

    # DB 타입에 맞춰 정수로 반올림한다
    n_frac = int((df[OHLC] % 1 != 0).sum().sum())
    for col in OHLC:
        df[col] = df[col].round(0)         
    logger.info(f"  정수 반올림   {len(df):>8,}행   (소수점이던 값 {n_frac:,}개)")

    # 종가를 고쳤으니 등락도 다시 계산
    prev = df.groupby("code")["close"].shift()
    df["change"] = (df["close"] - prev).round(0)
    df["changeRate"] = ((df["close"] - prev) / prev * 100).round(2)

    return df


def validate(df, logger):
    """정제가 끝났다는 것을 숫자로 확인한다. 실패하면 여기서 멈춘다."""
    checks = [
        ("날짜가 datetime", pd.api.types.is_datetime64_any_dtype(df["date"])),
        ("code+date 중복 0", df.duplicated(subset=["code", "date"]).sum() == 0),
        ("종가 결측 0", df["close"].isna().sum() == 0),
        ("OHLC 정합성", bool(((df["low"] <= df["close"]) & (df["close"] <= df["high"])).all())),
        ("거래량 음수 0", bool((df["volume"].dropna() >= 0).all())),
    ]
    failed = [n for n, ok in checks if not ok]
    for name, ok in checks:
        logger.info(f"  {'OK  ' if ok else 'FAIL'} {name}")

    if failed:
        raise ValueError(f"검증 실패: {failed}")
    return True
