"""
    연산자
    - 산술 연산자
    - 비교 논리 연산자
    - 복합대입 연산자
"""

print("=" * 40)
print("산술 연산자")
print("=" * 40)

print(f"7 + 3 = {7 + 3}")
print(f"7 - 3 = {7 - 3}")
print(f"7 * 3 = {7 * 3}")
print(f"7 / 3 = {7 / 3}")   # Java는 2(몫), Python은 실수
print(f"7 // 3 = {7 // 3}") # java에서의 /와 같이 몫을 구함
print(f"7 % 3 = {7 % 3}")
print(f"7 ** 3 = {7 ** 3}") # 거듭제곱

print()
print(f"type(6 / 3) = {type(6 / 3)}") # 실제로 값이 딱 나누어 떨어지더라도 타입은 실수(float)이다.
print(f"(6 / 3) = {6 / 3}") # 실제로 값이 딱 나누어 떨어지더라도 타입은 실수(float)이다.

print(f"(-7 / 3) = {-7 / 3}")
print(f"(-7 // 3) = {-7 // 3}") # Java는 버림이지만 Python은 내림

print("=" * 40)
print("비교와 논리 연산자")
print("=" * 40)

a, b = 10, 20
print(f"a, b = {a} {b}")
print(f"a == b = {a == b}")
print(f"a != b = {a != b}")
print(f"a > b = {a > b}")
print(f"a < b = {a < b}")

print()

# Java에서는 &&(and) ||(or) -> Python에서는 and, or로 표기
# !연산은 not으로 작성
print(f"True and True : {True and True}")
print(f"True and False : {True and False}")
print(f"True or True : {True or True}")
print(f"True or False : {True or False}")
print(f"not False : {not False}")

print("=" * 40)
print("연쇄 비교 가능")
print("=" * 40)

score = 85

# Java : if (score >= 80 && score < 90), Python : if 80 <= score < 90:
if 80 <= score < 90:
    print(f"점수가 {score}로 80이상 90미만입니다. -> B학점")

print(f"1 < 2 < 3 : {1 < 2 < 3}")

print("=" * 40)
print("in(멤버십)과 is(식별)")
print("=" * 40)

members = ["김일현", "김이현", "김삼현"]
print(f"members = {members}")
print(f"'김일현' in members : {'김일현' in members}")
print(f"'김일현' in members : {'김명현' not in members}")
print(f"'ll' in \"Hello\" : {'ll' in "Hello"}")

print()

# ==은 값을 비교함, is를 통한 비교는 같은 객체인지를 비교함 (Java에서의 equals와 동일)
x = [1, 2, 3]
y = [1, 2, 3]
z = x

print(f"x = {x}, y = {y}, z = {z}")
print(f"x == y : {x == y}") # ==은 배열의 값을 비교
print(f"x is y : {x is y}") # is는 객체의 주소를 비교
print(f"x is z : {x is z}")

# None 비교 시에는 반드시 is를 사용함
data = None
data2 = None
print(f"data is None : {data is None}")
print(f"data is not None : {data is not None}")

print("=" * 40)
print("복합 대입 연산자")
print("=" * 40)

x = 10
print(f"x = {x}")

x += 5 # x = x + 5
print(f"x = {x}")

x -= 5 # x = x - 5
print(f"x = {x}")

x *= 5 # x = x * 5
print(f"x = {x}")

x //= 5 # x = x // 5
print(f"x = {x}")

