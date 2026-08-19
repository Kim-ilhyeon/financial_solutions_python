"""
    파이썬 함수 기본
    - def로 함수 정의
    - 반환값과 None
    - 다중 반환
"""

print("=" * 40)
print("함수 정의 방법")
print("=" * 40)

def greet(name):
    return f"{name}님 안녕하세요."

print(greet("김수민"))
print(greet("박지호"))

# 반환값이 없는 함수 -> 반환값 : None
def show(msg):
    print(f"메시지 : {msg}")
    # return 없음

result = show("hi")
print(f"반환값 : {result}")

print()

# 다중 반환 - 반환 값이 여러 개일 때
def calc(a, b):
    return a+b, a-b, a*b

result = calc(10, 5)
print(f"결과 : {result}")
print(f"결과 : {type(result)}")

print()

# 언패킹해서 받기
add, sub, mul = calc(10, 5)
print(f"덧셈 : {add}")
print(f"뺼셈 : {sub}")
print(f"곱셈 : {mul}")

print("=" * 40)
print("docstring - 해당 함수가 어떤 역할을 하는지 설명문구를 작성하는 법")
print("=" * 40)

def calc_tax(price: int, rate: float = 0.1) -> int:
    """
    부가세를 포함한 최종금액은 다음과 같다
    args:
        price : 공금가액
        rate : 세율(기본값은 0.1)
    return : 
        부가세가 포함된 금액(정수)
    """
    return int(price * (1 + rate))

print(f"calc_tax(10000) = {calc_tax(10000):,}")
help(calc_tax)
# help함수에 함수를 넣어주면 해당 함수의 대한 설명을 출력해준다.

print("=" * 40)
print("함수는 정의 후에만 사용이 가능하다.")
print("=" * 40)

# 파이썬은 위에서 아래로 한줄씩 실행된다.
# 정의 전에는 함수 호출이 불가하다. (호이스팅 없음)

# print(f"{later()}")
def later():
    return "나중에 정의한 함수"
print(f"{later()}")








