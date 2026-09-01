"""
실습용 통합 데이터 로더.

앞에서 만든 3단 조인(prices -> companies -> sectors)을 그대로 옮겨 두었다.
세 파일이 매번 merge 를 다시 쓰지 않도록 여기 모은 것이다.

'이미 붙인 데이터' 에서 출발한다.
  그려야 할 것이 '섹터별 분포', '종목 간 상관' 처럼 마스터 정보를 필요로 하기 때문이다.
  sector · market · name 열은 시세 파일에 없고 조인해야 생긴다.
"""

from _load import load_prices, load_companies, load_sectors


def load_merged():
    """prices + companies + sectors 를 붙인 90,000행 통합 데이터."""
    prices = load_prices()
    companies = load_companies()

    sectors = load_sectors().rename(columns={"code": "sectorCode", "name": "sector"})

    df = (
        prices
        .merge(
            companies[["code", "name", "sectorCode", "market"]],
            on="code", how="left", validate="many_to_one",
        )
        .merge(
            sectors[["sectorCode", "sector"]],
            on="sectorCode", how="left", validate="many_to_one",
        )
    )

    return df.sort_values(["code", "date"]).reset_index(drop=True)
