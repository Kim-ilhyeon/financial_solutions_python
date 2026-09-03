"""
    데이터 파이프라인과 재실행 검증
    pipeline/ 폴더에 지금까지 배운 것들의 구현함수가 정의되어 있다.
    - config.py 설정, 환경변수
    - logger.py 로깅을 해주는 함수들
    - extract.py 수집 (API, CSV)
    - transform.py 정제
    - load.py 적재
    - pipeline.py 전체 흐름
"""

from _db import connect

"""
    pipeline은 이 파일 옆 폴더명, 그리고 .pipeline은 pipeline.py, 그리고 그 안에 run함수 가져옴
    pipeline/ 안에서는 서로 from . import extract처럼 상대 경로로 부를 수 있음
"""
from pipeline.pipeline import run

# ETL - 파이프라인의 단계를 왜 나눠서 만드는가?

"""
    단계 : Extract    ->     Transform    ->    Load
           (수집)          (정제, 계산, 검증)    (DB에 적재)

    단계를 나눠서 개발하고 실행하면
    - 어디서 실패했는지가 명확해짐.
    - 실패한 단계만 다시 돌리면 됨.
    - 단계별 테스트가 편리함.
    - 수집처가 API에서 파일로 바뀌어도 Extract만 수정하면 됨. (유지보수가 쉬움) ★★★
"""

# 시작 상태를 비워두고
conn = connect()

with conn.cursor() as cur:
    cur.execute("TRUNCATE TABLE daily_price")
conn.commit()

def row_count():
    def count(name):
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) AS n FROM daily_price")
            return cur.fetchone()['n']

print("="*70)
print("=== 1회차 실행 ===")
print("="*70)

ok1 = run()
n1 = row_count()

print()

print("="*70)
print("=== 2회차 실행 ===")
print("="*70)

ok2 = run()
n2 = row_count()

print("="*70)
print("=== 검증 ===")
print("="*70)

checks = [
    ("1회차 성공", ok1),
    ("2회차 성공", ok2),
    ("행 수가 같은가? ", n1 == n2),
    ("종목 수 120 ", None),
]

with conn.cursor() as cur:
    cur.execute("SELECT COUNT(DISTINCT code) AS c FROM daily_price")
    codes = cur.fetchone()['c']
checks[3] = ("종목 수 120 ", codes == 120)

print(f" 1회차 적재 : {n1}행")
print(f" 2회차 적재 : {n2}행")
print(f" 종목 수 : {codes}개")
print()
for name, ok in checks:
    print(f" {name} : {'통과' if ok else '실패'}")

"""
    두 번 돌려도 행 수는 그대로 멱등하다.
    행이 두배가 되거나 에러가 났다면 셋 중 하나가 빠진거다.
    - 유니크 제약 조건이 없거나
    - ON DUPLICATE KEY UPDATE, upsert를 사용하지 않았거나
    - 정재 데이터에 오류가 있거나
"""