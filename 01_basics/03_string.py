"""
    문자열 다루기
    - 주요 메소드 (split, join, replace, strip)
    - 인덱싱과 슬라이싱
"""

print("=" * 40)
print("인덱싱, 슬라이싱")
print("=" * 40)

str = "Python Programming"
print(f"str = '{str}'")
print(f"문자열의 인덱스는 0부터 시작 : 0123456789...")
print()
print(f"str[0] = {str[0]}")
print(f"str[-1] = {str[-1]}")

# 슬라이싱 str[초기인덱스:끝인덱스+1:건너뛸갯수] 건너뛸갯수의 기본은 1
print(f"str[0:6] = {str[0:6]}") # 0이상 6미만
print(f"str[0:6] = {str[:6]}") # 시작값 생략 시 0부터 시작
print(f"str[0:6] = {str[7:]}") # 미만값 생략 시 끝까지 실행
print(f"str[0:6] = {str[:]}") # 처음부터 끝까지
print(f"str[0:6] = {str[::2]}") # 2칸씩 건너뛰기
print(f"str[0:6] = {str[::-1]}") # -1입력 시 역순으로 출력 

print("=" * 40)
print("문자열 주요 메소드")
print("=" * 40)

str = "  Hello Python World  "
print(f"원본    : [{str}]")
print(f"strip()    : [{str.strip()}]") # 좌우 공백 제거 (Java에서의 trim()과 동일)
print(f"upper()   : [{str.upper()}]") # 대문자 변환
print(f"upper()   : [{str.upper()}]") # 소문자 변환
print(f"replace()     : [{str.replace('Python', 'java')}]") # 치환
print(f"split()   : [{str.split(',')}]") # 특정 문자로 자르기 (잘라서 배열로)
print(f"'-'.join([...])      : [{'-'.join(['2026', '08','18'])}]")  # 문자열로 합치기
print()
print(f"str.count('l')  : [{str.count('l')}]") # 찾아서 갯수 반환
print(f"str.find('Python')  : [{str.find('Python')}]") # 찾아서 시작 인덱스 반환, 없으면 -1

# 문자열 메소드는 원본을 변경하지 않는다.
str.split(',')
print(str)
str2 = str.split(',')
print(str2)

# 여러 줄 문자열 사용
str3 = """
문자열 다루기
- 주요 메소드 (split, join, replace, strip)
- 인덱싱과 슬라이싱
"""

print(f"str3:{str3}")
