# TODO 부분을 직접 채워 완성하세요.
# 실행부(맨 아래)는 그대로 두면 됩니다. 함수만 완성하면 결과가 출력됩니다.



# =========================================================================
# PRACTICE 1. 다중 반환 + docstring          [01_function_basic]
#   문장을 받아 (전체 글자수, 공백 제외 글자수, 단어수) 를 튜플로 반환한다.
#   빈 문자열이거나 공백만 있으면 (0, 0, 0)
#
#   [출력 예시]
#     analyze_text("파이썬 함수 실습 입니다") -> (13, 10, 4)
#
#   [힌트] return 에 콤마로 나열하면 자동으로 튜플이 된다.
#          공백 제외 글자수는 replace(" ", "") 후 len()
#          단어수는 split() 의 결과 길이. split() 은 연속 공백도 알아서 처리한다.
#          docstring(Args/Returns)도 반드시 작성할 것.
#          (docstring이 없으면 help()가 위 주석을 대신 보여준다. 작성 후 다시 확인해 볼 것)
# =========================================================================
def analyze_text(text: str) -> tuple:
    # TODO: docstring 작성 (Args / Returns)
    """
    문장의 글자 수와 단어 수를 계산하는 함수
    """

    # TODO: 공백만 있는 경우 처리
    if not text.strip():
        return 0, 0, 0

    # TODO: 세 값을 계산해 튜플로 반환
    total_chars = len(text)
    no_space = len(text.replace(" ", ""))
    word_leng = len(text.split()) 
    return total_chars, no_space, word_leng


# =========================================================================
# PRACTICE 2. 기본값 매개변수 + 키워드 인자   [02_parameters]
#   호스트 정보를 받아 URL 문자열을 만들어 반환한다.
#     port 가 None 이면 포트를 붙이지 않는다.
#     path 가 "/" 로 시작하지 않으면 앞에 "/" 를 붙여준다.
#
#   [출력 예시]
#     make_url("example.com")                          -> https://example.com/
#     make_url("localhost", "api/users", port=8000)    -> https://localhost:8000/api/users
#
#   [힌트] 기본값이 있는 매개변수는 반드시 뒤쪽에 온다.
#          startswith("/") 로 검사한 뒤 문자열을 이어 붙이면 된다.
# =========================================================================
def make_url(host: str, path: str = "/", protocol: str = "https", port: int | None = None) -> str:
    """호스트 정보로 URL 문자열을 만들어 반환한다."""
    # TODO: path 앞에 "/" 보정
    if not path.startswith("/"):
        path = "/" + path

    # TODO: port 유무에 따라 URL 조립 후 반환
    if port is None:
        return f"{protocol}://{host}{path}"

    return f"{protocol}://{host}:{port}{path}"


# =========================================================================
# PRACTICE 3. *args                          [02_parameters]
#   경로 조각을 개수 제한 없이 받아 "/" 로 이어 붙인 문자열을 반환한다.
#     빈 문자열이나 공백만 있는 조각은 건너뛴다.
#     조각이 하나도 없으면 "" 를 반환한다.
#
#   [출력 예시]
#     join_path("api", "v1", "users")  -> "api/v1/users"
#     join_path("data", "", "raw")     -> "data/raw"
#     join_path()                      -> ""
#
#   [힌트] *parts 는 전달된 위치 인자들을 튜플로 묶어 받는다.
#          쓸 조각만 빈 리스트에 append 로 모은 뒤 "/".join(리스트) 로 합친다.
#          (컴프리헨션은 아직 배우지 않았으므로 for 문으로 작성할 것)
# =========================================================================
def join_path(*parts: str) -> str:
    """경로 조각들을 "/" 로 이어 붙여 반환한다."""
    # TODO: 빈 리스트를 만들고, 쓸 조각만 골라 담기
    usable = []

    for part in parts:
        p = part.strip()
        if p:           # ""과 " " 전부 걸러짐
            usable.append(p)

    # TODO: "/" 로 합쳐서 반환
    return "/".join(usable)


# =========================================================================
# PRACTICE 4. **kwargs                       [02_parameters]
#   이름과 임의의 추가 정보를 받아 프로필을 출력한다.
#
#   [출력 예시]
#     [최지원]
#       age: 25
#       city: 서울
#
#     추가 정보가 없으면
#     [김지원]
#       (추가 정보 없음)
#
#   [힌트] **extra 는 키워드 인자들을 딕셔너리로 묶어 받는다.
#          extra.items() 로 (키, 값) 을 함께 꺼내 반복한다.
# =========================================================================
def build_profile(name: str, **extra) -> None:
    """이름과 임의의 추가 정보를 받아 프로필을 출력한다."""
    # TODO: 이름 줄 출력
    print(f"[{name}]")

    # TODO: 추가 정보가 없으면 안내 문구 출력 후 종료
    if extra is None:
        print(f"(추가 정보 없음)")
        return

    # TODO: items() 로 순회하며 한 줄씩 출력
    for key, value in extra.items():
        print(f" {key}: {value}")


# =========================================================================
# PRACTICE 5. 가변 객체와 원본 보존           [03_scope]
#   아래 unsafe_append 는 이미 작성되어 있다. 원본 리스트를 직접 바꾼다.
#   safe_append 는 원본을 건드리지 않고 '새 리스트'를 만들어 반환하도록 작성한다.
#
#   [힌트] 새 빈 리스트를 만들고 for 문으로 기존 값을 옮겨 담은 뒤,
#          마지막에 새 값을 append 하고 return 한다.
#          함수 안의 대입(=)은 지역이지만, 전달받은 객체를 수정하면 원본이 바뀐다.
# =========================================================================
def unsafe_append(items: list, value) -> None:
    """(비교용) 전달받은 리스트를 직접 수정한다. 원본이 바뀐다."""
    items.append(value)


def safe_append(items: list, value) -> list:
    """원본을 바꾸지 않고 value 가 추가된 새 리스트를 반환한다."""
    # TODO: 새 리스트에 기존 값 복사
    copy_items = list(map(lambda s : s, items))

    # TODO: 새 값 추가 후 반환
    copy_items.append(value)
    return copy_items


# =========================================================================
# PRACTICE 6. 스코프 - global 과 권장 방식     [03_scope]
#   같은 "누적" 동작을 두 가지 방식으로 만들어 비교한다.
#     add_global(n)        : 전역 변수 total 을 직접 증가시킨다 (global 사용)
#     add_safe(current, n) : 값을 받아 더한 결과를 반환한다 (전역을 건드리지 않음)
#
#   [힌트] global 없이 total = total + n 을 쓰면 UnboundLocalError 가 난다.
#          add_safe 는 반환값을 다시 대입해서 쓴다 -> n = add_safe(n, 5)
#
#   [생각해 볼 것] 아래 실행부의 출력이 어떻게 나올지 먼저 예측해 보고 실행할 것.
# =========================================================================
total = 0    # 전역 변수


def add_global(n: int) -> None:
    """전역 변수 total 을 n 만큼 증가시킨다."""
    # TODO: global 선언 후 total 증가
    global total
    total += n


def add_safe(current: int, n: int) -> int:
    """current 에 n 을 더한 결과를 반환한다. 전역 변수는 건드리지 않는다."""
    # TODO: 더한 값을 반환
    return current + n


# =========================================================================
# PRACTICE 7. sorted + key=lambda (다중 기준)  [04_lambda_hof]
#   상품 리스트를 '카테고리 오름차순 -> 같은 카테고리면 가격 내림차순' 으로
#   정렬한 새 리스트를 반환한다. 원본은 그대로 두어야 한다.
#
#   [힌트] 기준이 두 개면 key 에서 튜플을 반환한다.
#          내림차순 기준이 숫자 하나뿐이면 -값 을 이용하면 한 번에 해결된다.
#          reverse=True 는 '모든 기준'을 뒤집으므로 여기서는 쓰면 안 된다.
#          sorted() 는 원본을 바꾸지 않고 새 리스트를 반환한다. (sort() 와 비교)
# =========================================================================
def sort_products(products: list[dict]) -> list[dict]:
    """카테고리 오름차순, 가격 내림차순으로 정렬한 새 리스트를 반환한다."""
    # TODO: sorted 와 lambda 로 한 줄 작성
    array_product = sorted(products, key=lambda p : (p["category"], -p["price"]))
    # => 비교 값이 숫자인 경우 내림차순은 -로 가능

    return array_product


# =========================================================================
# PRACTICE 8. map / filter / all              [04_lambda_hof]
#   섭씨 온도 리스트를 받아 다음 세 값을 튜플로 반환한다.
#     ① 화씨로 변환한 리스트 (소수 1자리 반올림)   -> map
#     ② 영하(0도 미만)인 섭씨 온도만 모은 리스트   -> filter
#     ③ 모든 온도가 영상(0도 초과)인지 여부         -> all
#
#   [출력 예시]
#     analyze_temps([12.5, -3.0, 0.0, 25.4, -7.2])
#       -> ([54.5, 26.6, 32.0, 77.7, 19.0], [-3.0, -7.2], False)
#
#   [힌트] 화씨 = 섭씨 * 9 / 5 + 32,  반올림은 round(값, 1)
#          map / filter 는 이터레이터를 반환하므로 list() 로 감싸야 한다.
#          all(...) 안에는 04에서 본 제너레이터 표현식을 써도 된다.
# =========================================================================
def analyze_temps(temps: list[float]) -> tuple:
    """섭씨 리스트를 받아 (화씨 리스트, 영하 리스트, 모두 영상인가) 를 반환한다."""
    # TODO: ① map 으로 화씨 변환
    fahrenheit = list(map(lambda c : round(c * 9 / 5 + 32, 1), temps))

    # TODO: ② filter 로 영하만 추출
    zero = list(filter(lambda c : c < 0, temps))

    # TODO: ③ all 로 전체 영상 여부 판정 후 튜플 반환
    all_zero = all(c > 0 for c in temps)
    return fahrenheit, zero, all_zero


# =========================================================================
# 실행부 - 수정하지 말 것
# =========================================================================
if __name__ == "__main__":

    print("=" * 60)
    print(" PRACTICE 1. 다중 반환 + docstring")
    print("=" * 60)
    print(analyze_text("파이썬 함수 실습 입니다"))   # 기대: (13, 10, 4)
    print(analyze_text("hello"))                      # 기대: (5, 5, 1)
    print(analyze_text("   "))                        # 기대: (0, 0, 0)
    print("\n--- help(analyze_text) ---")
    help(analyze_text)

    print("\n" + "=" * 60)
    print(" PRACTICE 2. 기본값 매개변수 + 키워드 인자")
    print("=" * 60)
    print(make_url("example.com"))
    # 기대: https://example.com/
    print(make_url("localhost", "api/users", port=8000))
    # 기대: https://localhost:8000/api/users
    print(make_url("test.com", protocol="http", path="login"))
    # 기대: http://test.com/login

    config = {"host": "data.go.kr", "path": "/service", "port": 443}
    print(make_url(**config))   # ** 로 딕셔너리 펼쳐 전달
    # 기대: https://data.go.kr:443/service

    print("\n" + "=" * 60)
    print(" PRACTICE 3. *args")
    print("=" * 60)
    print(repr(join_path("api", "v1", "users")))   # 기대: 'api/v1/users'
    print(repr(join_path("data", "", "raw")))      # 기대: 'data/raw'
    print(repr(join_path("  ", "logs")))           # 기대: 'logs'
    print(repr(join_path()))                       # 기대: ''

    parts = ["static", "img", "logo.png"]
    print(repr(join_path(*parts)))                 # 기대: 'static/img/logo.png'

    print("\n" + "=" * 60)
    print(" PRACTICE 4. **kwargs")
    print("=" * 60)
    build_profile("최지원", age=25, city="서울")
    build_profile("김지원")

    info = {"age": 30, "job": "개발자", "city": "부산"}
    build_profile("박지원", **info)

    print("\n" + "=" * 60)
    print(" PRACTICE 5. 가변 객체와 원본 보존")
    print("=" * 60)
    origin = [1, 2, 3]
    unsafe_append(origin, 99)
    print(f"unsafe_append 후 원본 : {origin}")      # 기대: [1, 2, 3, 99]

    origin = [1, 2, 3]
    result = safe_append(origin, 99)
    print(f"safe_append 반환값    : {result}")      # 기대: [1, 2, 3, 99]
    print(f"safe_append 후 원본   : {origin}")      # 기대: [1, 2, 3]

    print("\n" + "=" * 60)
    print(" PRACTICE 6. 스코프")
    print("=" * 60)
    add_global(5)
    add_global(3)
    print(f"global 방식  : total = {total}")        # 기대: 8

    n = 0
    n = add_safe(n, 5)
    n = add_safe(n, 3)
    print(f"권장 방식    : n = {n}")                # 기대: 8

    print("\n" + "=" * 60)
    print(" PRACTICE 7. sorted + key=lambda")
    print("=" * 60)
    products = [
        {"name": "노트북", "category": "전자", "price": 1200000},
        {"name": "마우스", "category": "전자", "price": 35000},
        {"name": "책상", "category": "가구", "price": 250000},
        {"name": "의자", "category": "가구", "price": 250000},
        {"name": "키보드", "category": "전자", "price": 89000},
    ]
    ordered = sort_products(products)
    if ordered:
        for p in ordered:
            print(f"  {p['category']} | {p['name']} | {p['price']:,}원")
    # 기대 순서: 책상, 의자, 노트북, 키보드, 마우스
    print(f"  원본 첫 항목 : {products[0]['name']}")   # 기대: 노트북 (원본 유지)

    print("\n" + "=" * 60)
    print(" PRACTICE 8. map / filter / all")
    print("=" * 60)
    print(analyze_temps([12.5, -3.0, 0.0, 25.4, -7.2]))
    # 기대: ([54.5, 26.6, 32.0, 77.7, 19.0], [-3.0, -7.2], False)
    print(analyze_temps([10.0, 20.0]))
    # 기대: ([50.0, 68.0], [], True)