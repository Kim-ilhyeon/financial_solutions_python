"""
    dtype
    - 오류가 발생하지 않더라도 잘 봐야할 것
"""

import numpy as np

# dtype의 주요 데이터 타입
# 정수 - int64
# 실수 - float64
# 참/거짓 - bool
# 객체 - object(파이썬 객체)

sample = [
    [1, 2, 3],
    [1.0, 2.0],
    [True, False],
    [1, 2.5],
    [1, "two"],
]

for s in sample:
    a = np.array(s)

    print(f" np.array({str(s)}) : dtype={a.dtype}")

# 타입이 섞이면 둘다 표현할 수 있는 범위의 타입으로 올라감
# 정수 + 실수 -> float64
# 숫자 + 문자 -> 문자(<U -> 유니코드 문자열)
# 이러한 과정을 UPCASTING이라고 한다.

# 정수 배열에는 np.nan를 넣을 수 없다.
int_arr = np.array([5200, 51500, 53200])
print(f"{int_arr} dtype= {int_arr.dtype}")

# int_arr[0] = np.nan     # Not a number
print(f" np.nan dtype= {type(np.nan).__name__}")
# nan는 실수형이다. 정수칸에 들어갈 수 없다.

int_arr2 = np.array([5200, np.nan, 53200])
print(f" {int_arr2} dtype= {int_arr2.dtype}")

# astype은 버림
# 지수표기(5.2009e+03)를 나오지 않게 해줌
np.set_printoptions(suppress=True)

f = np.array([5200.9, 5199.2, -3.7])
print(f" 원본 : {f}")
print(f" astype(int) : {f.astype('int64')}")
print(f" 반올림 후 astype(int) : {np.round(f).astype('int64')}")

# dtype이 object일 때

dirty = np.array([52000, 51500, "53,200"])
print(f" -> {dirty}")
print(f" -> {dirty.dtype}")

# dirty.mean()
# 숫자여야할 열의 dtype이 object이거나 문자열이라면
# 그 열에 숫자가 아닌 값이 섞여있다.
# -> 데이터 정제가 필요하다.

cleaned = np.array([str(x).replace(",", "") for x in dirty]).astype("int64")
print(f" {cleaned} dtype= {cleaned.dtype}")
print(f" mean(평균) = {cleaned.mean()}")


