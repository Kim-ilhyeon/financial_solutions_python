"""
    튜플(tuple)
    - 불변성
    - 요소가 1개일 때 주의
"""

# 튜플 생성 방식
point = (10, 20)
point2 = 10, 20

single = (10,)  # 요소가 1개일 때 콤마(,) 필수
single2 = (10)  # 그냥 10, 튜플x, int

print(f" point = {point} {type(point)}")
print(f" point2 = {point2} {type(point2)}")
print(f" single = {single} {type(single)}")
print(f" single2 = {single2} {type(single2)}")

print()

# 불변성 - 수정이 안됨
print(f" point[0] = {point[0]}")
# point[0] = 99 # 리스트와 다르게 인덱스로 접근은 가능하지만 수정은 불가능함

# 새로 튜플을 만드는 것은 가능
point = (99, 20)
print(f" point[0] = {point[0]}")

print()

# 언패킹
x, y = (10, 20)
print(f" x, y = (10, 20) -> {x} {y}")

def get_numbers():
    return 10, 20

x, y = get_numbers()    # 튜플의 언패킹이다.

# 튜플의 일부만 받고 싶을 떄에는 관례적으로 _를 사용한다.
x, _, y = (10, 20, 30)
print(f" _ : {_}")

# *를 활용해서 나머지 값을 한 번에 받을 수 있다.
head, *rest = (1,2,3,4,5)
print(f" head : {head}, *rest : {rest}")

print()

#   튜플            VS      리스트
#   변경x                    변경o
#   ()                      []
#   속도가 빠름              속도가 느림
#   dict의 key로 사용 가능   dict의 key로 사용 불가능

# 튜플은 변하지 않으므로 dict의 key로 사용이 가능한거다.
location_names = {
    (35.5451, 126.9750) : "서울역",
    (35.5450, 126.9050) : "부산역",
}

print(f" 좌표를 키로 사용 : {location_names[(35.5450, 126.9050)]}")

# 데이터가 자주 변한다. -> 리스트 사용
# 데이터가 고정적이다.  -> 튜플 사용
# 함수가 여러 값을 반환 -> 튜플 사용 (자동으로 됨)
# dict의 key로 사용   -> 튜플 사용
