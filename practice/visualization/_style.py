"""
한글 폰트 설정과 그림 저장 경로.
"""

import platform
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager


# ==============================================================
#  1. 한글 폰트 찾기
# ==============================================================

# OS 별 기본 한글 폰트. 따로 설치하지 않아도 이미 깔려 있는 것들이다.
_CANDIDATES = {
    "Windows": ["Malgun Gothic"],
    "Darwin": ["AppleGothic"],       # platform.system() 이 macOS 를 이렇게 부른다
}
# 리눅스·도커 등에서 쓸 수 있는 후보들 (설치되어 있는 것을 찾아 쓴다)
_FALLBACK = ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "IPAGothic"]


def find_korean_font():
    """
    설치된 폰트 중 한글을 표시할 수 있는 것을 찾는다.

    Returns:
        str  : 찾은 폰트 이름 (예: 'Malgun Gothic')
        None : 하나도 못 찾았을 때
    """
    # fontManager.ttflist 는 matplotlib 이 시스템을 훑어 만들어 둔 '설치된 폰트 목록' 이다.
    # 집합으로 만들면 'name in installed' 검사가 빠르다.
    installed = {f.name for f in font_manager.fontManager.ttflist}

    for name in _CANDIDATES.get(platform.system(), []) + _FALLBACK:
        if name in installed:
            return name
    return None


# ==============================================================
#  2. 그림 저장 경로
# ==============================================================
#

OUTPUT_DIR = Path(__file__).with_name("output")


def out(name):
    """
    output/ 안의 파일 경로를 만들어 준다. 폴더가 없으면 만든다.

        out("01_line.png")  ->  '.../10_visualization_practice/output/01_line.png'

    mkdir(exist_ok=True) 는 '이미 있으면 그냥 넘어가라' 는 뜻이다.
    이게 없으면 두 번째 실행에서 FileExistsError 가 난다.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    return str(OUTPUT_DIR / name)


def saved_files():
    """output/ 에 저장된 파일 이름 목록. 끝에서 결과를 확인할 때 쓴다."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    return sorted(p.name for p in OUTPUT_DIR.iterdir() if p.is_file())


# ==============================================================
#  3. 설정 - 순서가 전부다
# ==============================================================


def setup(theme=True, verbose=True):
    """
    한글 폰트와 마이너스 기호를 설정한다.

    Args:
        theme   : seaborn 테마를 함께 적용할지. False 면 matplotlib 기본 모양.
        verbose : 어떤 폰트를 잡았는지 화면에 찍을지.

    Returns:
        str 또는 None : 실제로 적용된 폰트 이름

    """
    if theme:
        import seaborn as sns
        sns.set_theme(style="whitegrid")      # ① 테마 먼저

    font = find_korean_font()                 # ② 그다음 폰트
    if font:
        # plt.rcParams 는 matplotlib 의 전역 기본값 표(dict 처럼 쓴다).
        # 한 번 넣어 두면 이후 그리는 모든 그림에 적용된다.
        plt.rcParams["font.family"] = font
    elif verbose:
        print("[경고] 한글 폰트를 찾지 못했습니다. 제목이 네모로 표시됩니다.")
        print("       Linux: sudo apt install fonts-nanum  후 캐시 삭제")

    # ③ 마이너스 기호는 별개 문제다.
    plt.rcParams["axes.unicode_minus"] = False

    plt.rcParams["figure.dpi"] = 100
    # savefig 할 때마다 bbox_inches="tight" 를 적는 대신 기본값으로 박아 둔다.
    # 축 라벨이 잘리는 사고를 미리 막는 설정이다.
    plt.rcParams["savefig.bbox"] = "tight"

    if verbose:
        print(f"[폰트] {font or '(없음)'} / unicode_minus=False")

    return font