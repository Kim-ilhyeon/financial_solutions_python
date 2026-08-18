"""
    변수와 자료형
    - 기본 자료형 5가지
    - 다중 할당 값 교환
    - 타입 힌트와 상수 표기
"""

print("=" * 30)
print("변수 선언")
print("=" * 30)

# 타입을 지정하지 않는다 - 동적 타이핑
name = "김일현"
age = 26
height = 175.3
is_student = False
data = None # Java에서의 null과 같다.

print(name, age, height, is_student, data)

print("=" * 30)
print("기본 자료형 5가지")
print("=" * 30)

print(f"{name} : {type(name)}")
print(f"{age} : {type(age)}")
print(f"{height} : {type(height)}")
print(f"{is_student} : {type(is_student)}")
print(f"{data} : {type(data)}")
# str, int, float, bool, NoneType

value = 25
print(f"{value} : {type(value)}")
value = "스물다섯"
print(f"{value} : {type(value)}")

# 편리하지만 위험한 면이 있다.
# 보편적으로 한 변수에 한가지 타입만 담기로 한다.

print("=" * 30)
print("다중 할당과 값 교환")
print("=" * 30)

x, y, z = 1, 2, 3
print(f"x, y, z -> {x} {y} {z}")

a = b = c = 0
print(f"a, b, c -> {a} {b} {c}")

# java에서는 값 교환시에 tmp같은 중간 변수가 필요함.
x, y = y, x
print(f"x, y -> {x} {y}")

print("=" * 30)
print("타입 힌트")
print("=" * 30)

user_name: str = "김일현"
print(f"user_name : {user_name}")

# 타입 힌트를 어겨도 오류가 나지는 않는다.
wrong: int = "문자열입니다."
print(f"wrong : {wrong}")

print("=" * 30)
print("상수")
print("=" * 30)

# Python에는 final이 없음. 대문자로 변수명을 입력해서 약속만 함.
MAX_AGE = 100
print(f"MAX_AGE : {MAX_AGE}")
