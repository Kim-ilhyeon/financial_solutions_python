"""
    충전 기록 데이터 정제 (clean_charging_logs)
"""

import sys
import os
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from _dp  import (regions_path, raw_stations_path, raw_charging_logs_path, ENCODING)


# 충전 기록 데이터
rawChargingLogs = pd.read_csv(raw_charging_logs_path(), encoding=ENCODING,
                        dtype=str, keep_default_na=False)

# 복사본 : 원본을 건들지 않기 위해
clean_charging_logs = rawChargingLogs.copy()

# energy_kwh, fee : 콤마 제거 후 숫자로 변환. (실패는 결측으로)
print(len(clean_charging_logs))
print(clean_charging_logs.head(20))
print()
print(clean_charging_logs[20:41])
print()
print(clean_charging_logs[40:61])
print()
print(clean_charging_logs[60:81])
print()
clean_charging_logs['energy_kwh'] = (
    clean_charging_logs['energy_kwh']
    .map
)




# start_time, end_time : datetime으로 통일 (원본에는 3가지 형식 존재)




# payment_method : 공백 제거 후 대문자로 통일




# log_id기준으로 중복 제거










