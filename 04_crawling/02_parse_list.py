"""
    목록파싱 - list[dict]
"""

import requests
import re
import csv
import json
from bs4 import BeautifulSoup
from _config import BASE, TIMEOUT, HEADER
from _parsers import get_text, get_attr, get_number, parse_rate, parse_stocks

response = requests.get(f"{BASE}/stocks", headers=HEADER, timeout=TIMEOUT)

response.raise_for_status()  # 상태코드가 200이 아니면 예외를 발생

html = response.text

soup = BeautifulSoup(html, "lxml")

row = soup.select_one("tr.stock-row")

# row.select_one("td.test") 해당하는 클래스가 없을 때
try :
    row.select_one("td.test").get_text
except Exception as e:
    print(f" 에러 : {e}")

print(f" {get_text(row, 'td.test', '없음')}")

# 컨테이너 단위로 순회하기
names = soup.select("td.col-name")
prices = soup.select("td.col-price")

# 지금은 갯수가 같아서 zip으로 묶어도 딱 맞아 떨어짐.
# 하지만 갯수가 보장되는 것은 아니다. 만약 이름과 가격의 수가 다르면 매칭이 섞일 수 있음.
print(f" 전체에서 따로 뽑으면 : 이름 {len(names)}개, 가격 {len(prices)}개")

for row in soup.select("tr.stock-row"):
    names = get_text(row, "td.col-name")
    prices = get_number(row, "td.col-price")

print()

# 텍스트 정제 - 정규 표현식
cases = [
    ("  71,200 $ ", "가격"),
    ("+2.35% ", "등락률(양수)"),
    ("-1.04% ", "등락률(음수)"),
    ("12,340,567", "거래량"),
]

for text, label in cases:
    if "%" in text:
        value = parse_rate(text)
    else:
        digits = re.sub(r"[^\d]", "", text)
        value = int(digits) if digits else None

    print(f" {text!r:<16} {str(value):<16} {label}")


# stock 데이터 추출 함수화
stocks = parse_stocks(html)

print(f" {'코드':<8}{'종목명':<12}{'섹터':<10}{'현재가':>12}{'등락률':>8}")

for s in stocks:
    print(f" {s['code']:<8}{s['name']:<12}{s['sector']:<10}{s['price']:>12}{s['rate']:>8}")


# 파일로 저장
# json, 
# csv -> 상품명, 가격, 재고,
#        맥북, 1500000, 10

def save_csv(data, path):
    if not data:
        return

    with open(path, "w", newline="", encoding="UTF-8") as f:
        # dict를 그대로 한 행으로 쓸다. 컬럼 순서는 fieldnames으로 정함
        writer = csv.DictWriter(f, fieldnames=data[0].keys())

        # csv파일 맨 첫 줄에 컬럼 이름 씀
        writer.writeheader()

        # 딕셔너리 리스트 전체를 각 행으로 기록
        writer.writerow(data)

# 경로를 따로 지정하지 않으면 지금 실행되는 프로젝트 위치에 저장됨
save_csv(stocks, "stocks.csv")

def save_json(data, path):
    with open(path, "w", encoding="UTF-8") as f :
        json.dump(data, f, ensure_ascii=False, indent=2)

save_json(stocks, "stocks.json")

