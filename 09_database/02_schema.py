"""
    수집 데이터를 위한 스키마 설계
"""

import pandas as pd
from _db import connect, raw_prices_path, ENCODING

pd.set_option("display.width", 130)

conn = connect()

# 원본 테이블 - 데이터를 받아서 저장이 목적이다.
RAW_DDL = """
    CREATE TABLE IF NOT EXISTS raw_daily_price(
        id              BIGINT AUTO_INCREMENT PRIMARY KEY,
        code            VARCHAR(20), 
        date            VARCHAR(20), 
        open            VARCHAR(30), 
        high            VARCHAR(30), 
        low             VARCHAR(30), 
        close           VARCHAR(30), 
        volme           VARCHAR(30), 
        `change`        VARCHAR(30),    -- change는 SQL 예약어라 백팁(`)으로 감싸기 
        changeRate      VARCHAR(30),
        -- 수집시각이나 출처 같은 따로 필요한 정보를 자유롭게 추가
        collected_at    DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 수집일
        source          VARCHAR(100)    -- 출처
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

with conn.cursor() as cur:
    cur.execute(
        "DROP TABLE IF EXISTS raw_daily_price"
    )
    cur.execute(RAW_DDL)
conn.commit()

"""
    원본 테이블 생성 시
    - 모든 컬럼은 문자열로 (어떤 값이든 원본 그대로 받을 수 있도록)
    - 제약조건을 걸지 않는다.
    - 수집시간 및 출처도 함께 기록

    원본을 무조건 저장해야하는 이유
    - 정제하는 로직이 잘못되어 잘못 정제된 데이터가 DB에 저장된 경우 원본이 없다면 되돌릴 수 없다.
"""

print("raw_daily_price 테이블 생성 완료")


raw_sample = pd.read_csv(raw_prices_path(), encoding=ENCODING,
                        dtype=str, keep_default_na=False)

bad = raw_sample[raw_sample["close"].isin(["N/A", "-"])].head(2)
good = raw_sample[~raw_sample["close"].isin(["N/A", "-"])].head(2)

mix = pd.concat([good, bad])

print("실제 저장된 정보 확인")
print(mix[["code", "date", "close"]].to_string(index=False))



# 제약이 있는 테이블에 비정제 데이터를 넣을 시
with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS demo_strict")
    cur.execute("""
        CREATE TABLE demo_strict(
            code VARCHAR(20), date DATE, close INT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
conn.commit()

# close INT NOT NULL로 만들 시에
success_count = 0
for _, r in mix.iterrows():
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO demo_strict VALUES (%s, %s, %s)",
                        (r["code"], r["date"], r["close"]))
        conn.commit()
        success_count += 1
    except Exception as e:
        conn.rollback()
        print(f"close={r['close']} -> {type(e)}.__name__")
print(f" 성공 : {success_count}건 / 4건")

# 제약없이 만든 원본 테이블에 데이터 추가
with conn.cursor() as cur:
    cur.executemany(
        "INSERT INTO raw_daily_price(code, date, close, source) VALUES (%s, %s, %s, %s)",
        [(r['code'], r['date'], r['close'], '실습데이터') for _, r in mix.iterrows()]
    )
conn.commit()

with conn.cursor() as cur:
    cur.execute(
        "SELECT COUNT(*) AS n FROM raw_daily_price"
    )
    print(f" 성공 {cur.fetchone()['n']}건 / 4건")


"""
    원본테이블은 데이터를 받아서 그대로 저장하는 것이 목적이고, 판단은 정제단계에서 한다.
"""

CLEAN_DDL = """
    CREATE TABLE IF NOT EXISTS daily_price(
        id              BIGINT AUTO_INCREMENT PRIMARY KEY,
        code            VARCHAR(20)     NOT NULL, 
        date            DATE            NOT NULL, 
        open            BIGINT, 
        high            BIGINT, 
        low             BIGINT, 
        close           BIGINT, 
        volme           BIGINT, 
        `change`        BIGINT,    -- change는 SQL 예약어라 백팁(`)으로 감싸기 
        changeRate      DECIMAL(6, 2),
        -- 수집시각이나 출처 같은 따로 필요한 정보를 자유롭게 추가
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP   -- 수정일
                            ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uk_code_date (code, date)        -- code와 date를 묶어서 unique하게 관리한다.
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

with conn.cursor() as cur:
    cur.execute(
        "DROP TABLE IF EXISTS daily_price"
    )
    cur.execute(CLEAN_DDL)
conn.commit()
print("daily_price 테이블 생성 완료")


"""
    float타입 금지 - 숫자를 나타낼때 이진법으로 나타내기 때문에 부동 소수점이 조금씩 생기는데 그러한 경우 오차가 누적된다.

    금액 : float타입 금지 - 오차가 누적된다.
    비율 : deciaml - 자릿수가 고정, 오차를 줄일 수 있다.
    날짜 : date - 문자열 저장 시 계산 및 정렬이 어렵다.
    코드 : varchar - 앞자리 0인 경우에 날라가는걸 방지하고 0을 그대로 보존하기 위해서
"""

with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS demo_strict")

conn.commit()
conn.close()

print("테이블 정리 완료")
