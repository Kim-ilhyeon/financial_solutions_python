"""
    상관 히트맵과 그래프
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
df["ret"] = df.groupby("code")["close"].transform(lambda s : s.pct_change())

# 상관 히트맵 만들기
# 여러 변수들 간의 상관관계를 계산한 표를 색상의 농도와 밝기로 표현한 시각화 그래프






"""
    center=0은 반드시 넣어줘야 한다.
    그래야 -1 ~ 1까지 기준점 0을 가지고 색상을 직관적으로 표현할 수 있다.
"""








"""
    수치로보니 상관관계가 섹터별로 존재한다. -> 그림으로는 전혀 보이지 않는다.
    시장 전체가 함께 움직이는 요인이 워낙 커서
    섹터차이가 심하게 발생하지는 않기 때문에 바로 식별할 정도가 되지 않는다.
"""
