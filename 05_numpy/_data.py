"""
    실습 데이터를 로딩 (불러오기)
"""
from pathlib import Path
import numpy as np

# __file__는 지금 현재 파일의 경로(_data.py)
CSV_PATH = Path(__file__).with_name("prices.csv")

_COLUMNS = {
    "code": 0,
    "date": 1,
    "open": 2,
    "high": 3,
    "low": 4,
    "close": 5,
    "volume": 6,
    "change": 7,
    "changeRate": 8,
}

# 한 번 읽은 열을 담아두는 곳
_cache = {}

def _read(col, dtype):
    """
        csv에서 하나의 열만 읽어 1차원 배열로 리턴
    """
    key = (col, str(dtype))

    if key not in _cache:
        if not CSV_PATH.exists():
            raise FileNotFoundError(f" {CSV_PATH} 파일을 찾을 수 없습니다.")

    _cache[key] = np.loadtxt(
        CSV_PATH,
        delimiter=",",   # 구분자지정(,)
        skiprows=1,      # 첫줄을 건너뜀
        usecols=_COLUMNS[col],  # 필요한 열 하나만 읽는 것
        dtype=dtype,            # 작성 안하면 기본값 float64로 출력됨
        encoding="UTF-8-sig",   # -sig를 추가하면 밑에 설명한 표식을 제거하고 읽어줌
    )
    # CSV는 맨 앞에 BOM이라는 눈에 안보이는 표식이 붙음.
    # 그냥 읽으면 첫 열 이름이 'code'가 아니라 앞에 표식이 붙어서 나옴.

    # 원본을 그대로 주면, 받아간 쪽에서 값을 변경했을 때 값이 변경.
    return _cache[key].copy()
    

def load_flat():
    # 종가만 1차원 배열로 뽑아서 return
    return _read('close', 'int64')

def load_one_stock(idx=0):
    """
        한 종목의 종가만 1차원으로, 
        csv자체가 종목 하나당 750줄, 그다음 종목 751줄 ~
        idx번째 종목 : idx * 750
    """

    flat = (load_flat())
    start = idx * N_DAYS
    return flat[start : start + N_DAYS]





