"""
    충전소 데이터 정제 (clean_stations)
"""

import sys
import os
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from _dp  import (regions_path, raw_stations_path, raw_charging_logs_path, ENCODING)


# 충전소 데이터
rawStations = pd.read_csv(raw_stations_path(), encoding=ENCODING,
                        dtype=str, keep_default_na=False)

# 복사본 : 원본을 건들지 않기 위해
clean_stations = rawStations.copy()

# station_name : 앞뒤중간 공백 제거, 전각문자를 반각으로 통일
clean_stations['station_name'] = (
    clean_stations["station_name"]
    .map(lambda value: unicodedata.normalize("NFKC", value))    # unicodedata.normalize("NFKC", value) => 전각 문자와 전각 공백을 일반 문자·일반 공백으로 통일
    .str.replace(r"\s+", "", regex=True)        # .str.replace(r"\s+", "", regex=True) => 앞뒤·중간의 공백을 모두 제거
)

name_compare = pd.DataFrame({
    "원본": rawStations['station_name'],
    "정제본": clean_stations['station_name']
})

print(f"{name_compare[name_compare["원본"] != name_compare["정제본"]]}")

print(rawStations['charger_type'])

# charger_type : 앞뒤중간 공백 제거, 전각문자를 반각으로 통일 후 'DC급속', 'AC완속'으로 분기
"""
    기존 데이터

    - AC 완속
    - ac완속
    - 완속
    - DC 급속
    - dc급속
    - 급속
"""
clean_stations['charger_type'] = (
    clean_stations["charger_type"]
    .map(lambda value: unicodedata.normalize("NFKC", value))    # unicodedata.normalize("NFKC", value) => 전각 문자와 전각 공백을 일반 문자·일반 공백으로 통일
    .str.replace(r"\s+", "", regex=True)        # .str.replace(r"\s+", "", regex=True) => 앞뒤·중간의 공백을 모두 제거
    .str.upper()        # upper() => 대문자로 변경
)
"""
    uppper()로 대소문자 대문자로 통일 후 데이터

    - AC완속
    - DC급속
    - 완속
    - 급속
"""

# 급속 -> DC급속 / 완속 -> AC완속
clean_stations['charger_type'] = clean_stations['charger_type'].replace({
    "급속": "DC급속",
    "완속": "AC완속",
})

print(clean_stations['charger_type'])
print("="*50)
print(clean_stations['charger_type'].unique())


# region_code : 대문자로 통일, 빈 값은 결측으로 처리
clean_stations['region_code'] = (
    clean_stations["region_code"]
    .str.strip()        # 양쪽 공백 제거    
    .str.upper()        # upper() => 대문자로 변경
)

# 빈 값은 결측 NaN으로 처리
clean_stations["region_code"] = clean_stations["region_code"].replace("", pd.NA)

print(clean_stations['region_code'].unique())

print(clean_stations['region_code'].value_counts(dropna=False))


# capacity_kw, unit_price : 단위 문자를 제거하고 정수로만 정제
# print(clean_stations['capacity_kw'])
# print(clean_stations['unit_price'])

clean_stations['capacity_kw'] = (
    clean_stations['capacity_kw']
    .map(lambda value: unicodedata.normalize("NFKC", value))
    .str.replace("kW", "", regex=False)     # 데이터에서 kw부분을 ""빈값으로 변경
    .str.strip()        # 양쪽 공백 제거
)
clean_stations["capacity_kw"] = pd.to_numeric(
    clean_stations["capacity_kw"],
    errors="coerce",
).astype("Int64")


clean_stations['unit_price'] = (
    clean_stations['unit_price']
    .map(lambda value: unicodedata.normalize("NFKC", value))
    .str.replace("원", "", regex=False)     # 데이터에서 '원'부분을 ""빈값으로 변경
    .str.strip()        # 양쪽 공백 제거
)
clean_stations["unit_price"] = pd.to_numeric(
    clean_stations["unit_price"],
    errors="coerce",
).astype("Int64")


print(clean_stations[["capacity_kw", "unit_price"]].dtypes)
print()

print(clean_stations[["capacity_kw", "unit_price"]].agg(["min", "max"]))
print()

print(clean_stations[["capacity_kw", "unit_price"]].isnull().sum())
print()

print("="*40)



# installed_date : datetime으로 통일 (원본에는 형식이 3종으로 섞여있음) ex) 2026-09-04
print(clean_stations['installed_date'])
"""
    기존 원본 데이터 3가지 형식
    1. 20260904
    2. 2026-09-04
    3. 2026.09.04
"""

clean_stations['installed_date'] = (
    clean_stations['installed_date']
    .map(lambda value: unicodedata.normalize("NFKC", value))
    .str.strip()        # 양쪽 공백 제거
    .str.replace(".", "-", regex=False)     # 데이터에서 '.'부분을 "-"으로 변경
    .str.replace(
        r"^(\d{4})(\d{2})(\d{2})$",
        r"\1-\2-\3",
        regex=True
    )
    # r : 뒤에 문자열에서 역슬래시(\)는 인식하지 않는다.
    # ^ : 문자열 시작, $ : 문자열 끝
    # (\d{4}) : 4개를 하나의 그룹으로
    # \1 : 순서상 첫번째 그룹, \2 : 순서상 두번째 그룹, ...
    # => 20260904 -> 2026-09-04
)
"""
    정제 데이터의 형식
    2. 2026-09-04
"""

print(clean_stations['installed_date'])

print(f"{"="*30}중복 제거 전{"="*30} : {len(clean_stations)}행")
print(clean_stations)

# 중복 제거 : station_id 기준으로 중복 제거
clean_stations = clean_stations.drop_duplicates(
    subset='station_id',
    keep='first',
)
print(f"{"="*30}중복 제거 후{"="*30} : {len(clean_stations)}행")
print(clean_stations)

# 중복 제거 후 비어있는 인덱스가 있어 재정렬
clean_stations = clean_stations.reset_index(drop=True)
print(f"{"="*30}중복 제거 후 인덱스 초기화{"="*30} : {len(clean_stations)}행")
print(clean_stations)




