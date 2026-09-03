"""
    대량 적재
"""
import time

import pandas as pd
from _db import connect, get_engine, prices_path, ENCODING

pd.set_option("display.width", 130)

SAMPLE = 1_000
TOTAL = 90_000

conn = connect()    # pymysql
engine = get_engine()   # SQLAlchemy

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=['date'])
sample = df.head(SAMPLE).copy()

cols = ["code", "date", "open", "high", "low", "close", "volume", "change", "changeRate"]
sample = sample[cols]   # 정렬

# 데이터 추가 병목

def reset_table():
    """ 테이블을 비워주는 함수 """
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE daily_price")
    conn.commit()


def count_rows():
    """ daily_price의 행 개수를 가져오는 함수 """
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) AS n FROM daily_price"
        )
        return cur.fetchone()['n']

# {','.join(['%s'] * 9)} --> 열이 늘어나거나 줄어도 숫자만 변경하면 된다. (유지보수가 좋다.)
INSERT_SQL = f"""
INSERT INTO daily_price (code, date, open, high, low, close, volume, `change`, changeRate)
VALUES ({','.join(['%s'] * 9)})
"""

# iterrows() 대신 itertuples()를 사용할 수 있음.
# itertuples() -> 행 단위로 가져오지만 속도가 비교적 더 빠르다.
rows = [tuple(r) for r in sample.itertuples(index=False)]
print(rows)

print("="* 70)

# 적재방식 4가지
results = []

# 1. execute를 반복 - 한 행씩 sql을 전달. 가장 느림
reset_table()
start = time.perf_counter()

with conn.cursor() as cur:
    print("들어옴")
    for r in rows:
        print(f"현재 데이터 길이: {len(r)} | 데이터: {r}")
        print("반복중")
        cur.execute(INSERT_SQL, r)
        print("반복 후")
    print("작업중")
conn.commit()

t1 = time.perf_counter() - start

results.append(("execute 반복", t1, count_rows()))

print(results)

print("=" * 70)

# 2. executemany - sql을 한 문장으로 한번에 보냄
reset_table()
start = time.perf_counter()
with conn.cursor() as cur:
    cur.executemany(INSERT_SQL, rows)
conn.commit()

t2 = time.perf_counter() - start

results.append(("executemany", t2, count_rows()))

print(results)

print("=" * 70)

"""
    df.to_sql(테이블명, engine, if_exists="append", index=Fasle)
    => df를 통째로 테이블에 넣는다. --> 내부적으로는 executemany를 사용한다.
    (직접 insert문을 작성하지 않아도 된다.)

    if_exists : "append" = 뒤에 붙임 / "replace" = 테이블 지우고 새로 만들건지 / "fail" = 실패 처리
"""

# 3. to_sql 기본값 - 내부적으로 executemany를 사용해서 적재
reset_table()
start = time.perf_counter()
sample.to_sql("daily_price", engine, if_exists="append", index=False)
t3 = time.perf_counter() - start
results.append(("to_sql(기본값)", t3, count_rows()))

# 4. to_sql method="multi" - 원하는 개수만큼 청킹해서 insert시킬 수 있다.
reset_table()
start = time.perf_counter()
sample.to_sql("daily_price", engine, if_exists="append", index=False,
              method="multi", chunksize=500)
t4 = time.perf_counter() - start
results.append(("to_sql(multi)", t4, count_rows()))

for name, t, n in results:
    est = t * (TOTAL / SAMPLE)
    print(f" {name:<22} {t*1000:>8.0}ms {n:>8,} {est:>14.1f}초")


"""
    차이가 심하게 보이지는 않는다.
    그리고 to_sql(multi)도 엄청 빠르지는 않다.

    원인은 DB가 같은 컴퓨터에 있어서 그렇게 보일 수 있다.
    왕복 비용을 직접 재보자.
"""

# 한 번 왕복 시 얼마나 소요가 되는가..?

N_RT = 2000
with conn.cursor() as cur:
    cur.execute("SELECT 1")     # 간단한 SELECT로 연결 정리
    start_rt = time.perf_counter()
    for _ in range(N_RT):
        cur.execute("SELECT 1")
        cur.fetchone()
    rt = (time.perf_counter() - start_rt) / N_RT    # 한 번 왕복의 시간

print(f" 왕복 1회 비용(로컬기준) : {rt * 1000:.4f}ms")
print(f" 90000회 반복 시 : {rt * TOTAL:.1f}초")
"""
    로컬에서 네트워크를 타지 않고 하는 반복은 거의 비용이 없는 수준이다.
    그래서 우리 눈에는 실습으로 체감하기는 어렵다.
    
    실무에서는 DB가 다른 서버에 존재한다. (네트워크를 타면 왕복 비용은 커진다.)
"""


# chunksize와 max_allowed_packet
# max_allowed_packet : 한 번에 주고받을 수 있는 최대 바이트 수
with conn.cursor() as cur:
    cur.execute("SHOW VARIABLES LIKE 'max_allowed_packet'")
    packet = int(cur.fetchone()['value'])

print(f" 이 서버의 max_allowed_packet : {packet:,}bytes ({packet / 1024 / 1024:.0f}MB)")

"""
    chunksize없이 90,000행을 한 번에 보내면 SQL문 하나가 너무 길어서 max_allowed_packet(한도)을 넘을 수 있다.
    'Packet too large' --> chunksize를 줄여야 한다.

    무조건 크게 묶는다고 빨라지는 것이 아니다.
    왕복은 줄지만 메모리 사용량과 트랜잭션 크기가 커진다.
    실패했을 경우 되돌림 연산도 늘어난다.
"""

print(f"\n 청크 크기별 측정 ({SAMPLE:,}행)")
for cs in[100, 500, 2000, 5000]:
    reset_table()
    start = time.perf_counter()
    sample.to_sql("daily_price", engine, if_exists="appned", index=False,
                  method="multi", chunksize=cs)
    print(f" {cs:>12,} {(time.perf_counter() - start) * 1000:>10.0f}ms")
# 보통 벌크 데이터는 청크사이즈를 기본값으로 5000으로 지정한다. 조금 많으면 10000개로 한다.

"""
    너무 작으면 왕복이 많아지고, 너무 크면 메모리 이득이 줄어든다.
    보통 청크사이즈를 5000행을 기준으로 잡고 사용한다. 
"""



"""
    인덱스가 있으면 INSERT시 마다 전체 인덱스를 갱신해야 된다.
    조회는 빨라질 수 있지만 적재는 무조건 느려진다.

    그렇다고 인덱스를 아예 빼버리면 안됨.
    UNIQUE(code, date) -> 속도를 위한 것이 아닌 중복 차단을 위한 것임

    초기 적재에서만 인덱스를 잠시 끌 수도 있지만,
    그럴 경우 제약도 함께 꺼지므로 맨~ 처음 한 번 넣을 때만 사용.
"""



