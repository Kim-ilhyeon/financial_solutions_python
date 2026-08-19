"""
    람다식과 고차함수
    - lambda (익명함수)
    - map / filter
    - sorted
    - reduce
    - any / all / sum / max
"""
from functools import reduce

print("=" * 40)
print("lambda - 익명함수")
print("=" * 40)

def double_def(x):
    return x*2

# lambda 매개변수 : 반환식
# js의 화살표 함수와 유사 x => x*2
# 1종변수 = 변수에 함수를 담을 수 있다.
double_lambda = lambda x : x*2
print(f"일반 함수 : {double_def(5)}")
print(f"람다 함수 : {double_lambda(5)}")
# => 함수를 매개변수로 넘길 떄를 위해 사용

print("=" * 40)
print("map / filter")
print("=" * 40)

nums = [1,2,3,4,5,6]

# map : 전달한 함수로 새로운 값을 만들어서 배열을 반환
doubled = list(map(lambda n : n*2,nums))
print(f" map(2배) : {doubled}")

# filter : 전달한 함수의 결과가 true인 값만 남김
even = list(filter(lambda n : n%2==0, nums))
print(f" filter(짝수) : {even}")

# map/filter는 이터레이터를 반환됨. list()로 감싸야 확인이 가능 (이터레이터 = 반복자)

print("=" * 40)
print("sorted - 정렬")
print("=" * 40)

nums = [30,10,25,7]
print(f" sorted() : {sorted(nums)}")
print(f" sorted() : {sorted(nums, reverse=True)}")

students = [
    {"name" : "김일현", "score" : 75},
    {"name" : "김이현", "score" : 65},
    {"name" : "김삼현", "score" : 90},
    {"name" : "김삼현", "score" : 80},
]

# 객체 정렬 시에는 sorted(배열, key=정렬기준람다식)

# 점수 내림차순 정렬
print("=" * 30, "내림차순", "=" * 30)
by_score = sorted(students, key=lambda s : s["score"])
for s in by_score:
    print(f" {s['name']} : {s['score']}점")

# 점수 오름차순 정렬
print("=" * 30, "오름차순", "=" * 30)
by_score_rev = sorted(students, key=lambda s : s["score"], reverse=True)
for s in by_score_rev:
    print(f" {s['name']} : {s['score']}점")

#  이름 가나다순 정렬
print("=" * 30, "이름 가나다순", "=" * 30)
for s in sorted(students, key=lambda s : s["name"]):
    print(f" {s['name']} : {s['score']}점")

# 여러 기준으로 정렬 가능
print("=" * 30, "이름 가나다순 + 점수 내림차순", "=" * 30)
for s in sorted(students, key=lambda s : (s["name"], s["score"])):
    print(f" {s['name']} : {s['score']}점")

print()


print("=" * 40)
print("reduce - 반복하며 누적값을 구할 때")
print("=" * 40)

nums = [10, 20, 30]

# 데이터를 처음부터 끝까지 돌면서 누적계산을 수행하는 함수
# acc : 지금까지 누적된 누적 값
# cur : 이번 순서에서 가져온 값
total = reduce(lambda acc, cur : acc + cur, nums, 0)
print(f" total : {total}")

strList = ["가", "나다", "라마바", "사아자차"]
# 가장 긴 문자열을 구하고 싶다.
longest = reduce(lambda a, b : a if len(a) >= len(b) else b, strList)
print(f" 가장 긴 문자열 : {longest}")

# 자주 사용하는 내장 함수
nums = [3,1,4,1,6,9]
print(f"len() = {len(nums)}")
print(f"sum() = {sum(nums)}")
print(f"max() = {max(nums)}")
print(f"min() = {min(nums)}")

print()

print(f"any() = {any(n > 8 for n in nums)}") # 하나라도 8보다 큰 수가 들어있다면 true
print(f"any() = {all(n > 8 for n in nums)}") # 모두 8보다 큰 수가 들어있어야 true



