"""
Pandas 데이터 결합·집계 실습문제
나뉘어 저장된 표 다섯 장을 붙여 분석용 통합 데이터를 만든다.

TODO 부분을 채워 완성하세요.
맨 아래 실행부와 validate() 는 그대로 두면 됩니다.
"""

import unicodedata

import pandas as pd

from _data import (load_prices, load_companies, load_sectors, load_financial)

# 화면 표시 설정. 표가 줄바꿈되지 않게 넓힌다. 데이터가 아니라 보이는 방식만 바꾼다.
pd.set_option("display.width", 140)


# =========================================================================
# PRACTICE 1. 키 정제
#   종목 마스터(raw)의 키가 오염돼 있다. merge 는 키가 '완전히 같을 때만' 붙는다.
#   사람 눈에 같아 보여도 소용없다. 붙기 전에 다듬는다.
#
#     · name   : 전각 문자를 반각으로 바꾸고, 공백을 전부 없앤다
#                (앞뒤 공백 8건, 중간 공백 8건, 전각 문자 1건이 들어 있다)
#     · market : 대문자로 통일하고 앞뒤 공백을 없앤다
#     · code   : 이 파일에서는 이미 깨끗하지만 같은 규칙을 걸어 둔다
#
#   [기대 결과]
#     행 수 122 그대로
#     market 종류 5종 -> 2종  ['GX-GROWTH', 'GX-MAIN']
#     companies.csv 와 이름이 맞는 건수 106 -> 122
#
#   [힌트] 전각 -> 반각 : unicodedata.normalize("NFKC", 문자열)
#            pandas 함수가 아니라 파이썬 표준 라이브러리다. 문자열 하나를 받는다.
#            Series 에 적용하려면 s.map(lambda x: ...) 로 값 단위로 풀어 준다.
#          공백 제거   : s.str.replace(r"\s+", "", regex=True)
#            r"\s+" 는 '공백 한 칸 이상'. 앞뒤·중간이 한 번에 지워진다.
#            strip() 만 쓰면 '아람데이  터' 같은 중간 공백이 남는다.
#          대소문자    : s.str.upper()
#          원본을 건드리지 않으려면 맨 앞에서 raw.copy() 부터 한다.
#
#   ★ 순서에 함정이 있다.
#     전각 공백(U+3000)은 NFKC 를 거쳐야 보통 공백이 된다.
#     공백을 먼저 지우면 전각 공백이 살아남아 그대로 통과한다.
# =========================================================================
def clean_master(raw: pd.DataFrame) -> pd.DataFrame:
    """키가 정제된 새 DataFrame 을 반환한다. 행 수는 그대로다."""
    # TODO: 복사본을 만들고 name·market·code 를 각각 정제해 반환
    pass


# =========================================================================
# PRACTICE 2. 마스터 중복 제거
#   마스터는 120종목이어야 하는데 122행이다. code 가 두 번 나오는 종목이 있다.
#   먼저 들어온 행을 원본으로 보고 남긴다.
#
#   [기대 결과]
#     122행 -> 120행       code 가 유일해진다
#
#   [힌트] df.drop_duplicates(subset=["기준열"], keep="first")
#            반환은 중복 행이 빠진 '새 DataFrame' 이다. 원본은 그대로 남는다.
#          걸러내면 인덱스가 띄엄띄엄 남는다. reset_index(drop=True) 로 다시 매긴다.
#          유일한지 확인 : df["code"].is_unique  -> True / False
#
#   ★ 120행짜리 작은 표의 중복 2건이 90,000행을 오염시킨다.
#     시세 한 행이 마스터 두 행과 각각 짝을 지어 그 두 종목만 행이 두 배가 된다.
#     90,000행이 91,500행이 되는데(2종목 x 750일) 에러도 경고도 없다.
#     이 단계를 건너뛰면 PRACTICE 3 의 validate 가 막아 선다.
# =========================================================================
def dedup_master(df: pd.DataFrame) -> pd.DataFrame:
    """code 가 유일한 마스터를 반환한다."""
    # TODO: 중복 제거 후 인덱스를 0부터 다시 매겨 반환
    pass


# =========================================================================
# PRACTICE 3. 3단 조인
#   시세에 종목 정보를, 다시 섹터 이름을 붙인다.
#     prices -> master -> sectors
#
#   조건 세 가지
#     · 시세 90,000행이 하나도 늘거나 줄지 않아야 한다
#     · master 에서는 code · name · sectorCode · market 네 열만 가져온다
#     · sectors 를 붙이기 전에 code/name 을 sectorCode/sector 로 바꿔 둔다
#
#   [기대 결과]
#     90,000행 그대로     열 9개 -> 13개
#     name 결측 0건       sector 결측 6,750건  ← 0이 아니다. PRACTICE 4 에서 다룬다
#
#   [힌트] 붙이기   : 왼쪽표.merge(오른쪽표, on="키열", how="left")
#            ★ how 를 생략하면 inner 다. 짝이 없는 행이 에러 없이 사라진다.
#              "왼쪽은 전부 남긴다" 는 의도라면 how="left" 를 반드시 적는다.
#          이름 변경: df.rename(columns={"code": "sectorCode", "name": "sector"})
#            반환은 이름만 바뀐 새 DataFrame 이다.
#            미리 바꿔 두지 않으면 code_x / code_y 가 생겨 나중에 뭐가 뭔지 모른다.
#          방어     : merge(..., validate="many_to_one")
#            '오른쪽 키가 유일한가' 를 검사한다. 아니면 MergeError 를 낸다.
#            오른쪽이 유일하기만 하면 행 수는 절대 늘지 않는다.
#          merge 는 DataFrame 을 돌려주므로 그 결과에 또 merge 를 이어 붙일 수 있다.
#
#   ★ 마스터의 열 12개를 통째로 끌고 오지 말 것.
#     주소·대표자까지 90,000행에 복사되어 메모리만 낭비한다.
# =========================================================================
def join_all(prices: pd.DataFrame, master: pd.DataFrame,
             sectors: pd.DataFrame) -> pd.DataFrame:
    """시세에 종목 정보와 섹터 이름을 붙인 통합 데이터를 반환한다."""
    # TODO: sectors 의 열 이름을 바꾸고, master -> sectors 순으로 붙여 반환
    pass


# =========================================================================
# PRACTICE 4. 결측 진단
#   how="left" 로 붙였는데 sector 에 결측이 6,750건 생겼다.
#   어느 종목이 섹터를 못 받았는지 찾아라.
#
#   [기대 결과]
#     9개 종목      6,750 = 9종목 x 750거래일
#
#   [힌트] 결측 위치 : df["sector"].isna()  -> 길이가 같은 bool Series
#          그 행의 code 만 : df.loc[조건, "code"]
#          중복 제거 : .unique()  -> 순서가 들쭉날쭉하므로 sorted() 로 정렬해 반환
#          반환 타입은 리스트다. .tolist() 를 붙인다.
#
#   ★ how="left" 인데 왜 결측이 생기나
#     왼쪽 행은 전부 남았지만 오른쪽에서 짝을 못 찾은 것이다.
#     merge 는 짝이 없는 자리를 NaN 으로 채운다. 에러가 아니다.
#
#     원인을 확인하는 것이 이 문제의 목적이다.
#     오염된 키 때문인가(고쳐야 한다), 원래 정보가 없는 것인가(정상이다)?
#     원본 마스터의 sectorCode 열을 직접 열어 보면 답이 보인다.
# =========================================================================
def find_missing_sector(df: pd.DataFrame) -> list:
    """sector 를 못 받은 종목코드 목록을 정렬해 반환한다."""
    # TODO: sector 가 결측인 행의 code 를 중복 없이 모아 정렬해 반환
    pass


# =========================================================================
# PRACTICE 5. 분기 재무 결합
#   분기 재무(1,440행)를 통합 데이터에 붙인다. 행 수가 변하면 안 된다.
#
#   실행부가 'code 로만 붙였을 때' 를 먼저 보여준다. 90,000행이 1,080,000행이 된다.
#   왼쪽 한 행이 오른쪽 열두 행과 각각 짝을 짓기 때문이다.
#   merge 는 짝이 되는 '모든 조합' 을 만든다. 하나만 고르지 않는다.
#
#   행이 안 불어나게 붙여라.
#
#   [기대 결과]
#     90,000행 그대로      revenue 결측 3,360건 (= 120종목 x 28거래일)
#
#   [힌트] '어느 분기의 재무인가' 를 맞춰야 한다. 시세에 연도·분기 열을 만든다.
#          날짜에서 뽑기 : s.dt.year / s.dt.quarter
#            반환은 원본과 길이가 같은 정수 Series 다.
#            문자열에 .str 을 붙이듯 날짜에는 .dt 를 붙인다.
#            ★ dtype 이 datetime 이어야 쓸 수 있다.
#          열 이름은 financial 쪽과 같게 맞춘다 : fiscalYear · fiscalQuarter
#          여러 열을 키로 : on=["code", "fiscalYear", "fiscalQuarter"]
#            지정한 열이 '전부' 같은 행끼리만 붙는다.
#          키를 제대로 잡으면 validate="many_to_one" 도 통과한다. 함께 걸어 둘 것.
#
#   ★ 1:N 폭발의 해법은 대개 '키를 제대로 잡는 것' 이다.
#     결과의 결측 3,360건은 오류가 아니다. 왜 생겼는지는 실행부가 알려준다.
# =========================================================================
def join_financial(df: pd.DataFrame, financial: pd.DataFrame) -> pd.DataFrame:
    """분기 재무를 행 수 변화 없이 붙인 새 DataFrame 을 반환한다."""
    # TODO: 연도·분기 열을 만들고 세 개의 키로 붙여 반환
    pass


# =========================================================================
# PRACTICE 6. 섹터별 요약
#   섹터별 요약표를 만든다. 열 네 개를 아래 이름 그대로 만들 것.
#
#     종목수      그 섹터에 종목이 몇 개인가
#     거래일수    행이 몇 건인가
#     평균종가    close 의 평균
#     최대거래량  volume 의 최댓값
#
#   [기대 결과]
#     10행 4열       금융 섹터의 종목수는 17
#     ★ 종목수를 다 더하면 120 이 아니라 111 이다. 왜인지 실행부가 보여준다.
#
#   [힌트] 이름을 직접 주는 집계:
#            df.groupby("기준열").agg(새열이름=("대상열", "함수"), ...)
#            반환은 그룹 수만큼의 행을 가진 DataFrame 이다.
#            agg(["mean","max"]) 는 열 이름이 2겹이 되어 다루기 번거롭다.
#
#   ★★ 종목 수는 count 가 아니라 nunique 다
#     count   결측이 아닌 '행' 의 개수   -> 한 종목이 750행이면 750
#     nunique '고유값' 의 개수          -> 한 종목이 750행이어도 1
#
#     count 로 종목 수를 세면 750배 부풀려진 값을 얻는다. 에러는 안 난다.
#     여러 표를 붙인 뒤에 특히 자주 나오는 실수다.
# =========================================================================
def sector_summary(df: pd.DataFrame) -> pd.DataFrame:
    """섹터를 인덱스로 하는 요약표(4열)를 반환한다."""
    # TODO: groupby + named aggregation 으로 네 열을 만들어 반환
    pass


# =========================================================================
# PRACTICE 7. 피벗과 긴 형식
#   같은 데이터를 두 가지 형식으로 만들어 본다.
#
#   (1) quarterly_pivot : 행이 섹터, 열이 분기인 '넓은 형식' 평균 종가표
#   (2) to_long         : 그것을 sector · quarter · close 세 열짜리 '긴 형식' 으로
#
#   [기대 결과]
#     넓은 형식 (10, 13)      섹터 10개 x 분기 13개
#     긴 형식   (130, 3)      10 x 13 = 130행
#
#   [힌트] 분기 만들기 : s.dt.to_period("Q")  ->  2026-03-14 이 2026Q1 이 된다
#            astype(str) 로 글자로 만들어 두면 열 이름으로 쓰기 좋다.
#          피벗 : df.pivot_table(index="행기준", columns="열기준",
#                                values="집계할열", aggfunc="mean")
#            반환은 index 의 고유값이 행, columns 의 고유값이 열인 DataFrame 이다.
#          녹이기 : df.melt(id_vars="유지할열", var_name="...", value_name="...")
#            열 이름이 값으로 내려온 세로로 긴 DataFrame 을 돌려준다.
#            ★ sector 는 지금 인덱스라 melt 가 보지 못한다.
#              reset_index() 로 보통 열로 내려 놓는 것이 먼저다.
#
#   ★ pivot 과 pivot_table 은 다르다.
#     pivot 은 집계하지 않아서 (행,열) 조합이 중복되면 에러가 난다.
#     여기는 한 섹터·한 분기에 수천 행이 있으므로 pivot_table 이어야 한다.
#
#   ★ 저장과 분석은 긴 형식, 보고는 넓은 형식으로 기억할 것.
#     분기가 하나 늘 때마다 열을 추가하는 구조는 오래 유지되지 않는다.
# =========================================================================
def quarterly_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """행이 섹터, 열이 분기인 평균 종가표를 반환한다."""
    # TODO: 분기 열을 만들고 pivot_table 로 넓은 형식 표를 만들어 반환
    pass


def to_long(wide: pd.DataFrame) -> pd.DataFrame:
    """넓은 형식 표를 sector·quarter·close 세 열짜리 긴 형식으로 바꾼다."""
    # TODO: 인덱스를 열로 내린 뒤 melt 로 녹여서 반환
    pass


# =========================================================================
# PRACTICE 8. 시계열 지표
#   통합 데이터에 지표 네 개를 열로 추가한다.
#
#     ret     전일 대비 수익률 (비율)
#     ma5     5일 이동평균
#     ma20    20일 이동평균
#     golden  골든크로스 여부 (True/False)
#             단기선이 장기선을 아래에서 위로 뚫은 날
#             = 오늘은 ma5 > ma20 인데, 어제는 ma5 <= ma20 이었다
#
#   [기대 결과]
#     ret 결측 120건    ma5 결측 480건    ma20 결측 2,280건
#     골든크로스 2,620건
#
#   [힌트] 수익률   : s.pct_change()  ->  (s[i] - s[i-1]) / s[i-1], 첫 행은 NaN
#          이동평균 : s.rolling(20).mean()  ->  앞의 19칸은 값이 모자라 NaN
#          한 칸 밀기: s.shift(1)  ->  i번째 자리에 s[i-1] 이 온다
#          종목별로 : df.groupby("code")[col].transform(lambda s: ...)
#            transform 은 원본과 길이가 같은 결과를 돌려주므로 열로 바로 붙는다.
#            rolling·pct_change 는 이름으로 부를 수 없어 lambda 로 감싼다.
#          조건 결합 : (조건1) & (조건2)   and 가 아니라 & 이고 각 괄호는 필수다.
#          맨 앞에서 sort_values(["code", "date"]) 부터 한다.
#
#   ★★ groupby("code") 를 빠뜨리면 조용히 틀린다
#     종목이 120개 섞여 있다. groupby 없이 계산하면
#     A 종목의 마지막 19일과 B 종목의 첫날이 한 창(window)에 들어간다.
#     전혀 다른 회사의 주가가 섞이는데 값이 그럴듯해서 눈치채기 어렵다.
#
#   ★ 결측 수가 곧 검산이다
#     ma20 결측은 120종목 x 19일 = 2,280건이어야 한다.
#     groupby 를 빠뜨리면 19건이 나온다. 전체에서 딱 한 번만 모자라니까.
#     초반의 NaN 은 오류가 아니다. 20개가 모여야 계산되는 것이 맞다.
#
#   ★ shift 에도 groupby 가 필요하다
#     df["ma5"].shift(1) 로 쓰면 종목 경계에서 앞 종목 값을 끌어온다.
#     같은 줄에 groupby 가 두 번 나오는 것이 어색해 보여도 그렇게 써야 한다.
# =========================================================================
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """ret · ma5 · ma20 · golden 네 열이 추가된 새 DataFrame 을 반환한다."""
    # TODO: 정렬한 뒤 종목별로 수익률과 이동평균을 계산

    # TODO: 전일 이동평균을 종목별로 구해 골든크로스를 판정해 반환
    pass


# =========================================================================
# PRACTICE 9. 파이프라인으로 엮기
#   위 함수들을 하나의 진입점으로 묶는다. 바깥에서는 이 함수 하나만 부르면 된다.
#   데이터를 읽는 것도 이 함수 안에서 한다.
#
#     필요한 것 : load_prices() · load_sectors() · load_companies(raw=True)
#     쓰는 함수 : clean_master -> dedup_master -> join_all -> add_indicators
#
#   순서를 스스로 정하고, 왜 그 순서여야 하는지 생각해 볼 것.
#   순서가 틀리면 validate() 가 잡아낸다.
#
#   [기대 결과]
#     90,000행       validate() 10개 항목 전부 통과
#
#   [힌트] 각 함수가 '새 DataFrame' 을 돌려주므로 df = 함수(df) 로 이어 붙인다.
#          verbose 가 True 면 단계마다 log(단계이름, df, 메모) 를 불러 행 수를 남긴다.
#          로그는 결과가 이상할 때 어느 단계에서 틀어졌는지 찾는 유일한 방법이다.
#
#   ★ 지표 계산은 마지막이다.
#     붙이기 전에 계산하면, 결합 과정에서 행이 불어났을 때
#     지표까지 함께 오염된다.
# =========================================================================
def build_dataset(verbose: bool = True) -> pd.DataFrame:
    """다섯 장의 표를 읽어 분석용 통합 데이터를 만든다. 이 함수가 진입점이다."""
    # TODO: 데이터를 읽고 네 단계를 순서대로 이어 붙여 반환
    pass


# =========================================================================
# PRACTICE 10. (서술형) 12배로 불어났는데 평균은 왜 그대로인가
#   PRACTICE 5 의 실행부가 보여준 장면이다.
#
#     90,000 -> 1,080,000행   (12배)
#     종가 평균  46,294 -> 46,294     변하지 않는다
#     종가 합계  41억  -> 499억       12배가 된다
#
#   왜 평균만 그대로인가?
#   그리고 이런 일이 벌어졌다는 것을 무엇으로 알아챌 수 있는가?
#   아래 문자열에 적으세요.
#
#   [힌트] 평균은 무엇을 무엇으로 나눈 값인가.
#          모든 행이 똑같이 12번씩 복제되면 그 둘은 각각 어떻게 되는가.
#          그리고 합계·건수·비중은 왜 다른가.
# =========================================================================
ANSWER = """
TODO: 여기에 답을 적으세요.
"""


# =========================================================================
#  실행부  ―  아래는 수정하지 않아도 됩니다
# =========================================================================
def log(step_name, df, note=""):
    print(f"  [{step_name:<12}] {len(df):>7,}행  {note}")


def validate(df, verbose=True):
    """통합 데이터가 제대로 만들어졌다는 것을 숫자로 확인한다."""
    n_stock = df["code"].nunique()

    def has(*cols):
        """검사에 필요한 열이 다 있는지 확인한다.

        아직 만들지 않은 열을 검사하면 KeyError 로 실행이 멈춘다.
        열이 없으면 '실패' 로 두고 나머지 검사를 계속하게 한다.
        """
        return all(c in df.columns for c in cols)

    checks = [
        ("행 수 90,000", len(df) == 90_000),
        ("종목 수 120", n_stock == 120),
        ("종목별 750행", df.groupby("code").size().nunique() == 1),
        ("code+date 중복 0", df.duplicated(subset=["code", "date"]).sum() == 0),
        ("name 결측 0", has("name") and df["name"].isna().sum() == 0),
        ("market 2종", has("market") and df["market"].nunique() == 2),
        ("섹터 10종", has("sector") and df["sector"].nunique() == 10),
        # 마스터에 sectorCode 가 비어 있는 9종목은 sector 를 받지 못한다.
        # 결합 실패가 아니라 원본에 정보가 없는 것이라 '기대되는 결측' 이다.
        ("sector 결측 6,750", has("sector") and df["sector"].isna().sum() == 6_750),
        # 결측 수로 groupby 를 제대로 걸었는지 검산한다.
        ("ret 결측 = 종목수", has("ret") and df["ret"].isna().sum() == n_stock),
        ("ma20 결측 = 종목수x19", has("ma20") and df["ma20"].isna().sum() == n_stock * 19),
    ]

    if verbose:
        print(f"\n  {'검증 항목':<24}{'결과'}")
        print("  " + "-" * 36)
        for name, ok in checks:
            print(f"  {name:<24}{'통과' if ok else '실패'}")

    failed = [n for n, ok in checks if not ok]
    if failed and verbose:
        print(f"\n  ⚠ 실패 : {failed}")
    return not failed


def section(title):
    print("\n" + "=" * 68)
    print(f" {title}")
    print("=" * 68)


def step(fn, *args):
    """앞 문제가 미완성이면 건너뛰고, 에러가 나도 실행이 멈추지 않게 감싼다."""
    if any(a is None for a in args):
        print("  [건너뜀] 앞 문제를 먼저 완성하세요.")
        return None
    try:
        out = fn(*args)
    except Exception as e:
        # MergeError 처럼 여러 줄짜리 메시지는 첫 줄만 보면 원인이 드러난다.
        print(f"  [미완성] {type(e).__name__}: {str(e).splitlines()[0][:90]}")
        return None
    if out is None:
        print("  [미완성] 함수가 아직 값을 돌려주지 않습니다.")
        return None
    return out


if __name__ == "__main__":

    prices = load_prices()
    sectors = load_sectors()
    financial = load_financial()
    raw = load_companies(raw=True)

    print(f"시세      {len(prices):>8,}행   {prices['code'].nunique()}종목")
    print(f"마스터    {len(raw):>8,}행   ★ 120종목이어야 하는데 122행이다")
    print(f"섹터      {len(sectors):>8,}행")
    print(f"재무      {len(financial):>8,}행   종목당 12분기")

    section("PRACTICE 1. 키 정제")
    m1 = step(clean_master, raw)
    if m1 is not None:
        print(f"  행 수            : {len(m1):>8,}")                       # 기대: 122
        print(f"  market 종류      : {m1['market'].nunique()}종  {sorted(m1['market'].unique())}")   # 기대: 2종
        print(f"  companies 와 매칭 : {m1['name'].isin(load_companies()['name']).sum():>3}건")       # 기대: 122
        print(f"    (정제 전에는 {raw['name'].isin(load_companies()['name']).sum()}건이었다)")
        # 원본 raw 의 market 은 여전히 5종이어야 한다. 2종이 되어 있으면
        # 함수가 넘겨받은 원본을 그 자리에서 고쳤다는 뜻이다. (copy() 를 빠뜨린 경우)
        kept = raw["market"].nunique() == 5
        print(f"  원본 보존        : {'통과' if kept else '실패 - 원본이 바뀌었다. copy() 를 확인할 것'}")

    section("PRACTICE 2. 마스터 중복 제거")
    m2 = step(dedup_master, m1)
    if m2 is not None:
        print(f"  행 수      : {len(m2):>8,}")            # 기대: 120
        print(f"  code 유일  : {m2['code'].is_unique}")   # 기대: True

    section("PRACTICE 3. 3단 조인")
    d3 = step(join_all, prices, m2, sectors)
    if d3 is not None:
        print(f"  행 수       : {len(prices):,} -> {len(d3):,}")     # 기대: 90,000 -> 90,000
        print(f"  열 수       : {prices.shape[1]} -> {d3.shape[1]}") # 기대: 9 -> 13
        print(f"  name 결측   : {d3['name'].isna().sum():>8,}")      # 기대: 0
        print(f"  sector 결측 : {d3['sector'].isna().sum():>8,}")    # 기대: 6,750

    section("PRACTICE 4. 결측 진단")
    codes = step(find_missing_sector, d3)
    if codes is not None:
        print(f"  sector 를 못 받은 종목 : {len(codes)}개")           # 기대: 9
        print(f"    {codes}")
        blank = (raw["sectorCode"].str.strip() == "").sum()
        print(f"\n  원본 마스터의 sectorCode 빈 행 : {blank}건")      # 기대: 10
        print("  중복 2건 중 하나가 빈값이라 제거 후에는 9종목이 남는다.")

    section("PRACTICE 5. 분기 재무 결합")
    if d3 is not None:
        boom = prices.merge(financial, on="code", how="left")
        print(f"  code 로만 붙이면 : {len(prices):,} -> {len(boom):,}  ({len(boom)//len(prices)}배)")
        print(f"    종가 평균 {prices['close'].mean():,.0f} -> {boom['close'].mean():,.0f}   변하지 않는다")
        print(f"    종가 합계 {prices['close'].sum():,} -> {boom['close'].sum():,}   12배다")
    d5 = step(join_financial, d3, financial)
    if d5 is not None:
        print(f"\n  분기까지 맞춰 붙이면 : {len(d5):,}행   행 수가 유지된다")   # 기대: 90,000
        miss = d5["revenue"].isna().sum()
        print(f"  revenue 결측 : {miss:,}건 = 120종목 x {miss // 120}거래일")  # 기대: 3,360 / 28일
        bad = d5[d5["revenue"].isna()]
        print(f"    기간 : {bad['date'].min().date()} ~ {bad['date'].max().date()}")
        print("    재무는 2026-Q2 까지인데 시세는 그 뒤까지 있다. 오류가 아니다.")

    section("PRACTICE 6. 섹터별 요약")
    summary = step(sector_summary, d3)
    if summary is not None:
        print(summary.round(0).to_string())
        total = summary["종목수"].sum()
        print(f"\n  종목수 합계 : {total}  /  전체 종목 {d3['code'].nunique()}")   # 기대: 111 / 120
        print(f"  {d3['code'].nunique() - total}종목이 요약표에서 빠졌다. 경고는 없다.")
        print("  groupby 는 키가 NaN 인 행을 조용히 버린다 (dropna=True 가 기본값).")

        cmp_ = sectors.set_index("name")["companyCount"]
        both = pd.DataFrame({"실제": summary["종목수"], "마스터": cmp_})
        both["차이"] = both["실제"] - both["마스터"]
        print(f"\n  섹터 마스터의 companyCount 와 비교:")
        print(both.to_string())
        print(f"    일치 {(both['차이'] == 0).sum()}개 / 10개")       # 기대: 5개
        print("    빠진 9종목만큼 모자란다. 집계 결과를 마스터와 대조하면 이렇게 드러난다.")

    section("PRACTICE 7. 피벗과 긴 형식")
    wide = step(quarterly_pivot, d3)
    if wide is not None:
        print(f"  넓은 형식 : {wide.shape}  (행=섹터, 열=분기)")      # 기대: (10, 13)
        print(wide.iloc[:4, :4].round(0).to_string())
    long = step(to_long, wide)
    if long is not None:
        print(f"\n  긴 형식   : {long.shape}   = {wide.shape[0]} x {wide.shape[1]}")  # 기대: (130, 3)
        print(long.head(4).round(0).to_string(index=False))

    section("PRACTICE 8. 시계열 지표")
    d8 = step(add_indicators, d3)
    if d8 is not None:
        n = d8["code"].nunique()
        print(f"  {'열':<8}{'결측':>10}{'기대':>10}   검산")
        print("  " + "-" * 46)
        for col, per in [("ret", 1), ("ma5", 4), ("ma20", 19)]:
            got, exp = d8[col].isna().sum(), n * per
            print(f"  {col:<8}{got:>10,}{exp:>10,}   {n}종목 x {per}일  {'OK' if got == exp else '확인 필요'}")
        print(f"\n  골든크로스 : {int(d8['golden'].sum()):,}건  (종목당 {d8['golden'].sum()/n:.1f}회)")  # 기대: 2,620
        print("\n  결측 수가 맞으면 종목별로 제대로 계산된 것이다.")
        print("  groupby 를 빠뜨리면 ma20 결측이 19건뿐이다. 전체에서 한 번만 모자라니까.")

    section("PRACTICE 9. 파이프라인으로 엮기")
    dataset = step(build_dataset)

    if dataset is not None:
        ok = validate(dataset)
        print(f"\n  전체 통과 : {ok}")
        print("\n  결합이 끝났다는 것을 '느낌' 이 아니라 '숫자' 로 확인한다.")
        print("  통과하지 못하면 다음 단계로 넘기지 않는다.")

    section("PRACTICE 10. 12배로 불어났는데 평균은 왜 그대로인가")
    print("  [제출한 답]")
    print("  " + ANSWER.strip().replace("\n", "\n  "))