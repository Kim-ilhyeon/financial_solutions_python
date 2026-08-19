"""
    컴프리헨션
    - 리스트 컴프리헨션
    - 딕셔너리 / 집합 컴프리헨션

    : 리스트, 딕셔너리, set같은 데이터 구조를 간결하고, 직관적으로 생성하는 문법
"""

result = []
for n in range(1,6):
    result.append(n * n)

print(f" result = {result}")

# 컴프리헨션 구조 : [표현식 for 변수 in 반복대상 if 조건]
result = [n * n for n in range(1,6)]
print(f" result = {result}")

nums = [1,2,3,4,5,6]
print(f" nums : {nums}")
print(f" 짝수만 : {[n for n in nums if n % 2 == 0]}")
print(f" 3보다 큰 값 : {[n for n in nums if n > 3]}")







