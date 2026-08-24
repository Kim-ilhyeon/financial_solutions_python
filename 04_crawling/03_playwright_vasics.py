import requests

from _config import BASE, HEADER, TIMEOUT

KEYWORD = "가온전자"

# ssr방식과 csr방식 호출

ssr = requests.get(f" {BASE}/stocks", headers=HEADER, timeout=TIMEOUT)
csr = requests.get(f" {BASE}/csr/stocks", headers=HEADER, timeout=TIMEOUT)


# 렌더링 방식에 따라서 <body>가 비어있을 수 있다.
# CSR일 때는 bs으로 파싱할 수 없다.
print(f" {'경로':<20}{'상태':<8}{'본문 길이':12} 키워드 포함 여부")
print(f" {'/stocks(SSR)':<20}{ssr.status_code:<8}{len(ssr.text):12}  {KEYWORD in ssr.text}")
print(f" {'/csr/stocks(CSR)':<20}{csr.status_code:<8}{len(csr.text):12}  {KEYWORD in csr.text}")


# csr본문 확인
for line in csr.text.strip().split("\n"):
    print(f" {line}")

# 데이터는 없고, root라는 데이터를 그려줄 공간만 들어있는 body가 리턴된다.

from playwright.sync_api import sync_playwright

# 기본구조
"""
    Browser     브라우저 프로세스
    Context     쿠키, 캐시 공간
    Page        탭
"""
# with를 쓴다는 것은 strim을 사용하여 데이터를 옮기는 통로를 사용하는 것을 생성하는 것이다.
# 사용 후에 strim을 닫아야 resource낭비가 없기 때문에 반납을 해주는 것이다.
with sync_playwright() as p:
    # browser : 크롬을 실제로 실행한다. -> 
    browser = p.chromium.launch(headless=True)

    # context : 시크릿창 하나를 띄우는 것과 같다. (그래서 쿠키, 캐시가 독립적으로 보관)
    # viewposrt : 창의 크기를 지정
    context = browser.new_context(
        locale="ko-KR",
        viewport={"width": 1280, "height": 800},
    )

    # 실제로 조작하기위한 탭을 하나 실행
    page = context.new_page()

    # page.route(패턴, 처리함수) : 특정 패턴의 요청을 가로채 직접 처리하는 함수
    # route.abort() : 요청을 취소
    # route.continue_(): 하려던 요청을 그대로 진행
    page.route(
        "**/*",
        lambda route : route.abort()
        if route.request.resource_type in {"image", "font", "media"}
        else route.continue_(),
    )

    # wait_until
    # domcontentloaded : HTML을 다 읽고 DOM트리가 만들어진 시점 (JS는 아직 실행 전)
    # load : 이미지까지 모든 리소스가 로드 - 느림(기본 값)
    # networkidel : 네트워크의 요청이 멈출때까지
    page.goto(f" {BASE}/csr/stocks", wait_until="domcontentloaded")

    # 해당 선택자가 DOM에 그려질 때까지 기다림.
    page.wait_for_selector("tr.stock-row")

    # 해당 선택자로 찾겠다.
    # count() : 찾은 선택자 갯수
    count = page.locator("tr.stock-row").count()


    # page.content() : DOM을 문자열로 리턴 = requests.text() 동작이 동일
    html = page.content()

    print(f" 렌더링 후 가져온 행 개수 : {count}")
    print(f" page.content : {html}")

    # with로 인해서 playwright는 반납이 자동으로 되지만, playwright를 통해 실행되는 브라우저는 꺼지지 않음
    # -> 그래서 브라우저를 따로 종료
    browser.close()


# 대기 전략
"""
    page.goto(url)

    time.sleep(5) : 5초 대기 (5초 뒤에는 응답이 올 것을 예상)
    html = page.content()

    - 네트워크가 느리면 5초 후에 가져올 수 있음 -> 실패..
    - 기본적으로 응답이 1초 이내라면 4초는 항상 낭비

    page.click("button.btn-add")    # "button.btn-add" 버튼이 나타날 때까지 기다림
    ~~ 행위

    명시적 대기
    page.wait_for_selector(선택자)                  # 나타날때까지
    page.wait_for_selector(선택자, state="hidden")  # 사라질때까지
    page.wait_for_load_state("networkidle")        # 네트워크 요청이 다 끝날때까지
    page.wait_for_timeout(100)      # 1초 고정대기
"""

from _parsers import parse_stocks

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(locale="ko-KR").new_page()

    # 대기 없이
    page.goto(f" {BASE}/csr/stocks", wait_until="domcontentloaded")
    without_wait = page.locator("tr.stock-row").count()

    page.wait_for_selector("tr.stock-row")
    with_wait = page.locator("tr.stock-row").count()

    print(f" 대기 없이 : {without_wait}")
    print(f" 대기 후 : {with_wait}")

    browser.close()

print("=" * 50)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(locale="ko-KR").new_page()

    page.route(
        "**/*",
        lambda route : route.abort()
        if route.request.resource_type in {"image", "font", "media"}
        else route.continue_()
    )

    page.goto(f" {BASE}/csr/stocks", wait_until="domcontentloaded")
    page.wait_for_selector("tr.stock-row")
    items = parse_stocks(page.content())

    browser.close()

for s in items[:5]:
    print(f'{s["code"]} : {s["name"]} : {s["price"]}')


"""
    1. headless=False, slow_mo=1000
    => 화면을 직접 보면서 확인할 수 있음.

    2. 스크린샷과 HTML 저장
    page.screenshot(path="~~~/debug.png", full_page=True)
    
    open("debug.html", "w", encoding="UTF-8".wirte(page.content()))

    3. 브라우저 콘솔
    page.on("console", lambda m : print(f" [BROWSER] {m.text}"))
"""




