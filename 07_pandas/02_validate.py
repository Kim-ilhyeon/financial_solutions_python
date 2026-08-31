"""
    - 1:N 결합에서 행이 불어나는 문제
    - validate와 concat
"""

import pandas as pd

from _load import load_companies, load_prices, load_financial, load_sectors


pd.set_option("display.width", 140)

prices = load_prices()
companies = load_companies()
sectors = load_sectors()
financial = load_financial()

# 1:N 결합 시 행이 불어난다.

print(f" prices : {len(prices)}행 = 종목당 750일")
print(f" financial : {len(financial)}행 = 종목당 12분기")

# 두 데이터를 code로 붙이면?
# 왼쪽 G0001 한 행이 오른쪽 G0001 열두 행과 각각 짝을 짓는다.
# merge는 짝이되는 모든 조합을 만든다.

boom = prices.merge(financial, on="code", how="left")
print(f" \n {len(prices)} -> {len(boom)} ({len(boom) // len(prices)}배)")


print(f"""
    종가 평균 : {prices['close'].mean():>18,.0f}{boom['close'].mean():>18,.0f}
    종가 합계 : {prices['close'].sum():>18,.0f}{boom['close'].sum():>18,.0f}
    행 수 : {len(prices):>18,}{len(boom):>18,}

    평균은 그대로인데 합계는 12배이다.
    모든 종목이 정확히 12분기씩 있어, 균등하게 붙여놨기 때문에.
""")

# validate로 막는다.
# merge옵션 중에 validate라는 옵션이 있다.
# df1.merge(df2, on="키", how="left", validate=". . .")
# many_to_one : validate에 해당하는 관계가 맞으면 원래와 같이 dataFrame을, 틀리면 결합하지 않고 MergeError.
# one_to_one(양쪽 모두 키가 유이리), one_to_many(왼쪽의 키가 유일), many_to_one(오른쪽의 키가 유일 <= 가장 자주 사용)

# many_to_one이 가장 많이 사용되는 이유.
# 시세(N행)에 마스터시트(1행)을 붙인다. -> 기본 형태
# 이런식의 데이터 merge를 사용해야 논리적, 물리적으로 행수가 늘어나지 않는다.

try:
    boom = prices.merge(financial, on="code", how="left", validate="many_to_one")
except Exception as e:
    print(f" {type(e).__name__} : {str(e)[:60]}...")

print("="*60)

raw = load_companies(raw=True)
try:
    prices.merge(raw[['code', 'name']], on="code", how="left", validate="many_to_one")
except Exception as e:
    msg = str(e).split("\n")[0]
    print(f" {type(e).__name__} : {msg}")

print("="*60)

# 중복된 행을 전부 True로 표시한 mask
# dups = raw[raw.duplicated(subset=["code"], keep=False)]["code"].unique()

ok = prices.merge(companies, on="code", how="left", validate="many_to_one")

print(f" {len(prices)} : {len(ok)}")


"""
    분기재무 데이터를 그대로 붙이려면...
    code로만 결합 시 어느분기의 재무인가?가 특정되지 않아서 고유한 값이 아니다.
    -> 여러 열을 복합키처럼 사용.
    merge(df, on=[key1, key2 . . .])
    지정한 열이 전부 일치하는 행끼리만 결합이 된다.
"""

p = prices.copy()
p["fiscalYear"] = p["date"].dt.year
p["fiscalQuarter"] = p["date"].dt.quarter

joined = p.merge(
    financial,
    on=["code", "fiscalYear", "fiscalQuarter"],
    how="left",
    validate="many_to_one",
)

print(f" {len(prices)} : {len(joined)} -> 행 수가 유지되는가?")

miss = joined["revenue"].isna().sum()

print(f" 매칭 실패 : {miss}건")

"""
    left merge에서 왼쪽에는 데이터가 있지만 오른쪽에 맞는 데이터가 없다면
    에러를 발생시키지 않고, NaN로 채운다.
"""


# 3단 join
# merge는 DataFrame을 돌려주므로, 그 결과에 또 merge를 붙일 수 있다.
full = (
    prices
    .merge(companies, on="code", how="left", validate="many_to_one")
    # sectors의 code/name은 companies의 code/name과 겹친다.
    .merge(sectors.rename(columns={"code": "sectorCode", "name": "sector"})
           , on="sectorCode", how="left", validate="many_to_one")
)

print(f" prices -> companies -> sectors")
print(f" {len(prices)}행 유지, {len(full)}행")

print(f" 섹터별 평균 종가 상위 5")
# nlargest(n) : 값이 큰 순으로 n개.
print(f" {full.groupby('sector')['close'].mean().nlargest(5).round(0).to_string()}")

print()

# concat - 이어 붙이기.
# pd.concat([df1, df2 . . .], ignore_index=True)

g1 = prices[prices['code'] == "G0001"].head(3)
g2 = prices[prices['code'] == "G0002"].head(3)

stacked = pd.concat([g1, g2])
print(f" 인덱스  : {stacked.index.tolist()}")

stacked = pd.concat([g1, g2], ignore_index=True)
print(f" 인덱스  : {stacked.index.tolist()}")

"""
    concat(axis=0) : 같은 구조로 쌓는다.
    concat(axis=1) : 옆으로 붙인다. - 인덱스 기준으로 정렬

    키로 정보를 붙인다. : merge사용
    같은 구조로 쌓고싶다. : concat(axis=0)
"""

# 결합이 완료되었을 때 검증 방법
before = len(prices)
after = len(full)

print(f" {'항목':<20}{'결과'}")
print("=" * 50)
print(f" {'행 수 유지':<20}{before:,} -> {after:,} : {before == after}")
print(f" {'새 결측':<20}{full['sector'].isna().sum():,}건")
print(f" {'종목 수':<20}{full['code'].nunique():,}개")
print(f" {'키가 유일한가'} {full.duplicated(subset=['code', 'date']).sum():,}건 중복")
