"""
    형 변환
    - 문자 <-> 숫자 변환
    - bool타입 변환과 False로 간주되는 값
"""

print("=" * 30)
print("문자열 -> 숫자")
print("=" * 30)

print(f'int("100") = {int("100")}')
print(f'float("3.14") = {float("3.14")}')

# 문자열이 실수 형태이면 바로 int로 변경이 안된다.
print(f'int("3.14") = {int(float("3.14"))}')

print("=" * 30)
print("숫자 -> 문자열")
print("=" * 30)

print(f'str(1000) + 원 : {str(1000) + "원"}')

# 숫자와 문자열은 +로 이을 수 없다.
price = 1000
print(f"{price}원")

print("=" * 30)
print("bool타입 변환 Falsy값")
print("=" * 30)

falsy_values = [0, 0.0, '\"\"', [], (), {}, set(), None, False]
truthy_values = [1, -1, '\"0\"', '\"False\"', [0], '\" \"']

print("거짓으로 취급되는 값")
for v in falsy_values:
    print(f"{str(v) : <10} -> {bool(v)}")

print("=" * 40)

print("참으로 취급되는 값")
for v in truthy_values:
    print(f"{str(v) : <10} -> {bool(v)}")


