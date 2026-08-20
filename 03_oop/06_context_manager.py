"""
    with문
    - 파일, 네트워크 연결, 스레드 락 같은 자원을 다룰 때 작업이 끝난 후 자원을 자동으로 처리해주는 컨텍스트 매니저

    - 파일 다루기

"""
import os       # 운영체제와 상호작용해서 파일 경로를 탐색하거나 , 기렉토리를 생성 / 삭제, 환경변수 조회등을 할 수 있는 모듈이다.
import json     # json형태의 데이터를 딕셔너리/리스트로 변환하거나 반대로 객체를 json으로 파싱할 때 사용하는 모듈 (직렬화/역직렬화)

# __file__ : 현재 실행중인 파이썬 파일의 경로
# 실행중인 파일이 있는 폴더 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TXT_PATH = os.path.join(BASE_DIR, "_demo.txt")
JSON_PATH = os.path.join(BASE_DIR, "_demo.json")

print(f" {BASE_DIR}")
print(f" {TXT_PATH}")
print(f" {JSON_PATH}")

# 파일 쓰기와 읽기
with open(TXT_PATH, "w", encoding="UTF-8") as f:
    f.write("삼성전자, 005123, 71200\n")
    f.write("SK하이닉스, 006023, 1700000\n")

print(f" 저장 완료 {os.path.basename(TXT_PATH)}")

with open(TXT_PATH, "r", encoding="UTF-8") as f:
    context = f.read()

print("context 전체 읽기")
for line in context.strip().split("\n"):
    print(f" {line}")

# json 저장 읽기
stocks = [
    {"code" : "005123", "name" : "삼성전자", "price" : 71200},
    {"code" : "006023", "name" : "SK하이닉스", "price" : 1700000},
]

with open(JSON_PATH, "w", encoding="UTF-8") as f:
    # dump() : 딕셔너리 -> json문자열
    json.dump(stocks, f, ensure_ascii=False, indent=2)

print(f" 저장완료 {os.path.basename(JSON_PATH)}")

print()

with open(JSON_PATH, "r", encoding="UTF-8") as f:
    loaded = json.load(f)

for s in loaded:
    print(f" {s['name']} : {s['price']}")
