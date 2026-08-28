"""
    merge 기본과 키정제 
"""

import pandas as pd
import unicodedata

from _load import load_companies, load_prices

pd.set_option("display.width", 140)

prices = load_prices()

companies = load_companies() # 정제본
raw = load_companies(True)  # 오염본

print(f" {'sectors':<14} {00:>10}")
print(f" {'companies':<14} {len(companies):10}     종목정보(섹터코드)")    
print(f" {'prices':<14} {len(prices):10}       종목별 일별 시세")

"""
    시세 90,000행에 섹터이름을 매번 저장하면
    같은 문자열이 수천번 씩 반복된다. -> 분리해서 저장하고 식별코드로 연결한다. (정규화)

    저장은 나누고, 분석은 합쳐서 한다.
    ex) 섹터별 평균 수익률
    = 나뉜 데이터를 다시 붙여주는 것을 merge라고 함.
"""

# merge - SQL의 JOIN과 같다.
# 왼쪽표.merge(오른쪽표, on="키열", how="기준(left/right/inner/outer)")
# 두 표의 열을 모두 가진 새로운 DataFrame을 반환
# how = "[inner]/left/right/outer"

m = prices.merge(companies, on="code", how="left")
print(f'\n prices.merge(companies, on="code", how="left")')
print(f" {len(prices):,} -> {len(m):,}행, 열{prices.shape[1]} -> {m.shape[1]}개")


# 열 이름이 겹치면 어떻게 될까? ..._x / ..._y가 붙는다.
p2 = prices.head(3).copy()
p2["name"] = "시세쪽이름"

bad = p2.merge(companies[["code", "name"]], on="code")

print(f" 기본값 : {[c for c in bad.columns if 'name' in c]}")

print(f" bad {bad}")

# suffixes : 양쪽에 같은 이름의 열이 있을 때 붙일 꼬리표를 정한다.
# 왼쪽표.merge(오른쪽표, on="키열", how="left", suffixes="(_왼쪽", "_오른쪽"))

good = p2.merge(companies[["code", "name"]], on="code", suffixes=("_price", "_companies"))
print(f" 기본값 : {[c for c in good.columns if 'name' in c]}")
# _x, _y같은 값은 추후에 어떤 값인지 알기 어렵다. 직접 지정하는 것이 좋다.

# merge는 키명이 완전히 같은 때에만 붙임. 사람눈에 같아보이는 것은 중요하지 않다.(타입 같아야 하고, 공백포함도 같아야 한다.)



# 1. 문자열의 공백이 있으면 동일 값이 아니다.
# 컬럼의 글자 양옆에 공백이 있는 데이터의 수
sp_edge = (raw["name"] != raw["name"].str.strip()).sum()    # 컬럼의 공백이 있는 것의 갯수

# 컬럼의 글자 중간에 공백이 들어있는 데이터의 수
mid_mask = raw["name"].str.contains(r"\S\s+\S", regex=True)
sp_mid = mid_mask.sum()

# repr 객체 내용 전달시 상태를 좀 더 잘 확인할 수 있다. - 특수문자나 공백같은 걸 그대로 표기
edge_ex = [repr(x) for x in raw.loc[raw["name"] != raw["name"].str.strip(), "name"].head(2)]
mid_ex = raw.loc[mid_mask, "name"].head(2).tolist()

print(f" 공백")
print(f" 앞뒤 공백 {sp_edge}건, 예시 : {edge_ex}")
print(f" 중간 공백 {sp_mid}건, 예시 : {mid_ex}")

print()

# 2. 대소문자
print(f" market 종류 {raw['market'].nunique()} 개 : {sorted(raw['market'].unique())}")
print(f" upper() 후 : {sorted(raw['market'].str.upper().unique())}")

print()

# 3. 전각문자
def has_hullwidth(s):
    """
        전각문자가 하나라도 있다면 True를 반환
        ord(문자) : 해당 문자의 유니코드 번호를 줌.
         0xFF01 ~ 0xFF5F : 전각 영문, 기호
         0x3000          : 전각 공백
    """
    return any((0xFF01 <= ord(c) <= 0XFF5F) or (ord(c) == 0x3000) for c in str(s))

# map(함수) : series의 값 하나하나에 함수를 적용한 응답 값으로 series를 생성 후 반환
fw = raw[raw["name"].map(has_hullwidth)]
print(f" 전각문자 {len(fw)} 건")
for v in fw["name"]:
    print(f" {v!r}")
    print(f" 정규화 -> {unicodedata.normalize('NFKC', v)!r}")

print()

# 타입 불일치
c_int = companies.copy()
c_int["code_num"] = c_int["code"].str.replace("G", "").astype("int64")
p_str = prices.head(100).copy()
p_str["code_num"] = p_str["code"].str.replace("G", "")

print(f" p_str code_num dtype : {p_str['code_num'][0]} {p_str['code_num'].dtype}")
print(f" c_int code_num dtype : {c_int['code_num'][0]} {c_int['code_num'].dtype}")
# 타입이 다르면 merge시에 에러가 발생함.
# (구 버전은 에러는 없지만 안붙고 데이터가 없어짐)

# 키를 할상 정제 후에 붙여줘야 한다.
clean = raw.copy()
clean["name"] = (clean["name"]
                    .map(lambda s : unicodedata.normalize("NFKC", s))      # 전각 제거
                    .str.replace(r"\s+", "", regex=True)        # 공백 전부 제거
                )

clean["market"] = clean["market"].str.upper().str.strip()       # 대소문자 통일
clean["code"] = clean["code"].str.upper().str.strip()

# outer merge를 활용해서 매칭이 안되는 데이터가 양쪽에 각각 몇개 있는지 확인이 가능.

# 일부 종목을 빼서 매칭 실패를 유도
partial = companies[companies["code"] != "G0001"]

# indicator=True : 각 행이 어느 쪽에서 왔는지 표기(_merge라는 열에 both / left_only / right_only)
chk = prices.merge(partial, on="code", how="outer", indicator=True)
print(f" chk['_merge'] : {chk["_merge"].value_counts().to_string()}")

print()

# inner merge로 붙였는데 행이 줄었다면 어떤것이 빠진건지 알 수 없다.
# -> outer + indicator로 한 번 확인하면 된다.
