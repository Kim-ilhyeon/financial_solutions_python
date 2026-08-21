"""
    BeautifulSoup
    - HTML 및 XML문서에서 원하는 데이터를 쉽게 추출할 수 있도록 해주는 스크래핑 라이브러리

    1. requests로 요청 후 문자열(HTML / XML)을 응답 받음.
    2. bs4의 find, select를 이용하여 특정 택스트를 추출. 
"""

import requests
from bs4 import BeautifulSoup
from _config import BASE, TIMEOUT, HEADER

response = requests.get(f"{BASE}/stocks", headers=HEADER, timeout=TIMEOUT)

response.raise_for_status()  # 상태코드가 200이 아니면 예외를 발생

html = response.text

print(f"{BASE}/stocks []{response.status_code} {len(html):,}자")

# 문자열 -> 태그 구조
# requests가 전달한 값은 그냥 긴 문자열이다.

# bs4은 이 문자열을 DOM트리처럼 다룰 수 있게 만들어 줌.
soup = BeautifulSoup(html, "lxml")
print(f"\n soup.title.text : {soup.title.text if soup.title else '(없음)'}")

# js -> document.querySelector와 같은 bs이 한다.

# select : css선택자를 그대로 사용. 선택자로 전부 가져옴. 못찾으면 []로 가져옴
# select_one : 선택자로 1개만 가져옴. 못찾으면 None가져옴
rows_select = soup.select('tr.stock-row')

print(f" tr.stock-row 갯수 : {len(rows_select)}")

# 택스트 꺼내서 사용하기
first = soup.select_one("tr.stock-row")
price_tag = first.select_one("td.col-price")

print(f" .text :  {price_tag.text}")
print(f" .get_text() :  {price_tag.get_text()}")
print(f" .get_text(strip=True) :  {price_tag.get_text(strip=True)}")
print()

# !r을 붙여주면 따옴표를 붙여서 가져온다. (개행문자나 띄어쓰기를 모두 인식하여 가져옴)
print(f" .text :  {price_tag.text!r}")
print(f" .get_text() :  {price_tag.get_text()!r}")
print(f" .get_text(strip=True) :  {price_tag.get_text(strip=True)!r}")
# 공백을 제거하고 가져오는것이 비교시에도 좋은데 strip=True속성을 사용할 수 있는 get_text를 권장한다.

# 속성을 꺼내야 한다 - get()
link = first.select_one("td.col-name a")

# 속성값은 없을 수도 있기 때문에 get()사용 권장
print(f" link['href'] : {link['href']}")
print(f" link.get('href') : {link.get('href')}")    # 권장
print(f" link.get('href', '없음') : {link.get('href', '없음')}")    # 권장
print()

# 첫번째 행 전체 꺼내보기
for sel in ["td.col-code", "td.col-name a", "td.col-sector", "td.col-price", "td.col-change", "td.col-volume"]:
    tag = first.select_one(sel)
    value = tag.get_text(strip=True) if tag else "(없음)"
    print(f" {sel:<20} {value}")
