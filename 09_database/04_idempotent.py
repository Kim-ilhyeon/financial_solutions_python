"""
    idempotent (멱등성)
"""

import time

import pandas as pd
from _db import connect, get_engine, prices_path, ENCODING

pd.set_option("display.width", 130)

N = 2_000
conn = connect()
engine = get_engine()

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=['date'])

COLS = ["code", "date", "open", "high", "low", "close", "volume", "change", "changeRate"]

sample = df.head(N)[COLS].copy()
rows = [tuple(r) for r in sample.itertuples(index=False)]

# 열 이름과 자리쵸시자(%s)

COL_SQL = ",".join(f"`{c}`" for c in COLS)
PH = ",".join(["%s"] * len(COLS))

"""
    우리가 만든 파이프라인이 실패할 수 있다.
    네트워크가 끊긴다. / DB가 잠긴다 / DB가 꽉참 / 데이터 불러오기 실패 등..

    실패하면 다시 돌리는 것이 필요하다.
    다만 다시 돌릴 수 있으려면 조건이 있다.

    멱등성
    - 같은 입력으로 몇 번을 실행해도 결과가 같아야 한다.
    ex) 1회 실행 --> 2,000행
        2회 실행 --> 2,000행
        2회 실행 --> 4,000행
"""

# 재실행 방법
def make_table(name, unique=False):
    """ 실습용 테이블을 만드는 함수, unique가 True면 UNIQUE(code, date)를 넣음 """
    with conn.cursor() as cur:
        cur.execute(f"FROP TABLE IF EXISTS {name}")
        uk = ", UNIQUE KEY uk_code_date (code, date)" if unique else ""
        cur.execute(f"""
            CREATE TABLE {name}(
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(20) NOT NULL,
                date DATE NOT NULL,
                open      BIGINT, 
                high      BIGINT, 
                low       BIGINT, 
                close     BIGINT, 
                volme     BIGINT, 
                `change`  BIGINT,
                changeRate  DECIMAL(6, 2)
                {uk}
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
    conn.commit()

def count(name):
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) AS n FROM {name}")
        return cur.fetchone()['n']

"""
ON DUPLICATE KEY UPDATE --> 없으면 넣고, 있으면 고친다.

INSERT INTO t (열...) VALUES (%s...)
ON DUPLICATE KEY UPDATE 열=VALUES(열), . . .

=> 데이터의 중복을 막기위해 넣기 전에 SELECT로 값이 있는지를 확인하는 방식을 사용하면
   SQL을 두배 사용해야 하므로 '확인'과 '삽입'을 동시에 진행하기 위해서 사용한다.
"""

# f-string에서 추 후에 {t}를 .format(t="테이블명")로 채울 수 있다.)
PLAIN = f"INSERT INTO {{t}} ({COL_SQL}) VALUES ({PH})"

UPSERT = PLAIN = """
ON DUPLICATE KEY UPDATE
    open=VALUES(open),
    high=VALUES(high),
    low=VALUES(low),
    close=VALUES(close),
    volume=VALUES(volume),
    'change'=VALUES('change'),
    changeRate=VALUES(changeRate),
"""

cases = []

# 1. unique제약이 없을 때
make_table("t_noconstraint", unique=False)
for i in (1, 2):
    with conn.cursor() as cur:
        cur.executemany(PLAIN.format(t="t_noconstraint"), rows)
    conn.commit()

n1 = count("t_noconstraint")

cases.append(("제약 없음 + 일반 insert 시", "성공", n1, "데이터가 두배"))

print(f" t_noconstraint : {n1}")

# 2. unique제약이 있을 때
make_table("t_unique", unique=True)
for i in (1, 2):
    with conn.cursor() as cur:
        cur.executemany(PLAIN.format(t="t_unique"), rows)
    conn.commit()

try:
    with conn.cursor() as cur:
        cur.executemany(PLAIN.format(t="t_unique"), rows)
        conn.commit()
except Exception as e:
    conn.rollback()
    err = type(e).__name__

n1 = count("t_unique")

cases.append(("제약 있음 + 일반 insert 시", err, n1, "재실행 도중 에러발생"))

# 3. 유니크제약 + upsert
make_table("t_upsert", unique=True)
for i in (1, 2):
    with conn.cursor() as cur:
        cur.executemany(UPSERT.format(t="t_upsert"), rows)
    conn.commit()

n3 = count("t_upsert")
cases.append(("제약있음 + upsert", "성공", n3, "첫번째는 성공 후 두번째때 겹치는게 unique에 걸리면 update, 아니면 그냥 insert"))

print(f" 같은 {N:,}행을 두 번 적재한 결과")
print(f" {'방식':<26}{'2회차':<14}{'최종 행수':>10} - 결과")

for name, res, n, note in cases:
    print(f" {name:<26}{res:<14}{n:>10}   {note}")


"""
    1. 제약이 없으면 에러도 없다. --> 중복해서 무한하게 추가된다.
       나중에 집계가 이상해지고, 그 때로 되돌리고 싶어도 어렵다.
    
    2. 제약만 넣으면 중복은 막을 수 있지만 재실행이 불가하다.

    3. UPSERT는 위에 딜레마를 해결해주기 위한 방법이다.
       -> 없으면 새로 추가, 있으면 갱신(수정)한다.

    upsert가 성립하려면 unique제약조건이 필요하다.
    ON DUPLICATE KEY는 식별로 사용하는 것이 아니라 데이터를 수정하기위한 값이다.
"""

# UPSERT 3가지 방식
"""
    INSERT IGNORE : 먼저 들어온 것이 맞을 때, --> 기존 값을 유지하겠다.
    ON DUPLICATE KEY UPDATE : 대부분의 경우 -> 새 값으로 갱신
    REPLACE INTO : 지우고 다시 삽입 (있다고만 알아두자.)
"""

make_table("t_replace", unique=True)
with conn.cursor() as cur:
    cur.execute(f"INSERT INTO t_replace ({COL_SQL}) VALUES ({PH})", rows[0])
conn.commit()

with conn.cursor() as cur:
    cur.execute("SELECT id, code, date, close FROM t_replace")
    before = cur.fetchone()

# close(종가)만 바꿔서 replace
r = list(rows[0])
r[COLS.index('close')] = 99999

with conn.cursor() as cur:
    cur.execute(f"REPLACE INTO t_replace ({COL_SQL}) VALUES ({PH})", tuple(r))
conn.commit()

with conn.cursor() as cur:
    cur.execute("SELECT id, code, date, close FROM t_replace")
    after_rep = cur.fetchone()


# ON DUPLICATE KEY UPDATE로 동일하게 진행
make_table("t_odku", unique=True)
with conn.cursor() as cur:
    cur.execute(f"REPLACE INTO t_odku ({COL_SQL}) VALUES ({PH})", rows[0])
conn.commit()

with conn.cursor() as cur:
    cur.execute(UPSERT.format(t="t_odku"), tuple(r))
conn.commit()

with conn.cursor() as cur:
    cur.execute("SELECT id, code, date, close FROM t_odku")
    after_odku = cur.fetchone()

print(f"""
    REPLACE INTO가 위험한 이유 - ID
    최초 INSERT : {before['id'] - {before['close']}}
    REPLACE INTO : {after_rep['id'] - {after_rep['close']}}
    ON DUPLICATE KEY : {after_odku['id'] - {after_odku['close']}}
""")

"""
    REPLACE는 내부적으로 DELETE 후에 INSERT를 실행한다.
    그래서 ID(식별키)를 다시 생성해서 부여한다.
    추후 원래 행을 ID로 조회할 수 없으며, 만약 외래키로 사용되었다면 데이터가 깨진다.
"""

# 신규 데이터와 갱신데이터를 구분하여 기록
"""
    MySQL에서 ON DUPLICATE KEY UPDATE의 결과를 rowcount로 알려준다.
    신규 -> 1
    값이 변경된 갱신 -> 2
    값이 같아 변화 없음 -> 0

    이를 통해서 몇 건이 새로 들어오고, 몇 건이 갱신되었는지 알 수 있다.
"""

def upsert_with_stats(table, data, chunk=1000):
    """ 청크마다 커밋하면서 신규 / 갱신 건 수를 집계하는 함수 """
    inserted = updated = 0

    start = time.perf_counter()

    for i in range(0, len(data), chunk):
        part = data[i:i+chunk]
        with conn.cursor() as cur:
            affected = cur.executemany(UPSERT.format(t=table), part)
        conn.commit()   # 청크마다 커밋
        """
            affected = 신규*1 + 갱신*2 + 변화없음*0
            신슈를 i, 값이 바뀐 갱신을 u, 값이 같아 변화없는 것을 z라고 하면
            i + u + z = len(part)
            i + 2u = affected
            미지수가 셋이라서 한 식으로는 못 품, 그래서 두 경우로 나눠서 근사값을 구함
            affected > len(part) : 갱신이 존재한다, z=0이라고 보면
                                    u = affected - len(part),
                                    i = len(part)*2 - affected
            그 외... : 갱신이 없다고 보고 affected를 전부 신규로 센다.
        """
        inserted += max(0, len(part) * 2 - affected) if affected > len(part) else affected
        updated += affected - len(part) if affected > len(part) else 0

    return inserted, updated, time.perf_counter() - start

make_table("t_stats", unique=True)

ins1, upd1, t1 = upsert_with_stats("t_stats", rows)

print(f"\n [적재] t_stats (1회차)")
print(f"   입력    {len(rows):>8,}행")
print(f"   신규    {ins1:>8,}행")
print(f"   갱신    {upd1:>8,}행")
print(f"   시간    {t1:>8.2f}초")

ins2, upd2, t2 = upsert_with_stats("t_stats", rows)
print(f"\n [적재] t_stats (2회차 - 동일 데이터)")
print(f"   입력    {len(rows):>8,}행")
print(f"   신규    {ins2:>8,}행")
print(f"   갱신    {upd2:>8,}행")
print(f"   시간    {t2:>8.2f}초")


"""
    로그를 남기는 것은 매우 중요하다.
    재실행 시 전부 갱신으로 찍히면 멱등하게 동작했다는 것이고,
    전부 신규이면 중복이 쌓이고 있다는 뜻으로 해석이 가능하다.

    위 데이터에서 2회차에 신규0, 갱신0인 것은 정상이다.
    
    청크마다 커밋 + UPSERT조합으로 9만 건을 돌리는 도중
    5만 건에서 실패해도 앞 전에 적재한 데이터는 그대로 적제되고,
    5만 건 이후부터 재실행해서 갱신 처리하면 된다.
"""


# 적재 데이터 검증
expected = sample
actual = pd.read_sql(f"SELECT {COL_SQL} FROM t_stats", engine)

checks = [
    ("행 수", len(expected), len(actual)),
    ("종목 수", len(expected['code'].nunique()), len(actual['code'].nunique())),
    ("종가 합계", len(expected['close'].sum()), len(actual['close'].sum())),
    ("평균 종가", len(expected['close'].mean()), len(actual['close'].mean())),
    ("거래량 합계", len(expected['volume'].sum()), len(actual['volume'].sum())),
    ("최소 날짜", len(expected['date'].min().date()), len(actual['date'].min())),
    ("최대 날짜", len(expected['date'].max().date()), len(actual['date'].max())),
]

all_ok = True

for name, exp, act in checks:
    ok = str(exp) == str(act)
    all_ok &= ok
    print(f" {name:<14}{str(exp):>20}{str(act):>20}{'O' if ok else 'X':>8}")

print(f"\n 모든 값 일치 : {all_ok}")


"""
    갯수가 맞아도 값이 틀릴 수 있다.
    타입 변환해서 소수가 잘렸거나 인코딩이 깨졌거나 열 순서가 밀렸거나...
    집계값을 대조하면 이런 것들을 확인하기 쉽다.
"""

with conn.cursor() as cur:
    for t in ["t_noconstaint", "t_odku", "t_replace", "t_stats", "t_unique", "t_upsert"]:
        cur.execute(f"DROP TABLE IF EXISTS {t}")
conn.commit()
conn.close()
