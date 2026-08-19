"""
    딕셔너리 (dict)
    - key-value 구조
    - 추가 / 수정 / 삭제 / 순회
"""

# api응답(json) -> 곧 딕셔너리 구조이다.

# 생성과 조회 방법
user = {
    "name" : "김일현",
    "age" : 26,
    "skills" : ["java", "sql", "python"],
}

print(f" user = {user}")
print(f" user['name'] = {user['name']}")
print(f" user['skills'] = {user['skills']}")

# [key]로 가져오거나 get(key)로 가져오기 가능
print(f" user.get('name') : {user.get('name')}")
print(f" user.get('skills') : {user.get('skills')}")
print(f" user.get('phone') : {user.get('phone')}")
print(f" user.get('phone') : {user.get('phone', '없음')}")  # get은 기본 값 설정 가능

# print(f" user['phone'] = {user['phone']}") # 로 가져올 시 해당 키값이 없을 경우 None이 아니라 에러 발생함

print()

# 추가 / 수정 / 삭제
user = {
    "name" : "김일현",
    "age" : 26,
}

# 추가
user['email'] = "kimilheon@naver.com"
print(f" user['email'] : {user['email']}")

# 수정
user['age'] = 40
print(f" user['age'] : {user['age']}")

# 삭제
del user['email']
print(f" user.get('email') : {user.get('email')}")

print()

# 전체 탐색
user = {
    "name" : "김일현",
    "age" : 26,
    "skills" : ["java", "sql", "python"],
}

for key in user:
    print(f" {key} : {user[key]}")

for key, value in user.items():
    print(f" {key} : {value}")

print()
print(f" keys() : {list(user.keys())}")
print(f" values() : {list(user.values())}")
print(f" items() : {list(user.items())}")   # (key, value)형태의 튜플 목록
