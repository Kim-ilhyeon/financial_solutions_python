"""
    조건문
    - if / elif / else
    - 삼항 연산자
    - match-case
    - pass
"""

print("=" * 40)
print("if / elif / else")
print("=" * 40)

# Python에서 블록은 들여쓰기로 구분
# 조건식은 ()가 아니라 if 바로뒤에 사용하고 :으로 마무리
# else if가 아니라 elif로 작성
for score in [95, 85,72,45]:
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"

    print(f"{score}점 -> {grade}")

print()
print("들여쓰기가 곧 블록")
print()

value = 10

if value > 5:
    print("if문 안에 있는 줄")
    print("if문 안에 있는 줄")
    print("if문 안에 있는 줄")
print("if문 밖에 있는 줄")

print("=" * 40)
print("삼항 연산자")
print("=" * 40)

# String result = (age >= 20) ? "성인" : "미성년자"
# [참일 때] if [조건] else [거짓]

for age in [25, 15]:
    result = "성인" if age >= 20 else "미성년자"
    print(f"{age} -> {result}")

print("=" * 40)
print("match-case -> Java의 swtich")
print("=" * 40)

for status_code in [200, 404, 500, 302]:
    match status_code:
        case 200: 
            msg = "정상"
        case 404:
            msg = "페이지 찾을 수 없음"
        case 500:
            msg = "서버 에러"
        case _: # default
            msg = "알 수 없는 상태코드"
    print(f"{status_code} -> {msg}")
# match-case는 별도의 break가 필요없다.

print("=" * 40)
print("pass")
print("=" * 40)

# 내요잉 비어있는 블록을 만들 때 사용
score = 95

if score > 90:
    pass    # 나중에 구현 or 진짜 내용이 없을 때
else: 
    print("else블록은 실행")
