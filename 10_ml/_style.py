"""
한글 폰트 설정.

노트북이나 스크립트 맨 위에서 setup() 을 한 번 부르면 된다.
    from _style import setup
    setup()
"""

import platform

import matplotlib.pyplot as plt
from matplotlib import font_manager


# OS 별 기본 한글 폰트
_CANDIDATES = {
    "Windows": ["Malgun Gothic"],
    "Darwin": ["AppleGothic"],
}
# 리눅스·도커 등에서 쓸 수 있는 후보들
_FALLBACK = ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "IPAGothic"]


def find_korean_font():
    """설치된 폰트 중 한글을 표시할 수 있는 것을 찾는다."""
    installed = {f.name for f in font_manager.fontManager.ttflist}

    for name in _CANDIDATES.get(platform.system(), []) + _FALLBACK:
        if name in installed:
            return name
    return None


def setup(theme=True, verbose=True):
    """
    한글 폰트와 마이너스 기호를 설정한다.
    """
    if theme:
        import seaborn as sns
        sns.set_theme(style="whitegrid")      # ① 테마 먼저

    font = find_korean_font()                 # ② 그다음 폰트
    if font:
        # 한글 폰트 하나만 지정하면 안 된다. 순서까지 중요하다.
        plt.rcParams["font.family"] = ["DejaVu Sans", font]
    elif verbose:
        print("[경고] 한글 폰트를 찾지 못했습니다. 제목이 네모로 표시됩니다.")
        print("       Linux: sudo apt install fonts-nanum  후 캐시 삭제")

    # 일반 눈금의 마이너스는 별개 설정이다.
    plt.rcParams["axes.unicode_minus"] = False

    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.bbox"] = "tight"

    if verbose:
        print(f"[폰트] {font or '(없음)'} / unicode_minus=False")

    return font
