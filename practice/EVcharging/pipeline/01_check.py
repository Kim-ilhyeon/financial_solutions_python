"""
    Step1. 진단

    정제하기 전에 **무엇이 얼마나 망가졌는지** 파악합니다.
    세 파일을 읽고 아래를 확인해 표로 정리하세요.
    - 각 파일의 행 수, 컬럼별 dtype
    - 숫자여야 하는데 문자열로 읽힌 컬럼
    - 컬럼별 결측 수와 비율
    - `station_id`, `log_id` 의 중복 건수
    - `charger_type`, `region_code`, `payment_method` 의 고유값 목록
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from _dp  import (regions_path, raw_stations_path, raw_charging_logs_path, ENCODING)


# 지역 데이터
regions = pd.read_csv(regions_path(), encoding=ENCODING,
                        dtype=str, keep_default_na=False)

# 충전소 데이터
rawStations = pd.read_csv(raw_stations_path(), encoding=ENCODING,
                        dtype=str, keep_default_na=False)

# 충전기록 데이터
rawChargingLogs = pd.read_csv(raw_charging_logs_path(), encoding=ENCODING,
                        dtype=str, keep_default_na=False)

# print(regions)
# print("="*40)
# print(rawStations)
# print("="*40)
# print(rawChargingLogs)
# print("="*40)

datasets = {
    "regions": regions,
    "raw_stations": rawStations,
    "raw_charging_logs": rawChargingLogs,
}

# 각 파일의 행 수, 컬럼별 dtype
for name, df in datasets.items():
    print(f"{name} 행 수: {len(df)}행")
    print(f"\n  [컬럼]           [dtype]")
    print(df.dtypes)
    print("="*50)

print()

# 각 파일의 컬럼별 결측 수와 비율
for name, df in datasets.items():
    na_count = df.isnull().sum()
    na_ratio = df.isnull().mean() * 100
    print(f"[{name}]")
    print()
    print(f"{name} 컬럼별 결측 수 \n{na_count}")
    print("-"*30)
    print(f"{name} 컬럼별 결측 비율 \n{na_ratio}")
    print("="*50)

print()

# station_id, log_id 컬럼의 중복 건수
station_id_duplicates = rawStations["station_id"].duplicated().sum()
log_id_duplicates = rawChargingLogs["log_id"].duplicated().sum()

duplicate_summary = pd.DataFrame({
    "컬럼": ["station_id", "log_id"],
    "중복 건수": [station_id_duplicates, log_id_duplicates],
})

print(duplicate_summary)

print()

unique_charger_type = rawStations["charger_type"].unique()
unique_region_code = rawStations["region_code"].unique()
unique_payment_method = rawChargingLogs["payment_method"].unique()

print(unique_charger_type)
print()
print(unique_region_code)
print()
print(unique_payment_method)
print()

unique_stations_count = rawStations["station_id"].nunique()
print(f" 중복값 제거한 충전소 갯수 : {unique_stations_count}")


