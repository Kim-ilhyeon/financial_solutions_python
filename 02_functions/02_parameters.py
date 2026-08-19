"""
    파이썬 함수의 매개변수
"""

print("=" * 40)
print("기본 매개변수")
print("=" * 40)

def connect(host, port=8080, charset="UTF-8"):
    print(f"접속완료 : {host}:{port}({charset})")

connect("localhost")
connect("localhost", 3306)
connect("localhost", 3306, "EUCKR")
# 기본값을 많이 사용하는 매개변수일수록 매개변수의 순서 뒤쪽으로 배치한다. (기본값이 없는 경우에는 앞으로)

print()

print("=" * 40)
print("키워드 인자")
print("=" * 40)

# 순서와 무관하게 이름으로 전달
connect(port=3306, host="127.0.0.1")

print("=" * 40)
print("args - 위치 인자를 튜플(순서기반)로")
print("=" * 40)

def total(*nums):
    print(f" 받은 값 : {nums} ({type(nums)})")
    return sum(nums)

print(f"total(1,2,3) = {total(1,2,3)}")
print(f"total() = {total()}")

print("=" * 40)
print("**args - 위치 인자를 딕셔너리(키-값 기준)로")
print("=" * 40)

def create_user(**info):
    print(f"받은 값 : {info} ({type(info)})")
    for key, value in info.items():
        print(f" {key} : {value}")

create_user(name="김일현", age=26, city="시흥시")

def log(level, *messages, **options):
    print(f" level: {level}")
    print(f" messages: {messages}")
    print(f" options: {options}")

log("INFO", "서버시작", "포트 8080...", timestamp=True, color="green")



