"""
    차트와 Seaborn
"""

import matplotlib

# Agg속성은 화면 없이 백 단에서 처리하겠다.
# 차트를 따로 띄우지 않고, 따로 처리해서 저장한다.
matplotlib.use("Agg")

import matplotlib.pyplot as plt

import seaborn as sns

from _style import setup, out, find_korean_font
from _merged import load_merged

setup()

df = load_merged()

# 종목별 일간 수익률(%)
df["ret"] = df.groupby("code")["close"].transform(lambda s : s.pct_change() * 100)

print(df["ret"])

"""
    무엇을 보는 용도로 사용할 것인가?
    시간에 따른 변화 -> 선(plot)
    범주 간 크기 비교 -> 막대(bar)
    하나의 분포 -> 히스토그램(hist)
    분포 + 이상치 -> 박스(boxplot)
    두 변수의 관계 -> 산점도(scatter)
    여러 변수의 상관 -> 히트맵(heatmap)

    차트 선택이 중요하다.
"""

# 분포 보기 - 히스토그램
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# ax.hist(값들, bins=구간 수)
# 값을 bins개의 구간으로 나눠서 각 구간에 몇개가 들어있는지 막대로 센다.
# hist는 NaN을 만나면 축 범위 계산이 깨진다. -> dropna()를 선행한다.
axes[0].hist(df["ret"].dropna(), bins=60, color="steelblue")
axes[0].set_title("일간 수익률 분포")
axes[0].set_xlabel("수익률 (%)")
axes[0].set_ylabel("빈도")

axes[1].hist(df["close"], bins=60, color="indianred")
axes[1].set_title("종가 분포")
axes[1].set_xlabel("종가 (원)")

fig.tight_layout()
fig.savefig(out("04_hist.png"), dpi=120)
plt.close(fig)

print(f" 수익률 : 평균 {df['ret'].mean():.3f}% , 표준편차 {df['ret'].std():.3f}%")
print(f" 종가 : 중앙값 {df['close'].median():,.0f}원 , 최대값 {df['close'].max():,.0f}원")


"""
    수익률은 0을 중심으로 좌우 대칭에 가깝초, 
    종가는 오른쪽으로 길게 늘어진 모양이다. -> 비싼종목이 소수다.(더 적다)

    bins갯수에 따라 차트의 인상이 달라진다.
    (너무 적으면 뭉개지고, 너무 많으면 등락이 심해보인다.)
    보통 bins의 갯수는 30 ~ 60 으로 바꿔가면서 확인해본다.
"""

# 박스 플롯 = IQR 확인하기
# IQR을 표기할 때 박스의 양 끝이 Q1, Q3 수염이 1.5 * IQR의 범위가 된다.
# 그 외에 점이 이상치로 찍힌다.

fig, ax = plt.subplots(figsize=(13, 5))

# seaborn의 호출형태 : sns.그래프(data=DataFrame, x="열 이름", y="열 이름", ax=Axes)
# ax=Axes -> 현재 그래프가 어디에 그려져야 하는지를 나타내 줌

sns.boxplot(data=df, x="sector", y="ret", ax=ax)
ax.set_title("섹터별 일간 수익률 분포")
ax.set_xlabel("섹터")
ax.set_ylabel("수익률 (%)")

fig.savefig(out("05_box.png"), dpi=120)
plt.close(fig)


q1, q3 = df["ret"].quantile([0.25, 0.75])
iqr = q3 - q1
n_out = ((df["ret"] < q1 - 1.5 * iqr) | (df["ret"] > q3 + 1.5 * iqr)).sum()

print(f" Q1 {q1:.3f}, Q3 {q3:.3f}, IQR {iqr:.3f}")
print(f" {q1 - 1.5 * iqr:.3f} ~ {q3 + 1.5 * iqr:.3f}")
print(f" 범위 밖 : {n_out:,}건")

"""
    박스 하나하나가 그 섹터만의 Q1, Q3로 다시 계산을 해줘야 한다.
    전체 기준으로 이상치를 선별하면 사실상 큰 의미가 없다. 섹터별 기준 이상치가 필요하다.
"""
per_sector=0
for name, g in df.groupby("sector"):
    a, b = g["ret"].quantile([0.25, 0.75])
    i = b - a
    per_sector += ((g["ret"] < a - 1.5 * i) | (g["ret"] > b + 1.5 * i)).sum()

print(f" 섹터별 실제 이상치의 합 : {per_sector:,}건")
print(f" 범위 밖 이상치 : {n_out:,}")
print(f" 섹터 별 이상치의 합 : {per_sector:,}")
print(f" 차이 : {n_out - per_sector:,} 건")

# 산점도

# sample(n, random_state=시드값)
# 무작위로 n행을 뽑는다. -> 5000개를 랜덤으로 값을 뽑는다.
sample = df.dropna(subset=["ret"]).sample(5000, random_state=42)

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

# scatter(x, y, s=점 크기, alpha=투명도)
# s : 점 하나의 면적. 기본값은 36
axes[0].scatter(sample["volume"], sample["ret"], s=6)
axes[0].set_title("산점도 (기본 값)")
axes[0].set_xlabel("거래량")
axes[0].set_ylabel("수익률 (%)")

axes[1].scatter(sample["volume"], sample["ret"], s=6, alpha=0.25)
axes[1].set_title("산점도 (투명하게)")
axes[1].set_xlabel("거래량")

fig.tight_layout()
fig.savefig(out("06_scatter.png"), dpi=120)
plt.close(fig)

# 산점도는 밀집도를 확인하기 위한 값으로 투명도를 조금 주면 눈으로 바로 확인하기가 더 용이하다.

# =========================================

# barplot (막대)
# 같은 sector에 속한 90000/10 = 9000개의 ret을 평균내서 막대 하나로 만듬
# 합계를 원하면 estimator="sum"을 지정해야 한다.
# 이미 groupby로 집계한 표를 넘기면 평균의 평균이 될 수 있다.
fig, ax = plt.subplots(figsize=(11, 4))

sns.barplot(date=df, x="sector", y="ret", ax=ax)

ax.axhline(0, color="gray", lw=0.8)

ax.set_title("섹터별 평균 일간 수익률")
ax.set_xlabel("섹터")
ax.set_ylabel("평균 수익률 (%)")
# axis=x -> x축 눈금에 적용해, rotation=30 글자를 30도 기울여라
ax.tick_params(axis="x", rotation=30)
fig.savefig(out("07_bar.png"), dpi=120)
plt.close(fig)

"""
    07_bar.png의 막대 위의 검은 선은 95%의 신뢰구간이다.
    합계가 아니라 평균을 그리고 있다.
"""

by_sector = df.groupby("sector")["ret"].agg(["mean", "str", "count"])
print(by_sector.round(4).head(4).to_string())


"""
    sns.barplot(data=df, x="sector", y="ret", ax=ax)

    x와 y열에 열 이름을 문자열로 넘김.
    즉, 한 열에 값이 쌓여있고, 다른 열이 그룹을 나타내는 구조여야 한다.
"""
