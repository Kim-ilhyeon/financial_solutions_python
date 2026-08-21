"""
    공통 parser 모듈
"""
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from _config import BASE

# 특정 요소가 없을 때 에러가 발생하지 않도록 텍스트를 파싱하는 함수
# 텍스트 추출
def get_text(node, selector, default =""):
    """ 선택자에 해당하는 텍스트를 안전하게 추출 """
    tag = node.select_one(selector)
    # 만약 tag가 없으면 None이 반환 -> default값을 리턴
    return tag.get_text(strip=True) if tag else default

# 속성 추출
def get_attr(node, selector, attr, default=""):
    """ 선택자에 해당하는 요소의 속성이 없는 경우 안전하게 추출 """
    tag = node.select_one(selector)

    # 만약 tag가 없으면 None이 반환 -> default값을 리턴
    if not tag:
        return default

    return tag.get(attr, default)

# 숫자 추출
def get_number(node, selector, default=0):
    text = get_text(node, selector)
    digits = re.sub(r"[^\d]", "", text)  # 숫자가 아닌 문자를 전부 제거

    return int(digits) if digits else default

# 
def parse_rate(text, default=None):
    """ +3.5%  -1.7% 같은 값에서 부호를 유지한 실수를 뽑는다. """
    if not text:
        return default

    m = re.search(r"-?[\d.]+", text)    # 음수 부호까지 포함한 값 검사
    return float(m.group()) if m else default    # .group() 표현식 일치하는 값 추출

# 목록 parser
def parse_stocks(html):
    """ 종목 목록 html에서 행 단위로 데이터를 추출 """

    soup = BeautifulSoup(html, "lxml")
    results = []

    for row in soup.select("tr.stock-row"):
        results.append({
            "code": get_text(row, "td.col-code"),
            "name": get_text(row, "td.col-name"),
            "sector": get_text(row, "td.col-sector"),
            "price": get_number(row, "td.col-price"),
            "rate": parse_rate(get_text(row, "td.col-change")),
            "volume": get_number(row, "td.col-volume"),
            "link": urljoin(BASE, get_attr(row, "td.col-name a", "href")),
        })

    return results
