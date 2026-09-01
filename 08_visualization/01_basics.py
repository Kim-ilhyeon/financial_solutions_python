"""
    matplotlib을 활용한 기본적인 차트 생성 방법
    
    - Figure와 Axes
"""

import matplotlib

# Agg속성은 화면 없이 백 단에서 처리하겠다.
# 차트를 따로 띄우지 않고, 따로 처리해서 저장한다.
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from _style import setup, out, find_korean_font
from _merged import load_merged

setup()

df = load_merged()

one = df[df["code"] == "G0001"].sort_values("date")
# 차트는 시간기준으로 그린다.

# Figure와 Axes
# Figure (도화지) -> Axex (그래프 하나)

# subplots(행, 열, figsize(가로, 세로))
# 행과 열 생략 시 1 * 1 이다.
# figsuze에 12 * 4를 넣어주면 이전에 설정한 dpi(100)기준 1200 * 400 픽셀이 된다.
fig, ax = plt.subplots(figsize=(12, 4))

# ax.plot(x, y)
ax.plot(one["date"], one["close"])
ax.set_title("가온전자 주가 추이")
ax.set_xlabel("날짜")
ax.set_ylabel("종가 (원)")

# ax.grid() : 그래프 배경에 눈금선을 표시하는 메소드
ax.grid(alpha=0.3)

fig.savefig(out("01_basic.png"), dpi=120)
# plt.show()    # 화면에 띄워서 하나씩 바로 확인용

# ============================================

# 한글 폰트
print(f" 내 PC의 폰트 : {find_korean_font()}")
# 폰트만 한글로 변경 시 마이너스 값이 깨진다.
# plt.rcParams["font.family"] = font
# plt.rcParams["axes.unicode_minus"] = False

# seaborn을 사용할 때 순서를 잘 맞춰서 실행해야 함.
# sns.set_theme(style="whitegrid") -> 폰트 설정
# 테마 단계에서 폰트 파아미터가 초기화 된다.
# 테마 맞추고 폰트 설정 순서로 해야 함

# _style.py의 setup()을 먼저 실행하고 코드를 작성하면 된다.

fig, ax = plt.subplots(figsize=(10, 3))

# marker="."를 주면 각 데이터 점에 작은 점이 찍힌다.
ax.plot(one["date"].iloc[:60], one["changeRate"].iloc[:60], marker=".")

# axhline(y) y위치에 가라ㅘ 기준선 하나 그린다. lw은 선 굵기
ax.axhline(0, color="gray", lw=0.8)
ax.set_title("가온전자 일단 등락률")
ax.set_ylabel("등락률 (%)")
fig.savefig(out("02_minus.png"), dpi=120)
plt.close(fig)

# 최소한의 꾸미기
"""
    ax.set_title("타이틀")
    ax.set_xlabel("x축 제목")
    ax.set_ylabel("y축 제목")
    ax.legend() : 범례
    ax.grid(alpha=0.3) : 

    축 라벨과 단위가 없으면 그래프를 보고 판단이 어렵다.
    어떤 값인지 명확하게 보여줘야 한다.
"""

# 여러 개를 나란히 그리겠다.

codes = ["G0001", "G0002", "G0003", "G0004"]

# plt.subplot(2, 2) -> 그래프를 2행 2열로 네개를 그리겠다.
# axes은 (2, 2) numpy배열로 반환된다.
# sharex : x축을 모두 공유하겠다. -> 한 곳을 확대하면 전부 같이 움직임
fig, axes = plt.subplots(2, 2, figsize=(13, 6), sharex=True)

# flat으로 2차원 배열을 1차원으로 펼 수 있다.
# ravel과 비슷한 개념.
for ax, code in zip(axes.flat, codes):
    sub = df[df["code"] == code].sort_values("date")
    ax.plot(sub["date"], sub["close"], lw=1)
    ax.set_title(f"{sub['name'].iloc[0]} ({code})", fontsize=10)
    ax.grid(alpha=0.3)

fig.suptitle("종목별 주가 추이")

# fig.tight_layout() : 제목, 라벨이 서로 겹치지 않게 자동으로 여백을 계산해 줌.
fig.tight_layout()
fig.savefig(out("03_subplots.png"), dpi=120)

# 혹시 저장과 show()를 둘다 사용한다면 저장을 먼저 해야됨.