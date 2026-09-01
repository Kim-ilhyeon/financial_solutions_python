"""
한글 폰트 설정과 그림 저장 경로.

왜 이걸 따로 빼 두었나
  한글 폰트 설정은 세 파일이 똑같이 필요하고, 순서를 한 번 틀리면
  세 파일 전부 한글이 깨진다. 한 군데 모아 두면 고칠 곳도 한 군데다.
"""

import platform
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager


# ==============================================================
#  1. 한글 폰트 찾기
# ==============================================================

# OS 별 기본 한글 폰트. 설치 없이 이미 깔려 있는 것들이다.
#   dict.get(key, 기본값) 으로 꺼낼 것이라 없는 OS 여도 에러가 나지 않는다.
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

    font_manager.fontManager.ttflist 는 matplotlib 이 시스템을 훑어 만들어 둔
    '설치된 폰트 목록' 이다. 각 원소가 폰트 하나이고 .name 에 이름이 들어 있다.
    집합(set)으로 만드는 이유는 'name in installed' 검사를 빠르게 하기 위해서다.
    """
    installed = {f.name for f in font_manager.fontManager.ttflist}

    # 리스트끼리 + 하면 이어 붙는다. 'OS 기본 폰트 -> 공통 후보' 순으로 찾게 된다.
    for name in _CANDIDATES.get(platform.system(), []) + _FALLBACK:
        if name in installed:
            return name
    return None


# ==============================================================
#  2. 그림 저장 경로
# ==============================================================
#
#  savefig("output/01.png") 처럼 상대경로로 적으면 '실행한 위치' 기준이 된다.
#  프로젝트 루트에서 실행하면 output/ 이 없어 FileNotFoundError 가 난다.
#  __file__ 을 기준으로 잡으면 어디서 실행하든 이 폴더의 output/ 을 가리킨다.

OUTPUT_DIR = Path(__file__).with_name("output")


def out(name):
    """
    output/ 안의 파일 경로를 만들어 준다. 폴더가 없으면 만든다.

    Path 객체끼리 / 로 이으면 경로가 이어진다. OS 별 구분자(\ 와 /)를
    직접 신경 쓰지 않아도 된다.
    mkdir(exist_ok=True) 는 '이미 있으면 그냥 넘어가라' 는 뜻이다.
    이게 없으면 두 번째 실행에서 FileExistsError 가 난다.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    return str(OUTPUT_DIR / name)


def saved_files():
    """output/ 에 저장된 파일 이름 목록. 파일 끝에서 결과를 확인할 때 쓴다."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    # iterdir() 은 폴더 안을 하나씩 돌려준다. .name 은 폴더 경로를 뗀 파일명이다.
    return sorted(p.name for p in OUTPUT_DIR.iterdir() if p.is_file())


# ==============================================================
#  3. 설정 - 순서가 전부다
# ==============================================================


def setup(theme=True, verbose=True):
    """
    한글 폰트와 마이너스 기호를 설정한다.

    순서가 중요하다.
      seaborn 의 set_theme() 이 rcParams 를 초기화하므로
      테마를 '먼저' 적용하고 그다음에 폰트를 설정해야 한다.
      반대로 하면 한글이 다시 깨진다.
    """
    if theme:
        # import 를 함수 안에 둔 이유: theme=False 로 쓰는 사람은
        # seaborn 이 설치돼 있지 않아도 이 함수를 쓸 수 있게 하려는 것이다.
        import seaborn as sns
        sns.set_theme(style="whitegrid")      # 테마 먼저

    font = find_korean_font()                 # 그다음 폰트
    if font:
        # plt.rcParams 는 matplotlib 의 전역 기본값 표(dict 처럼 쓴다).
        # 여기에 한 번 넣어 두면 이후 그리는 모든 그림에 적용된다.
        plt.rcParams["font.family"] = font
    elif verbose:
        print("[경고] 한글 폰트를 찾지 못했습니다. 제목이 네모로 표시됩니다.")
        print("       Linux: sudo apt install fonts-nanum  후 캐시 삭제")

    # 마이너스 기호는 별개 문제다.
    #    폰트를 바꿔도 유니코드 마이너스(−, U+2212)가 한글 폰트에 없어 깨진다.
    #    False 로 두면 평범한 ASCII 하이픈(-)을 쓴다.
    #    등락률처럼 음수가 나오는 축에서 반드시 걸린다.
    plt.rcParams["axes.unicode_minus"] = False

    plt.rcParams["figure.dpi"] = 100
    # savefig 할 때마다 bbox_inches="tight" 를 적는 대신 기본값으로 박아 둔다.
    # 축 라벨이 잘리는 사고를 미리 막는 설정이다. 
    plt.rcParams["savefig.bbox"] = "tight"

    if verbose:
        print(f"[폰트] {font or '(없음)'} / unicode_minus=False")

    return font
