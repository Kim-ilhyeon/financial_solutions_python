"""
데이터 시각화 실습문제

같은 데이터를 그림으로 바꿔 보고, 그 그림이 정말 맞는지 숫자로 확인한다.

TODO 부분을 채워 완성하세요.
맨 아래 실행부는 그대로 두면 됩니다.
"""

import matplotlib
matplotlib.use("Agg")          # 화면 없이 파일로만 저장한다. 창이 떠서 멈추는 일이 없다.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from _data import load_merged, sector_order, corr_pairs
from _style import setup, out, saved_files

pd.set_option("display.width", 140)

setup()

# =========================================================================
# PRACTICE 1. 선 그래프 한 장
#   한 종목의 종가 추이를 선으로 그려 output/01_line.png 에 저장한다.
#
#   갖춰야 할 것
#     · 제목 · x축 라벨 · y축 라벨   ← y축에는 단위 "(원)" 을 넣는다
#     · 연한 격자
#     · 저장한 뒤 Figure 를 닫는다
#
#   [기대 결과]
#     output/01_line.png 이 만들어진다 (약 60 KB)
#
#   [힌트] 도화지와 그래프 : fig, ax = plt.subplots(figsize=(12, 4))
#            반환이 (Figure, Axes) 두 개짜리 튜플이라 두 이름으로 받는다.
#          선 그리기       : ax.plot(x값들, y값들)
#            x 가 날짜 타입이면 눈금을 알아서 날짜로 찍어 준다.
#          꾸미기          : ax.set_title(...) / ax.set_xlabel(...) / ax.set_ylabel(...)
#          격자            : ax.grid(alpha=0.3)     alpha 는 0(투명)~1(불투명)
#          저장            : path = out("01_line.png")
#                            fig.savefig(path, dpi=120)
#            out() 이 폴더를 만들고 절대경로를 돌려준다.
#          정리            : plt.close(fig)
#
#   plt.plot() 이 아니라 ax.plot() 을 쓸 것.
#     plt.plot() 은 '현재 그래프' 라는 숨은 상태에 그린다.
#     여러 장을 그리는 순간 어디에 그려졌는지 알 수 없게 된다.
# =========================================================================
def line_chart(one):
    """한 종목의 종가 추이를 그려 저장하고, 저장한 파일 경로를 반환한다."""
    # TODO: Figure/Axes 를 만들고 선을 그린 뒤 저장하고 경로를 반환
    pass
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(one["date"], one["close"])

    ax.set_title("종가 추이")
    ax.set_xlabel("날짜")
    ax.set_ylabel("종가 (원)")

    ax.grid(alpha=0.3)

    path = out("01_line.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)

    return path

# =========================================================================
# PRACTICE 2. 음수가 섞인 축
#   한 종목의 앞 60일 등락률(changeRate)을 선으로 그리고 0 기준선을 얹는다.
#
#   갖춰야 할 것
#     · 앞 60행만 쓴다              ← 750개를 다 그리면 아무것도 안 보인다
#     · 점 표시(marker)를 켠다
#     · y=0 위치에 회색 가로 기준선
#     · 제목과 y축 라벨 "(%)"
#
#   [기대 결과]
#     output/02_minus.png
#     y축 눈금의 음수가 '-1.5' 처럼 보여야 정상이다.
#       네모(□)로 보인다면 폰트 설정이 잘못된 것이다.
#
#   [힌트] 앞 60행   : one["date"].iloc[:60]
#          점 표시   : ax.plot(x, y, marker=".")
#          가로선    : ax.axhline(0, color="gray", lw=0.8)
#            lw 는 선 굵기(line width). 세로선은 axvline 이다.
#
#   한글 폰트만 바꾸면 마이너스 기호가 깨진다.
#     Matplotlib 이 쓰는 유니코드 마이너스(−)가 한글 폰트에 없기 때문이다.
#     실행부가 부르는 setup() 이 이미 두 가지를 함께 설정해 두었다.
#       plt.rcParams["font.family"]        = 폰트이름
#       plt.rcParams["axes.unicode_minus"] = False
#     음수가 나오는 축에서만 드러나는 함정이라 이 문제로 확인한다.
# =========================================================================
def minus_chart(one):
    """앞 60일 등락률을 0 기준선과 함께 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: 앞 60행만 그리고 axhline(0) 을 얹어 저장
    pass
    fig, ax = plt.subplots(figsize=(10, 3))

    ax.plot(one["date"].iloc[:60], one["changeRate"].iloc[:60], marker=".")

    ax.axhline(0, color="gray", lw=0.8)

    ax.set_title("한 종목의 앞 60일 등락률 추이")
    ax.set_xlabel("날짜")
    ax.set_ylabel("등락률 (%)")

    ax.grid(alpha=0.3)
    ax.axhline(0, color="gray", lw=0.8)

    path = out("02_minus.png")

    fig.savefig(path, dpi=120)

    plt.close(fig)

    return path

# =========================================================================
# PRACTICE 3. 네 개를 나란히
#   종목 네 개의 종가 추이를 2행 2열로 그린다.
#
#   갖춰야 할 것
#     · 2행 2열, x축 공유
#     · 각 칸의 제목은 "종목명 (코드)"    ← 종목명은 name 열에 있다
#     · 각 칸에 연한 격자
#     · 도화지 전체 제목 "종목별 주가 추이"
#     · 라벨이 겹치지 않게 정리
#
#   [기대 결과]
#     output/03_grid.png   네 칸이 모두 채워져 있어야 한다
#
#   [힌트] 여러 칸    : fig, axes = plt.subplots(2, 2, figsize=(13, 6), sharex=True)
#          이때 axes 는 Axes 하나가 아니라 (2, 2) 짜리 numpy 배열이다.
#          순회       : for ax, code in zip(axes.flat, codes):
#            axes.flat 이 (2,2) 를 (4,) 처럼 순서대로 펴서 준다.
#            zip 은 두 묶음을 짝지어 주고 짧은 쪽에서 멈춘다.
#          한 종목 뽑기: sub = df[df["code"] == code].sort_values("date")
#          종목명     : sub["name"].iloc[0]      750행 모두 같으므로 첫 행이면 된다
#          전체 제목  : fig.suptitle("...")      ax.set_title 과 다르다
#          여백 정리  : fig.tight_layout()
# =========================================================================
def grid_chart(df, codes):
    """네 종목의 종가 추이를 2x2 로 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: subplots(2, 2) 로 만들고 axes.flat 을 zip 으로 순회하며 그린다
    pass
    fig, axex = plt.subplots(2, 2, figsize=(13, 6), sharex=True)

    for ax, code in zip(axex.flat, codes):
        sub = df[df["code"] == code].sort_values("date")
        ax.plot(sub["date"], sub["close"], lw=1)
        ax.set_title(f"{sub['name'].iloc[0]} ({code})", fontsize=10)
        ax.grid(alpha=0.3)

    fig.suptitle("종복별 주가 추이")

    fig.tight_layout()

    path = out("03_grid.png")

    fig.savefig(path, dpi=120)

    plt.close(fig)

    return path


# =========================================================================
# PRACTICE 4. 분포 보기 - 히스토그램
#   왼쪽에 일간 수익률(ret), 오른쪽에 종가(close)의 분포를 그린다.
#
#   갖춰야 할 것
#     · 1행 2열
#     · 구간 수는 60
#     · 각 칸에 제목과 x축 라벨(단위 포함), 왼쪽에는 y축 라벨 "빈도"
#
#   [기대 결과]
#     output/04_hist.png
#     수익률은 0을 중심으로 좌우 대칭에 가깝고,
#     종가는 오른쪽으로 길게 늘어진 모양이다. 비싼 종목이 소수 있기 때문이다.
#
#   [힌트] 히스토그램 : ax.hist(값들, bins=60, color="steelblue")
#            bins 는 값을 몇 개의 구간으로 나눌지다.
#            너무 적으면 뭉개지고 너무 많으면 들쭉날쭉해 보인다. 30~60 이 무난하다.
#
#   ret 에는 NaN 이 120건 있다. 종목마다 첫날은 비교할 전날이 없기 때문이다.
#     hist 는 NaN 을 만나면 축 범위 계산이 깨진다. df["ret"].dropna() 로 넘길 것.
#     close 에는 결측이 없으므로 그대로 넘겨도 된다.
# =========================================================================
def hist_chart(df):
    """수익률과 종가의 분포를 나란히 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: 1x2 로 만들고 hist 두 개를 그린다. ret 는 dropna() 를 잊지 말 것
    pass


# =========================================================================
# PRACTICE 5. 섹터별 박스플롯
#   섹터별 일간 수익률 분포를 상자 열 개로 그린다.
#
#   갖춰야 할 것
#     · x 는 섹터, y 는 수익률
#     · 제목과 축 라벨(단위 포함)
#     · x축 눈금 글자를 30도 눕힌다   ← 섹터 이름 10개가 가로로 겹친다
#
#   [기대 결과]
#     output/05_box.png   상자 10개와, 그 위아래로 점(이상치)이 흩뿌려진 그림
#
#   [힌트] 박스플롯 : sns.boxplot(data=df, x="sector", y="ret", ax=ax)
#            ★ 값을 직접 넘기는 matplotlib 과 달리 '열 이름을 문자열로' 넘긴다.
#              한 열에 값이 쌓여 있고 다른 열이 그룹을 나타내는 구조여야 한다.
#            ★ ax= 를 빠뜨리면 '현재 그래프' 에 그려져 어디로 갔는지 알 수 없다.
#          눈금 회전 : ax.tick_params(axis="x", rotation=30)
#
#   상자를 읽는 법
#          ┌───┬───┐
#    ├─────┤   │   ├─────┤    ● ●
#          └───┴───┘
#    ↑     ↑   ↑   ↑     ↑    ↑
#   하한   Q1  중앙 Q3   상한  이상치
#
#     상자의 양 끝이 Q1·Q3 이고 수염이 1.5 x IQR 범위다. 그 밖의 점이 이상치로 찍힌다.
#     다음 문제에서 그 점의 개수를 직접 세어 본다.
# =========================================================================
def box_chart(df):
    """섹터별 수익률 분포를 박스플롯으로 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: sns.boxplot 으로 그리고 x축 눈금을 눕힌 뒤 저장
    pass


# =========================================================================
# PRACTICE 6. 박스플롯이 한 계산을 숫자로 검산하기
#   앞 문제의 그림에 찍힌 점이 몇 개인지 직접 세어 본다.
#
#   섹터마다 따로 Q1·Q3 을 구하고, 그 섹터의 수염 밖에 놓이는 값을 센다.
#   열 개 섹터의 합계를 정수 하나로 반환한다.
#
#     IQR       = Q3 - Q1
#     수염 범위 = Q1 - 1.5 x IQR  ~  Q3 + 1.5 x IQR
#
#   [기대 결과]
#     2,028건
#     실행부가 '전체를 한 덩어리로 봤을 때' 의 값(2,130건)도 함께 찍어 준다.
#     두 숫자가 다르다. 왜 다른지 생각해 볼 것.
#
#   [힌트] 그룹 순회 : for _, g in df.groupby("sector"):
#            (그룹 이름, 그 그룹만 담은 DataFrame) 을 하나씩 준다.
#            이름을 쓰지 않을 때는 _ 로 받아 버린다.
#          분위수    : q1, q3 = g["ret"].quantile([0.25, 0.75])
#            두 개를 한 번에 담은 Series 라 순서대로 언패킹된다.
#          조건 결합 : (g["ret"] < 아래) | (g["ret"] > 위)
#           or 가 아니라 | 이고, 각 조건을 괄호로 감싸야 한다.
#          세기      : 조건.sum()      True 는 1로 세므로 합계가 곧 건수다
#
#   왜 섹터별로 다시 구하는가.
#     박스플롯은 상자를 섹터마다 하나씩 그렸고,
#     상자 하나하나가 '그 섹터만의 Q1·Q3' 로 수염을 계산한다.
#     그림이 하는 계산을 따라 하려면 기준선도 섹터별로 다시 그어야 한다.
# =========================================================================
def count_outliers_by_sector(df):
    """섹터별 IQR 기준 이상치 건수의 합계를 정수로 반환한다."""
    # TODO: 섹터별로 Q1·Q3 을 구해 수염 밖 건수를 세서 합산
    pass


# =========================================================================
# PRACTICE 7. 산점도와 alpha
#   거래량(volume)과 수익률(ret)의 산점도를 alpha 없이 / alpha=0.15 로 나란히 그린다.
#
#   갖춰야 할 것
#     · 5,000개만 뽑아 쓴다. 뽑을 때 random_state=42 를 반드시 지정한다
#     · 1행 2열, 왼쪽은 alpha 기본값, 오른쪽은 alpha=0.15
#     · 점 크기는 s=6
#     · 각 칸에 제목과 x축 라벨, 왼쪽에는 y축 라벨
#
#   [기대 결과]
#     output/06_scatter.png
#     왼쪽은 새까맣게 뭉치고, 오른쪽은 밀집 구간이 진하게 드러난다.
#
#   [힌트] 표본 뽑기 : sample = df.dropna(subset=["ret"]).sample(5000, random_state=42)
#            subset=["ret"] : 그 열이 NaN 인 행만 버린다.
#            random_state 를 고정해야 몇 번을 돌려도 같은 5,000개가 뽑힌다.
#              고정하지 않으면 실행할 때마다 그림이 달라져 비교가 안 된다.
#          산점도    : ax.scatter(x, y, s=6, alpha=0.15)
#            s 는 점 하나의 면적이다. 기본값 36 은 5,000개를 찍기엔 너무 크다.
#            alpha=0.15 면 점 하나는 거의 안 보이고 일곱 개쯤 겹쳐야 진해진다.
#            결과적으로 '몇 개가 겹쳐 있는지' 가 색의 진하기로 드러난다.
# =========================================================================
def scatter_chart(df):
    """거래량-수익률 산점도를 alpha 유무로 나란히 그려 저장하고, 경로를 반환한다."""
    # TODO: 5,000개를 뽑아 1x2 로 그린다
    pass


# =========================================================================
# PRACTICE 8. 막대그래프
#   섹터별 일간 수익률을 막대그래프로 그린다.
#
#   갖춰야 할 것
#     · x 는 섹터, y 는 수익률
#     · y=0 에 회색 가로 기준선   ← 음수 막대가 있어서 필요하다
#     · 제목과 축 라벨, x축 눈금 30도 회전
#
#   [기대 결과]
#     output/07_bar.png
#     막대 길이 차이는 미미하고 막대 위의 검은 세로선(신뢰구간)이 크다.
#     "섹터별로 수익률이 다르다" 고 말하기 어렵다는 뜻이다.
#     실행부가 groupby 로 구한 평균을 함께 찍어 주니 막대 높이와 대조해 볼 것.
#
#   [힌트] 막대 : sns.barplot(data=df, x="sector", y="ret", ax=ax)
#          기준선: ax.axhline(0, color="gray", lw=0.8)
#
#   barplot 은 값을 그대로 그리지 않는다.
#     같은 섹터에 속한 9,000개의 값을 **평균 내서** 막대 하나로 만든다.
#     합계로 오해하기 쉬우니 y축 라벨에 "평균" 이라고 적어 둘 것.
#     합계를 원하면 estimator="sum" 을 지정해야 한다.
# =========================================================================
def bar_chart(df):
    """섹터별 평균 일간 수익률을 막대로 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: sns.barplot 으로 그리고 0 기준선을 얹어 저장
    pass


# =========================================================================
# PRACTICE 9. 상관 행렬 만들기
#   종목끼리 수익률이 얼마나 같이 움직이는지를 담은 120 x 120 표를 만든다.
#
#   세 단계다.
#     ① 긴 표를 넓은 표로 세운다   행=날짜, 열=종목, 칸=수익률   -> (750, 120)
#     ② 열을 order 순서대로 다시 세운다
#     ③ 열끼리의 상관계수를 구한다                              -> (120, 120)
#
#   [기대 결과]
#     (120, 120) 짜리 DataFrame
#     대각선 값은 1.0    ← 자기 자신과의 상관이라 언제나 그렇다
#     첫 세 열은 ['G0004', 'G0005', 'G0008']
#
#   [힌트] 세우기 : df.pivot_table(index="date", columns="code", values="ret")
#            index 의 고유값이 행, columns 의 고유값이 열이 된다.
#          열 순서 바꾸기 : pivot = pivot[order]
#            열 이름 리스트를 대괄호에 넣으면 '그 순서대로 세운 표' 가 된다.
#            값은 그대로고 순서만 바뀐다.
#          상관     : pivot.corr()
#            열끼리의 상관계수 행렬을 돌려준다. -1(정반대) ~ 0(무관) ~ 1(똑같이 움직임).
#            NaN 이 있는 칸은 알아서 빼고 계산한다.
#
#   왜 종목을 '열' 로 세우는가.
#     corr() 이 열끼리의 상관을 구하기 때문이다. 비교하고 싶은 것을 열에 둔다.
#
#   order 는 _data.py 가 만들어 준다. 같은 섹터 종목이 이웃하게 정렬된 목록이다.
#     이 순서로 세우지 않으면 블록이 있어도 그림에 나타나지 않는다.
# =========================================================================
def corr_matrix(df, order):
    """종목 x 종목 상관 행렬(120 x 120)을 반환한다."""
    # TODO: pivot_table 로 세우고, order 순으로 열을 정렬한 뒤 corr() 을 반환
    pass


# =========================================================================
# PRACTICE 10. 히트맵과 center=0
#   같은 상관 행렬을 두 가지 설정으로 나란히 그려 인상이 어떻게 달라지는지 본다.
#
#     왼쪽  : center 를 지정하지 않는다
#     오른쪽: center=0, vmin=-1, vmax=1
#
#   갖춰야 할 것
#     · 1행 2열, 팔레트는 둘 다 "coolwarm"
#     · 눈금 글자는 양쪽 다 끈다   ← 종목 120개를 다 찍으면 읽을 수 없다
#     · 각 칸에 제목
#
#   [기대 결과]
#     output/08_heatmap.png
#     왼쪽이 훨씬 붉고 강해 보인다. 같은 데이터인데도 그렇다.
#
#   [힌트] 히트맵 : sns.heatmap(표, cmap="coolwarm", center=0, vmin=-1, vmax=1,
#                              xticklabels=False, yticklabels=False, ax=ax)
#            cmap="coolwarm" 은 발산형 팔레트다. 파랑 - 흰색 - 빨강 순으로 간다.
#
#   center 는 '팔레트의 흰색을 어느 값에 놓을지' 다.
#     상관계수는 -1 ~ 1 이고 0이 기준점이다.
#     지정하지 않으면 흰색이 '데이터 평균' 에 맞춰져,
#     약한 양의 상관이 강한 빨강으로 보인다. 발산형 팔레트와 center=0 은 짝이다.
#
#   vmin/vmax 는 색 범위의 양 끝을 고정한다.
#     고정하지 않으면 그림마다 같은 색이 다른 값을 뜻하게 되어 여러 장을 비교할 수 없다.
# =========================================================================
def heatmap_pair(corr):
    """center 유무를 나란히 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: 1x2 로 만들고 heatmap 을 두 번 그린다
    pass


# =========================================================================
# PRACTICE 11. 섹터 블록이 보이는가 - 숫자로 확인
#   히트맵을 보면 같은 섹터끼리 네모난 덩어리(블록)를 이룰 것 같은데 잘 안 보인다.
#   정말 신호가 없는 것인지 숫자로 확인한다.
#
#   pairs 에는 종목 쌍 7,140개가 한 행씩 들어 있다. 네 열짜리 표다.
#
#     a        b        corr      same_sector
#     G0004    G0005    0.3345    True
#     G0004    G0011    0.1102    False
#     ...
#
#   same_sector 로 나눠 각각의 평균 상관을 구하고, (같은 섹터, 다른 섹터) 순서로
#   실수 두 개를 반환한다.
#
#   [기대 결과]
#     같은 섹터 0.2227   /   다른 섹터 0.1650    차이 +0.0577
#
#   [힌트] 그룹 평균 : pairs.groupby("same_sector")["corr"].mean()
#            반환은 인덱스가 True / False 두 개짜리 Series 다.
#          꺼내기    : means.loc[True] / means.loc[False]
#           .iloc[0] 처럼 순서에 기대지 말 것. 정렬이 바뀌면 조용히 틀어진다.
#          반환      : return float(...), float(...)
#            쉼표로 이으면 튜플 하나가 된다. 실행부가 두 이름으로 받아 쓴다.
#
#   pairs 는 _data.py 의 corr_pairs() 가 만들어 준다. 실행부가 대신 불러 넘긴다.
#     120 x 120 = 14,400칸이지만 쓸 수 있는 것은 7,140개뿐이다.
#     대각선 120칸은 자기 자신이라 언제나 1.0 이고,
#     상관 행렬은 대칭이라 (A,B) 와 (B,A) 가 같은 값이기 때문이다.
# =========================================================================
def sector_block(pairs):
    """(같은 섹터 평균 상관, 다른 섹터 평균 상관) 을 반환한다."""
    # TODO: same_sector 로 묶어 평균을 구하고 두 값을 튜플로 반환
    pass


# =========================================================================
# PRACTICE 12. 축 범위가 만드는 착시
#   같은 데이터를 두 번 그린다. 왼쪽만 y축을 0부터 시작하게 만든다.
#
#     왼쪽  : y축을 0 ~ (최댓값 x 1.1) 로 고정
#     오른쪽: y축을 건드리지 않는다 (matplotlib 이 알아서 잡는다)
#
#   갖춰야 할 것
#     · 1행 2열
#     · 각 칸에 제목, 왼쪽에 y축 라벨 "(원)"
#     · 오른쪽 선은 다른 색으로 (예: color="crimson")
#
#   [기대 결과]
#     output/09_axis.png
#     왼쪽은 완만한 선, 오른쪽은 급등락하는 선으로 보인다. 같은 데이터다.
#     실행부가 실제 변동폭(8,885 ~ 14,584원)을 찍어 준다.
#
#   [힌트] y축 고정 : ax.set_ylim(아래, 위)
#            여기서는 ax.set_ylim(0, one["close"].max() * 1.1) 이다.
#            1.1 을 곱하는 것은 위쪽에 여유를 조금 두려는 것이다.
#            x축은 set_xlim 이다.
#          오른쪽은 set_ylim 을 아예 부르지 않으면 된다.
#
#   의도적으로 하면 조작이고, 모르고 하면 오독이다.
#     변화의 '크기' 를 보여주려면 0부터,
#     변화의 '패턴' 을 보려면 자동 범위가 낫다.
#     무엇을 보여주려는지 먼저 정하고 축을 고를 것.
# =========================================================================
def axis_illusion(one):
    """y축 0부터 / 자동 범위를 나란히 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: 1x2 로 그리고 왼쪽에만 set_ylim 을 건다
    pass


# =========================================================================
# PRACTICE 13. 이상치 하나가 스케일을 망친다
#   750행 중 301번째(번호로는 300) 행의 종가를 100배로 만든 표를 따로 만들어
#   원본과 나란히 그린다.
#
#     왼쪽  : 오염된 표
#     오른쪽: 원본
#
#   갖춰야 할 것
#     · 넘겨받은 one 을 바꾸지 않는다   ← 실행부가 이것을 검사한다
#     · 1행 2열, 각 칸에 제목, 왼쪽에 y축 라벨
#
#   [기대 결과]
#     output/10_outlier.png
#     왼쪽은 뾰족한 봉우리 하나와 바닥에 붙은 평평한 선,
#     오른쪽은 원래의 오르내림이 보인다.
#     실행부의 '원본이 바뀌지 않았는가' 가 통과여야 한다.
#
#   [힌트] 복사     : polluted = one.copy()
#            복사하지 않고 고치면 넘겨받은 원본까지 바뀐다.
#            함수가 조용히 바깥을 바꾸는 것은 원인을 찾기 가장 어려운 버그다.
#          한 칸 고치기 : polluted.iloc[300, polluted.columns.get_loc("close")] *= 100
#            iloc 은 이름이 아니라 번호만 받는다.
#            columns.get_loc("close") 가 close 열이 몇 번째인지 숫자로 알려 준다.
#            이렇게 해 두면 열 순서가 바뀌어도 이 코드가 계속 맞는다.
#
#   750개 중 단 1개 때문에 나머지 749개가 평평한 선이 된다.
#     y축이 그 한 점까지 담느라 100배로 늘어났기 때문이다.
#     그래프가 이상하면 먼저 데이터를 의심할 것.
# =========================================================================
def outlier_scale(one):
    """오염본과 원본을 나란히 그려 저장하고, 파일 경로를 반환한다."""
    # TODO: copy() 로 복사해 한 칸을 100배로 만든 뒤 1x2 로 그린다
    pass


# =========================================================================
# PRACTICE 14. 서술형 - 왜 히트맵에서는 안 보였는가
#   11번에서 숫자로는 분명한 차이를 확인했다.
#
#     같은 섹터 0.2227   다른 섹터 0.1650   차이 +0.0577
#     전체 평균 0.1708
#
#   그런데 10번의 히트맵에서는 섹터 블록이 잘 보이지 않았다.
#   왜 그런가? 그리고 신호가 있다는 것을 무엇으로 확인했는가?
#   아래 문자열에 적으세요.
#
#   [힌트] 세 숫자를 나란히 놓고 보세요.
#            전체 평균 0.1708 은 '모든 종목이 이만큼은 함께 움직인다' 는 뜻이다.
#            그 위에 얹힌 섹터 차이 0.0577 은 색으로 얼마나 구분될까.
#          그리고 히트맵의 색 범위가 -1 ~ 1 이라는 점도 함께 생각해 보세요.
# =========================================================================
ANSWER = """
TODO: 여기에 답을 적으세요.
"""


# =========================================================================
#  실행부  ―  아래는 수정하지 않아도 됩니다
# =========================================================================
def step(fn, *args):
    """앞 문제가 미완성이면 건너뛰고, 에러가 나도 실행이 멈추지 않게 감싼다."""
    if any(a is None for a in args):
        print("  [건너뜀] 앞 문제를 먼저 완성하세요.")
        return None
    try:
        result = fn(*args)
    except Exception as e:
        print(f"  [미완성] {type(e).__name__}: {str(e).splitlines()[0][:90]}")
        return None
    if result is None:
        print("  [미완성] 함수가 아직 값을 돌려주지 않습니다.")
        return None
    return result


def section(title):
    print("\n" + "=" * 68)
    print(f" {title}")
    print("=" * 68)


def show_file(path):
    """저장된 그림의 경로와 크기를 확인한다. 파일이 없으면 실패로 알린다."""
    import os
    if path is None:
        return
    if os.path.exists(path):
        kb = os.path.getsize(path) / 1024
        print(f"  저장됨 : output/{os.path.basename(path)}  ({kb:,.0f} KB)")
    else:
        print(f"  ⚠ 파일이 없습니다 : {path}")


if __name__ == "__main__":

    setup()

    df = load_merged()
    one = df[df["code"] == "G0001"].sort_values("date")

    print(f"\n통합 데이터  {len(df):>8,}행   {df['code'].nunique()}종목 x "
          f"{len(df) // df['code'].nunique()}거래일   섹터 {df['sector'].nunique()}종")
    print(f"수익률 결측  {df['ret'].isna().sum():>8,}건   "
          f"= 종목당 1건 (첫날은 비교 대상이 없다)")

    section("PRACTICE 1. 선 그래프 한 장")
    show_file(step(line_chart, one))

    section("PRACTICE 2. 음수가 섞인 축")
    show_file(step(minus_chart, one))
    print("  y축의 음수가 '-1.5' 처럼 보이면 정상입니다. 네모로 보이면 폰트 설정 문제입니다.")

    section("PRACTICE 3. 네 개를 나란히")
    show_file(step(grid_chart, df, ["G0001", "G0002", "G0003", "G0004"]))

    section("PRACTICE 4. 분포 보기 - 히스토그램")
    show_file(step(hist_chart, df))
    print(f"  수익률 : 평균 {df['ret'].mean():.3f}%, 표준편차 {df['ret'].std():.3f}%")
    print(f"  종가   : 중앙값 {df['close'].median():,.0f}원, 최댓값 {df['close'].max():,.0f}원")

    section("PRACTICE 5. 섹터별 박스플롯")
    show_file(step(box_chart, df))

    section("PRACTICE 6. 박스플롯이 한 계산을 숫자로 검산하기")
    n_sector = step(count_outliers_by_sector, df)
    if n_sector is not None:
        q1, q3 = df["ret"].quantile([0.25, 0.75])
        iqr = q3 - q1
        n_all = int(((df["ret"] < q1 - 1.5 * iqr) | (df["ret"] > q3 + 1.5 * iqr)).sum())
        print(f"  전체를 한 덩어리로 봤을 때 : {n_all:>6,}건   "
              f"(Q1 {q1:.3f}  Q3 {q3:.3f}  IQR {iqr:.3f})")
        print(f"  섹터별로 따로 봤을 때      : {n_sector:>6,}건   <- 그림이 하는 계산")
        print(f"  차이                       : {n_all - n_sector:>6,}건")
        print("\n  박스를 섹터별로 그렸으니 기준선도 섹터별로 다시 그어진다.")
        print("  '전체 기준으로는 이상치인데 자기 섹터 안에서는 평범한 값' 이 있어서 어긋난다.")

    section("PRACTICE 7. 산점도와 alpha")
    show_file(step(scatter_chart, df))

    section("PRACTICE 8. 막대그래프")
    show_file(step(bar_chart, df))
    by_sector = df.groupby("sector")["ret"].agg(["mean", "count"])
    print("\n  숫자로 대조 (막대 높이는 sum 이 아니라 mean 이다):")
    print(by_sector.round(4).head(4).to_string())

    section("PRACTICE 9. 상관 행렬 만들기")
    order = sector_order(df)
    corr = step(corr_matrix, df, order)
    if corr is not None:
        print(f"  상관 행렬 : {corr.shape}   (종목 x 종목)")
        print(f"  대각선 값 : {corr.iloc[0, 0]:.1f}  (자기 자신과의 상관이라 언제나 1.0)")
        print(f"  열 순서   : {corr.columns[:3].tolist()} ...  섹터 순으로 세워졌는가")

    section("PRACTICE 10. 히트맵과 center=0")
    show_file(step(heatmap_pair, corr))
    print("  두 그림을 나란히 열어 비교해 보세요. 같은 데이터, 다른 인상입니다.")

    section("PRACTICE 11. 섹터 블록이 보이는가 - 숫자로 확인")
    pairs = corr_pairs(corr, df) if corr is not None else None
    if pairs is not None:
        print(f"  종목 쌍 : {len(pairs):,}개   "
              f"(같은 섹터 {int(pairs['same_sector'].sum()):,} / "
              f"다른 섹터 {int((~pairs['same_sector']).sum()):,})")
    result = step(sector_block, pairs)
    if result is not None:
        same, diff = result
        print(f"  같은 섹터 평균 상관 : {same:>8.4f}")
        print(f"  다른 섹터 평균 상관 : {diff:>8.4f}")
        print(f"  차이                : {same - diff:>+8.4f}")
        print(f"  전체 평균 상관      : {pairs['corr'].mean():>8.4f}   <- 서술형의 열쇠")

    section("PRACTICE 12. 축 범위가 만드는 착시")
    recent = one.tail(120)
    show_file(step(axis_illusion, recent))
    lo, hi = recent["close"].min(), recent["close"].max()
    print(f"  같은 데이터다. 실제 변동폭은 {lo:,.0f} ~ {hi:,.0f}원 ({(hi / lo - 1) * 100:.1f}%)")

    section("PRACTICE 13. 이상치 하나가 스케일을 망친다")
    show_file(step(outlier_scale, one))
    print(f"  750개 중 단 1개 때문에 나머지 749개가 평평한 선이 된다.")
    print(f"  원본이 바뀌지 않았는가 : "
          f"{'통과' if one['close'].max() < 10_000_000 else '실패 - copy() 를 확인할 것'}")

    section("PRACTICE 14. 서술형")
    print("  [제출한 답]")
    print("  " + ANSWER.strip().replace("\n", "\n  "))

    print("\n" + "=" * 68)
    print(" 저장된 그림")
    print("=" * 68)
    for f in saved_files():
        print(f"    output/{f}")