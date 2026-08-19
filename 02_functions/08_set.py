"""
    set
    - 중복 제거
    - 집합 연산
"""

# 생성방법

nums = {1,2,3,3,3,4,2}

print(f" nums : {1,2,3,3,3,4,2} -> {nums}")

# 빈 자료구조 생성 시에는 set()을 사용하여 만들어야 함. {}는 빈 딕셔너리이다.
empty_set = set()
empty_dict = {}

print()

# 값을 잠시 set자료구조에 넣었다가 꺼내면 -> 중복 제거
nums = [1,2,3,3,3,4,2]
print(f" 원본 : {nums}")
print(f" 중복제거 : {set(nums)}")
print(f" 중복제거 후 다시 리스트로 변환 : {list(set(nums))}")

print()

# 집합 연산
a = {1,2,3,4}
b = {3,4,5,6}

print(f" a|b 합집합 = {a|b}")
print(f" a&b 교집합 = {a&b}")
print(f" a-b 차집합 = {a-b}")
print(f" a^b 대칭 차집합 = {a^b}")

# 값을 추가하거나 삭제
s = {1, 2}
print(f" s : {s}")

s.add(3)
print(f" s : {s}")

s.update([4, 5])
print(f" s : {s}")

s.discard(1)    # 해당 값을 없앰
print(f" s : {s}")
s.discard(99)    # 없는 값을 없애도 에러x
print(f" s : {s}")
