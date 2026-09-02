"""
Load - DB 에 적재한다. 가공하지 않는다.
"""

import time

from .config import connect, CHUNK_SIZE

COLS = ["code", "date", "open", "high", "low", "close", "volume", "change", "changeRate"]
COL_SQL = ", ".join(f"`{c}`" for c in COLS)
PH = ", ".join(["%s"] * len(COLS))

UPSERT = f"""
INSERT INTO daily_price ({COL_SQL}) VALUES ({PH})
ON DUPLICATE KEY UPDATE
    open=VALUES(open), high=VALUES(high), low=VALUES(low),
    close=VALUES(close), volume=VALUES(volume),
    `change`=VALUES(`change`), changeRate=VALUES(changeRate)
"""


def to_db(df, logger, chunk=CHUNK_SIZE):
    """
    UPSERT 로 적재하고 신규·갱신 건수를 돌려준다.

    적재는 중간에 실패하면 멈추는 편이 낫다.
    """

    # NaN 을 None 으로 바꿔야 한다
    data = df[COLS].astype(object).where(df[COLS].notna(), None)
    # executemany 가 요구하는 '튜플의 리스트'. COLS 순서가 아래 SQL 의 %s 자리와 짝이다.
    rows = [tuple(r) for r in data.itertuples(index=False)]

    conn = connect()
    inserted = updated = 0
    start = time.perf_counter()

    try:
        for i in range(0, len(rows), chunk):
            part = rows[i:i + chunk]
            with conn.cursor() as cur:
                affected = cur.executemany(UPSERT, part)
            # 청크마다 커밋한다.
            conn.commit()

            if affected > len(part):
                updated += affected - len(part)
                inserted += len(part) * 2 - affected
            else:
                inserted += affected
    except Exception:
        # 커밋하지 못한 마지막 청크를 되돌린다. 그리고 예외는 그대로 위로 올린다.
        conn.rollback()
        raise
    finally:
        # 성공하든 실패하든 연결은 반드시 닫는다. 
        conn.close()

    return inserted, updated, time.perf_counter() - start


def verify(df, logger):
    """
    적재 후 검증. 행 수만 보면 놓치므로 집계값도 대조한다.

    개수가 맞아도 값이 틀릴 수 있다
    """
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) AS n, COUNT(DISTINCT code) AS codes,
                   SUM(close) AS close_sum,
                   MIN(date) AS min_d, MAX(date) AS max_d
            FROM daily_price
        """)
        db = cur.fetchone()
    conn.close()

    expected = {
        "행 수": (len(df), db["n"]),
        "종목 수": (df["code"].nunique(), db["codes"]),
        "종가 합계": (int(df["close"].sum()), int(db["close_sum"])),
        "최소 날짜": (str(df["date"].min().date()), str(db["min_d"])),
        "최대 날짜": (str(df["date"].max().date()), str(db["max_d"])),
    }

    all_ok = True
    for name, (exp, act) in expected.items():
        ok = str(exp) == str(act)
        all_ok &= ok
        logger.info(f"  {'OK  ' if ok else 'FAIL'} {name:<12}{exp} / {act}")

    return all_ok
