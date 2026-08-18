"""
    입출력
    - print()
"""

print("=" * 30)
print("기본 출력")
print("=" * 30)

# 문자열은 따옴표('', "")로 감싸서 출력
print("hello python!!")

print('안녕 파이썬')

# 숫자는 따옴표 없이
print(100)
print(3.14)
print(10 + 20)

print("=" * 30)
print("여러 값을 동시에 출력 (,)로 구분")
print("=" * 30)

# 여러 값을 동시에 출력할 때는 ,로 구분
print("김일현", 30, "학생")
print("java", "sql", "python")

# 구분자를 변경하고 싶을 때 = sep옵션 부여
print("2026년", "8월", "18일")
print("2026년","8월","18일", sep="-")
print("김일현", 26, sep="님의 나이는 ")

print("=" * 30)
print("끝 문자 변경 (end 옵션)")
print("=" * 30)

# end: print출력 후 마지막에 출력할 문자 지정 옵션
print("첫번째 줄입니다.", end=" ")  # 기본인 개행 대신 공백을 한칸을 마지막에 넣겠다. (자동개행 안됨)
print("두번째 줄입니다.")

print("1+1=", end=" ")
print(2)

print("=" * 30)
print("이스케이프 문자")
print("=" * 30)

# 역슬래시(\)를 사용해서 이스케이프 문자를 작성할 수 있음
print("이번줄을 작성하고\n한줄 개행하고 싶다.")
print("이번줄을 작성하고\t한탭 개행하고 싶다.")

print("강사가 말했다 \"파이썬 재미있죠?\" ")

print("=" * 30)
print("문자 포맷팅")
print("=" * 30)

name = "김일현"
age = 26
height = 175.2

# Java의 printf()와 비슷한 방식
print("이름: %s, 나이: %d, 키: %.1f" % (name, age, height))

