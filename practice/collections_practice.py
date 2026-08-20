"""
TODO 부분을 직접 채워 완성하세요.
실행부(맨 아래)는 그대로 두면 됩니다. 함수만 완성하면 결과가 출력됩니다.
"""

import copy


# =========================================================================
# PRACTICE 1. 정렬 + 슬라이싱 + 원본 보존        [05_list]
#   종목 리스트에서 가격이 높은 순으로 상위 n개의 '이름'만 뽑아 반환한다.
#     price 가 없는 항목은 0원으로 취급한다.
#     종목 수보다 n 이 커도 오류 없이 있는 만큼만 반환한다.
#     원본 리스트의 순서는 바뀌면 안 된다.
#
#   [출력 예시]
#     top_n_by_price(stocks, 3) -> ['현대차', 'SK하이닉스', '삼성전자']
#
#   [힌트] sorted() 는 새 리스트를 반환하고, sort() 는 원본을 바꾼다.
#          숫자 하나짜리 내림차순은 key 에서 -값 을 쓰면 간단하다.
#          price 가 없을 수 있으므로 s["price"] 대신 s.get("price", 0).
#          상위 n개는 슬라이싱 [:n] 으로 자른다. 개수가 모자라도 오류가 없다.
# =========================================================================
def top_n_by_price(stocks: list[dict], n: int = 3) -> list[str]:
    """가격 상위 n개 종목의 이름 리스트를 반환한다. 원본은 바뀌지 않는다."""
    # TODO: 가격 내림차순으로 정렬한 새 리스트 만들기
    ordered_stocks = sorted(stocks, key=lambda s : -s.get('price', 0))

    # TODO: 앞에서 n개만 자르고, 이름만 모아서 반환
    ordered_stocks = ordered_stocks[:n]

    return [s.get('name', "이름 없음") for s in ordered_stocks]

# =========================================================================
# PRACTICE 2. 2차원 리스트                       [05_list]
#   행렬(모든 행의 길이가 같다)을 받아 '열별 합계' 리스트를 반환한다.
#     빈 행렬이면 [] 를 반환한다.
#
#   [출력 예시]
#     column_sums([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) -> [12, 15, 18]
#
#   [힌트] 빈 리스트에 matrix[0] 을 하면 IndexError 가 나므로 먼저 걸러낸다.
#          열 개수는 len(matrix[0]) 이다.
#          [0] * 열개수 로 0 이 채워진 리스트를 먼저 만들어 두고 더해 나간다.
#          바깥 for 는 행, 안쪽 for 는 열 인덱스(range)로 돈다.
# =========================================================================
def column_sums(matrix: list[list[int]]) -> list[int]:
    """2차원 리스트의 열별 합계 리스트를 반환한다."""
    # TODO: 빈 행렬 처리
    if not matrix:
        return []

    # TODO: 0으로 채운 합계 리스트 만들기
    # => 열 갯수만큼 0으로 채운 리스트 생성
    # [0] * n을하면 0으로 채워진 n개짜리 리스트가 생성됨
    sums = [0] * len(matrix[0])
    # sums = [0 for _ in range(len(martrix[0]))]

    # TODO: 행을 돌면서 각 열에 더한 뒤 반환
    for m in matrix:
        for i in range(len(m)):
            sums[i] += m[i]

    return sums


# =========================================================================
# PRACTICE 3. 튜플 반환과 언패킹                 [06_tuple]
#   "코드,이름,가격" 한 줄을 (code, name, price) 튜플로 파싱해 반환한다.
#     각 필드의 앞뒤 공백은 제거한다.
#     필드가 3개가 아니거나 가격이 숫자가 아니면 None 을 반환한다.
#     가격은 int 로 변환한다.
#
#   [출력 예시]
#     parse_record("005930, 삼성전자 ,71200") -> ('005930', '삼성전자', 71200)
#     parse_record("000660,SK하이닉스")       -> None
#
#   [힌트] line.split(",") 로 나눈 뒤 len() 으로 개수를 먼저 확인한다.
#          개수를 확인했다면 code, name, price = fields 로 언패킹할 수 있다.
#          try/except 대신 문자열의 isdigit() 으로 숫자인지 검사한다.
#          return 에 콤마로 나열하면 자동으로 튜플이 된다.
# =========================================================================
def parse_record(line: str) -> tuple | None:
    """CSV 한 줄을 (코드, 이름, 가격) 튜플로 반환한다. 형식이 틀리면 None."""
    # 005930, 삼성전자, 71200
    # TODO: 콤마로 나누고 필드 개수 확인
    fields = line.split(",")
    if len(fields) != 3:
        return None
    code, name, price = fields

    # TODO: 언패킹 후 공백 제거
    code = code.strip()
    name = name.strip()
    price = price.strip()

    # TODO: 가격이 숫자인지 검사하고 튜플로 반환
    if price.isdigit():
        return None

    return code, name, int(price)


# =========================================================================
# PRACTICE 4. 딕셔너리 집계 패턴  ★★★          [07_dict]
#   거래 목록을 종목명별로 집계한다.
#     total_by_name : {종목명: 금액합계}   (amount 가 없으면 0으로 취급)
#     count_by_name : {종목명: 등장횟수}
#
#   [출력 예시]
#     total_by_name(trades) -> {'삼성전자': 1068000, 'SK하이닉스': 370000, '카카오': 0}
#     count_by_name(trades) -> {'삼성전자': 2, 'SK하이닉스': 1, '카카오': 1}
#
#   [힌트] result[name] = result.get(name, 0) + 더할값
#          result[name] += 값 으로 쓰면 첫 등장에서 KeyError 가 난다.
#          두 함수는 '더하는 값'만 다르고 구조가 완전히 같다.
#          이 패턴은 앞으로 수없이 반복되므로 손에 익혀둘 것.
# =========================================================================
def total_by_name(trades: list[dict]) -> dict:
    """종목명별 금액 합계 딕셔너리를 반환한다."""
    # TODO: 빈 딕셔너리에서 시작해 get(name, 0) 패턴으로 누적
    result = {}

    for trade in trades:
        name = trade.get('name', '이름없음')
        amount = trade.get('amount', 0)
        result[name] = 
    pass


def count_by_name(trades: list[dict]) -> dict:
    """종목명별 등장 횟수 딕셔너리를 반환한다."""
    # TODO: 같은 패턴으로 1씩 누적
    pass


# =========================================================================
# PRACTICE 5. 중첩 구조와 get() 체이닝  ★★★     [07_dict]
#   API 응답에서 종목 목록을 꺼내 {"name", "price"} 형태로 정리해 반환한다.
#     응답 구조 : {"status": 200, "data": {"items": [ {...}, ... ]}}
#     data 나 items 가 아예 없을 수도 있다 -> 이때는 []
#     name 이 없으면 "이름없음", price 가 없으면 0
#
#   [출력 예시]
#     extract_items(response)         -> [{'name': '삼성전자', 'price': 71200}, ...]
#     extract_items({"status": 500})  -> []
#
#   [힌트] response["data"]["items"] 는 중간이 비면 KeyError 로 죽는다.
#          response.get("data", {}).get("items", []) 처럼 이어 붙인다.
#          기본값을 {} 로 주는 것이 핵심이다. None 이면 다음 get() 에서 죽는다.
# =========================================================================
def extract_items(response: dict) -> list[dict]:
    """응답에서 종목 목록을 꺼내 {"name", "price"} 리스트로 정리해 반환한다."""
    # TODO: get() 을 이어 붙여 items 안전하게 꺼내기

    # TODO: 각 항목을 name/price 만 담은 딕셔너리로 만들어 반환
    pass


# =========================================================================
# PRACTICE 6. 집합 - 중복 제거와 차집합          [08_set]
#   dedup_keep_order : 순서를 유지하면서 중복을 제거한 리스트를 반환
#   pick_new_urls    : 이번에 발견한 URL 중 아직 수집하지 않은 것만 정렬해 반환
#
#   [출력 예시]
#     dedup_keep_order(["a.com","b.com","a.com","c.com"]) -> ['a.com','b.com','c.com']
#     pick_new_urls({"a.com","b.com"}, {"b.com","c.com","d.com"}) -> ['c.com','d.com']
#
#   [힌트] list(set(urls)) 는 순서가 보장되지 않는다.
#          seen 이라는 set 을 따로 두고, 처음 보는 값만 리스트에 append 한다.
#          '이미 봤는가' 검사는 list 가 아니라 set 으로 해야 빠르다.
#          차집합은 found - collected. set 은 순서가 없으므로 sorted() 로 반환한다.
# =========================================================================
def dedup_keep_order(urls: list[str]) -> list[str]:
    """순서를 유지하면서 중복을 제거한 리스트를 반환한다."""
    # TODO: seen 집합과 결과 리스트를 만들고 순회하며 채우기
    pass


def pick_new_urls(collected: set, found: set) -> list[str]:
    """아직 수집하지 않은 URL 만 정렬해 반환한다."""
    # TODO: 차집합을 구해 정렬 후 반환
    pass


# =========================================================================
# PRACTICE 7. 컴프리헨션 - 필터 if 와 삼항 if  ★ [09_comprehension]
#   clean_prices : "1,000" 같은 문자열 목록을 정수 리스트로 정제한다.
#                  빈 문자열과 공백만 있는 값은 버린다.
#   label_prices : 가격마다 기준가 이상이면 "고가", 아니면 "저가" 라벨을 붙인다.
#
#   [출력 예시]
#     clean_prices(["1,000","2,500","","3,200","  "]) -> [1000, 2500, 3200]
#     label_prices([1000, 2500, 3200])                -> ['저가', '고가', '고가']
#
#   [힌트] 걸러내려면 if 가 뒤에 (else 불가), 값을 바꾸려면 if 가 앞에 (else 필수).
#          if p 만 쓰면 "  "(공백)이 통과해 int() 에서 죽는다. if p.strip() 이 정답.
#          콤마 제거는 replace(",", "").
#   [생각해 볼 것] 두 함수의 결과 '개수'가 왜 다르게 나오는지 설명해 볼 것.
# =========================================================================
def clean_prices(raw: list[str]) -> list[int]:
    """문자열 가격 목록을 정수 리스트로 정제해 반환한다."""
    # TODO: 리스트 컴프리헨션 한 줄 (필터 if 는 뒤에)
    pass


def label_prices(prices: list[int], standard: int = 2000) -> list[str]:
    """기준가 이상이면 "고가", 아니면 "저가" 라벨 리스트를 반환한다."""
    # TODO: 리스트 컴프리헨션 한 줄 (삼항 if 는 앞에, else 필수)
    pass


# =========================================================================
# PRACTICE 8. 딕셔너리 / 집합 컴프리헨션         [09_comprehension]
#   to_length_map  : 이름 리스트 -> {이름: 글자수} 딕셔너리
#   unique_lengths : 이름들의 글자수 '종류'를 오름차순 리스트로 반환
#
#   [출력 예시]
#     to_length_map(["박하", "김"])  -> {'박하': 2, '김': 1}
#     unique_lengths(["박하", "김"]) -> [1, 2]
#
#   [힌트] {key: value for ...} 는 dict 컴프리헨션, {value for ...} 는 set 컴프리헨션.
#          set 은 중복이 자동으로 사라지지만 순서가 없으므로 sorted() 로 반환한다.
# =========================================================================
def to_length_map(names: list[str]) -> dict:
    """{이름: 글자수} 딕셔너리를 반환한다."""
    # TODO: dict 컴프리헨션 한 줄
    pass


def unique_lengths(names: list[str]) -> list[int]:
    """중복 없는 글자수를 오름차순 리스트로 반환한다."""
    # TODO: set 컴프리헨션으로 글자수 모으기

    # TODO: 정렬해서 반환
    pass


# =========================================================================
# PRACTICE 9. 얕은 복사 vs 깊은 복사  ★★★       [10_copy]
#   아래 add_tag_unsafe 는 이미 작성되어 있다. 원본의 tags 까지 바꿔 버린다.
#   add_tag_safe 는 원본을 건드리지 않고 태그가 추가된 '새' 데이터를 반환한다.
#     이미 같은 태그가 있으면 중복해서 추가하지 않는다.
#
#   [힌트] data.copy() 는 바깥 리스트만 새로 만들고 안의 dict 는 원본과 공유한다.
#          중첩 구조를 완전히 분리하려면 copy.deepcopy(data) 를 써야 한다.
#          tags 가 아예 없는 항목도 있을 수 있으니 item.get("tags", []) 로 꺼낸다.
#
#   [생각해 볼 것] 실행부에서 unsafe 와 safe 의 결과가 어떻게 다를지 먼저 예측할 것.
# =========================================================================
def add_tag_unsafe(data: list[dict], tag: str) -> list[dict]:
    """(비교용) 얕은 복사만 해서 원본이 훼손되는 버전이다."""
    result = data.copy()

    for item in result:
        item["tags"].append(tag)     # 안쪽 dict 는 원본과 공유 중!

    return result


def add_tag_safe(data: list[dict], tag: str) -> list[dict]:
    """태그가 추가된 새 데이터를 반환한다. 원본은 바뀌지 않는다."""
    # TODO: 깊은 복사로 원본과 완전히 분리

    # TODO: 각 항목의 tags 에 tag 추가 (중복이면 건너뛰기) 후 반환
    pass


# =========================================================================
# 실행부 - 수정하지 말 것
# =========================================================================
if __name__ == "__main__":

    print("=" * 60)
    print(" PRACTICE 1. 정렬 + 슬라이싱 + 원본 보존")
    print("=" * 60)
    stocks = [
        {"code": "005930", "name": "삼성전자", "price": 71200},
        {"code": "000660", "name": "SK하이닉스", "price": 185000},
        {"code": "035720", "name": "카카오", "price": 42150},
        {"code": "005380", "name": "현대차", "price": 238000},
        {"code": "068270", "name": "셀트리온"},              # price 가 없다!
    ]
    print(top_n_by_price(stocks, 3))
    # 기대: ['현대차', 'SK하이닉스', '삼성전자']
    print(top_n_by_price(stocks, 10))
    # 기대: ['현대차', 'SK하이닉스', '삼성전자', '카카오', '셀트리온']
    print(top_n_by_price(stocks))
    # 기대: ['현대차', 'SK하이닉스', '삼성전자']   (기본값 n=3)
    print(f"원본 첫 항목 : {stocks[0]['name']}")   # 기대: 삼성전자 (원본 유지)

    print("\n" + "=" * 60)
    print(" PRACTICE 2. 2차원 리스트")
    print("=" * 60)
    print(column_sums([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))   # 기대: [12, 15, 18]
    print(column_sums([[10, 20], [30, 40], [50, 60]]))      # 기대: [90, 120]
    print(column_sums([]))                                   # 기대: []

    print("\n" + "=" * 60)
    print(" PRACTICE 3. 튜플 반환과 언패킹")
    print("=" * 60)
    print(parse_record("005930, 삼성전자 ,71200"))
    # 기대: ('005930', '삼성전자', 71200)
    print(parse_record("000660,SK하이닉스"))       # 기대: None (필드 부족)
    print(parse_record("035720,카카오,없음"))      # 기대: None (가격이 숫자가 아님)

    record = parse_record("005380, 현대차 , 238000 ")
    if record:
        code, name, price = record                 # 튜플 언패킹
        print(f"{code} {name} {price:,}원")        # 기대: 005380 현대차 238,000원

    print("\n" + "=" * 60)
    print(" PRACTICE 4. 딕셔너리 집계 패턴")
    print("=" * 60)
    trades = [
        {"name": "삼성전자", "amount": 712000},
        {"name": "SK하이닉스", "amount": 370000},
        {"name": "삼성전자", "amount": 356000},
        {"name": "카카오"},                                   # amount 가 없다!
    ]
    print(total_by_name(trades))
    # 기대: {'삼성전자': 1068000, 'SK하이닉스': 370000, '카카오': 0}
    print(count_by_name(trades))
    # 기대: {'삼성전자': 2, 'SK하이닉스': 1, '카카오': 1}

    print("\n" + "=" * 60)
    print(" PRACTICE 5. 중첩 구조와 get() 체이닝")
    print("=" * 60)
    response = {
        "status": 200,
        "data": {
            "count": 3,
            "items": [
                {"code": "005930", "name": "삼성전자", "price": 71200},
                {"code": "000660", "name": "SK하이닉스"},      # price 가 없다!
                {"code": "035720", "name": "카카오", "price": 42150},
            ],
        },
    }
    items = extract_items(response)
    if items:
        for item in items:
            print(f"  {item['name']:<10} {item['price']:>8,}원")
    # 기대: 삼성전자 71,200원 / SK하이닉스 0원 / 카카오 42,150원

    print(extract_items({"status": 500}))                # 기대: []  (data 자체가 없다)
    print(extract_items({"status": 200, "data": {}}))    # 기대: []  (items 가 없다)

    print("\n" + "=" * 60)
    print(" PRACTICE 6. 집합 - 중복 제거와 차집합")
    print("=" * 60)
    urls = ["a.com", "b.com", "a.com", "c.com", "b.com", "a.com"]
    print(dedup_keep_order(urls))
    # 기대: ['a.com', 'b.com', 'c.com']

    collected = {"a.com", "b.com"}
    found = {"b.com", "c.com", "d.com"}
    print(pick_new_urls(collected, found))
    # 기대: ['c.com', 'd.com']

    print("\n" + "=" * 60)
    print(" PRACTICE 7. 컴프리헨션 - 필터 if 와 삼항 if")
    print("=" * 60)
    raw = ["1,000", "2,500", "", "3,200", "  ", "12,000"]
    prices = clean_prices(raw)
    print(prices)                        # 기대: [1000, 2500, 3200, 12000]
    if prices:
        print(label_prices(prices))      # 기대: ['저가', '고가', '고가', '고가']
        print(label_prices(prices, 3000))  # 기대: ['저가', '저가', '고가', '고가']

    print("\n" + "=" * 60)
    print(" PRACTICE 8. 딕셔너리 / 집합 컴프리헨션")
    print("=" * 60)
    names = ["최지원", "김지원", "이지원", "박하", "김", "이하늘"]
    print(to_length_map(names))
    # 기대: {'최지원': 3, '김지원': 3, '이지원': 3, '박하': 2, '김': 1, '이하늘': 3}
    print(unique_lengths(names))
    # 기대: [1, 2, 3]

    print("\n" + "=" * 60)
    print(" PRACTICE 9. 얕은 복사 vs 깊은 복사")
    print("=" * 60)
    original = [
        {"name": "삼성전자", "tags": ["반도체", "대형주"]},
        {"name": "카카오", "tags": ["플랫폼"]},
    ]
    backup = copy.deepcopy(original)          # 실험 전 원본을 따로 보관해 둔다

    add_tag_unsafe(original, "KOSPI")
    print(f"unsafe 사용 후 원본 : {original[0]['tags']}")
    # 기대: ['반도체', '대형주', 'KOSPI']   <- 원본이 훼손됐다

    original = copy.deepcopy(backup)          # 원상 복구
    tagged = add_tag_safe(original, "KOSPI")
    if tagged:
        print(f"safe 반환값         : {tagged[0]['tags']}")
        # 기대: ['반도체', '대형주', 'KOSPI']
        print(f"safe 사용 후 원본   : {original[0]['tags']}")
        # 기대: ['반도체', '대형주']   <- 원본은 그대로
        print(f"원본과 결과가 다른 객체인가 : {original[0]['tags'] is not tagged[0]['tags']}")
        # 기대: True