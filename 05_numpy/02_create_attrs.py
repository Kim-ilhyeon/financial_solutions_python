"""
    배열 만들기 및 속성
    - 여러가지 생성 함수
    - arange
    - shape / ndim / size / dtype읽는
"""

import numpy as np
from _data import load_one_stock

# 배열 만들기
print(f" np.array(배열) -> {np.array([52000, 51500, 53200])}")
print(f" np.zeros(5) -> {np.zeros(5)}")
print(f" np.ones(5) -> {np.ones(5)}")
print(f" np.full(5, 7) -> {np.full(5, 7)}")
print(f" np.empty(3) -> {np.empty(3)}")
""" np.empty(3) -> 초기화하지 않고 만듬, 이전 값(쓰레기 값)이 들어있을 수 있음 """

# 기본 dtype float64 이기 때문에 0, 1로 초기화 시 0. 1.으로 됨.
print(f" np.zeros(5, dtype='int64') -> {np.zeros(5, dtype='int64')}")

# arange
# : numpy의 range가 arange이다.
# # numpy.arange([start,] stop, [step,] dtype=Node) 
print(f" np.arange(0, 1, 0.25) -> {np.arange(0, 1, 0.25)} 길이 {len(np.arange(0, 1, 0.25))}")


# 속성 읽기
arr = np.array([52000, 51500, 53200, 52800])
print(f" arr = {arr}")
print(f" arr.shape = {arr.shape}")  # 배열의 모양을 튜플 형식으로 표현
print(f" arr.ndim(차원수) = {arr.ndim}")    # 차원 수
print(f" size = {arr.size}")    # 전체 갯수
print(f" dtype = {arr.dtype}")  # 요소의 타입

# 튜플의 (4,) 형태
print(f" arr.shape = {arr.shape}")
# 요소가 하나인 튜플은 파이썬 문법상 쉼표가 필요하다.
print(f" type((4)) = {type((4)).__name__}")
print(f" type((4,)) = {type((4,)).__name__}")

"""
    shape을 읽을 때
    (4,) -> 1차원, 요소가 4
    (4, 1) -> 2차원 / 4행 1열
    (1, 4) -> 2차원 / 1행 4열
    (120, 750) -> 2차원 / 120행 750열
"""

# reshape(shape) : [0, 1, 2, 3] 배열에서 꺼낸 shape모양으로 쪼개고 재 배치한다.
for shape in [(4,), (4,1), (1,4)]:
    a = np.arange(4).reshape(shape)
    print(f" shape = {str(shape)}, ndim = {a.ndim} {repr(a).replace(chr(10), ' ')}")

print()

# 실제 데이터 로드
prices = load_one_stock(0)

print(f" 첫 종목의 750일 종가")
print(f" shape = {prices.shape}")  # 배열의 모양을 튜플 형식으로 표현
print(f" ndim(차원수) = {prices.ndim}")    # 차원 수
print(f" size = {prices.size}")    # 전체 갯수
print(f" dtype = {prices.dtype}")  # 요소의 타입
print(f" 앞의 5개 데이터 : {prices[:5]}")








