"""
    반복문
    - for
    - range / enumerate / zip
    - while
    - break / continue / for-else
"""

print("=" * 40)
print("for문은 항상 for-each")
print("=" * 40)

# Java의 for (String m : messages) -> Python의 for문
members = ["김일현", "김이현", "김삼현"]

for m in members:
    print(f"{m}님 안녕하세요.")

print()
for ch in "Python":
    print(ch, end=" ")
print()

print("=" * 40)
print("range(n, n-1, step)")
print("range(시작, 끝, 증감수)")
print("=" * 40)

print(f"range(5) -> {list(range(5))}")
print(f"range(1,6) -> {list(range(1,6))}")
print(f"range(0,10) -> {list(range(0,10))}")
print(f"range(0,10,2) -> {list(range(0,10,2))}")
print(f"range(5,0,-1) -> {list(range(5,0,-1))}")

print("=" * 40)
print("enumerate() - 번호랑 값 함께)")
print("=" * 40)

for i in range(len(members)):
    print(f"{i}번 : {members[i]}")

print()

# start지정으로 i의 시작값을 지정할 수 있다.
for i, name in enumerate(members, start=1):
    print(f"{i}번 : {name}")

print("=" * 40)
print("zip() - 여러 리스트를 동시에")
print("=" * 40)

names = ["삼성전자", "sk하이닉스", "카카오"]
today = [230000, 1600000, 200000]
yesterday = [220000, 1500000, 40000]

for name, now, prev in zip(names, today, yesterday):
    diff = now - prev
    print(f"{name:<10} : {now:>8}원 ({diff})")

print()

for i, (name,now) in enumerate(zip(names, today), start=1):
    print(f"{i} : {name} ({now}원)")

print("=" * 40)
print("while")
print("=" * 40)

count = 0
while count < 5:
    print(f"count : {count}")
    count += 1  # 탈출에 관련된 증감식

print("=" * 40)
print("break / continue / for-else")
print("=" * 40)

# 탈출을 위한 break
n = 1
while True:
    if n > 3:
        break
    print(f"n = {n}")
    n += 1

print()

print("1~10중 홀수만 출력, 단 7을 넘으면 중단")

for i in range(1, 11):
    if i % 2 == 0:  # 짝수면 넘김
        continue
    elif i > 7: # 7넘으면 중단
        break
    else:
        print(f"{i}")

print()
# for-else : break없이 끝까지 반복을 했을 때만 else 실행
for m in members:
    if m == "김일현":
        print("찾았습니다.")
        break

print()

for m in members:
    if m == "김명현":
        print("찾았습니다.")
        break
else:
    print("찾는 회원이 없습니다.")
    