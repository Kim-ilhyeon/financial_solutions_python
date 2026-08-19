"""
    스코프
    - 지역 변수와 전역변수
    - global키워드
"""

print("=" * 40)
print("함수 안에서 만든 변수는 함수 밖에서 안 보인다.")
print("=" * 40)

count = 0 # 전역변수

def increase_wrong():
    count = 10 # 지역변수가 선언됨 (만들어짐)
    print(f"함수 안 : conut = {count}")

increase_wrong()
print(f"함수 밖 : count = {count}") # 전역변수를 함수 내부에서 컨트롤하지 않는다.

# global - 전역변수를 명시적으로 사용가능
# 값이 어디서 변경되는지 추적하기 어려워지므로 권장하지 않음.
def increase_global():
    global count
    count += 1

increase_global()
increase_global()
print(f"global 사용 후 : count = {count}")

# 변수를 찾는 순서
# 지역 => 밖 => 전역
name = "전역"

def outer():
    name = "바깥 함수"

    def inner():
        name = "안쪽 함수"
        print(f"inner에서 확인하는 name : {name}")

    inner()
    print(f"outer에서 확인하는 name : {name}")

outer()
print(f"전역에서 확인하는 name : {name}")
