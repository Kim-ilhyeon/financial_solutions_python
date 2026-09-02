"""
    DB연동 및 조심할 것 3가지
"""

import pandas as pd
import pymysql

from _db import connect, get_engine, HOST, PORT, USER, NAME, PASSWORD

pd.set_option("display.width", 130)


# DB 연동 순서 및 방식은 Java와 다르지 않다.

# pymysql의 connection객체를 만들어서 반환받는다.
conn = connect()

# cursor() -> Cursor객체를 만들어줌.
# cur를 통해서 execute(sql), execute(sql, (값1, 값2, ...))를 통해서 sql을 전달 후 응답 받는 객체
with conn.cursor() as cur:
    cur.execute(
        "SELECT VERSION() AS v, DATABASE() AS db"
    )

    row = cur.fetchone()    # 한 행짜리 결과: fetchone, 여러 행짜리 결과 : fetchall

print(f" 접속 : {USER}@{HOST}:{PORT}/{NAME}")
print(f" 서버 : {row['v']} / 현재 DB : {row['db']}")

# 기본적으로 autocommit이 꺼져있다.
with conn.cursor() as cur:
    cur.execute(
        "DROP TABLE IF EXISTS demo_commit"
    )

    cur.execute(
        "CREATE TABLE demo_commit (id INT, memo VARCHAR(50))"
    )
conn.commit()

c1 = connect()
with c1.cursor() as cur:
    cur.execute(
        "INSERT INTO demo_commit VALUES (1, '커밋 안함')"
    )
    cur.execute(
        "SELECT COUNT(*) AS n FROM demo_commit"
    )
    print(f" insert후에 바로 확인 : {cur.fetchone()['n']}행")
c1.close()

c2 = connect()
with c2.cursor() as cur:
    cur.execute(
        "SELECT COUNT(*) AS n FROM demo_commit"
    )
    print(f" 새로운 커넥션에서 확인 : {cur.fetchone()['n']}행")
c2.close()

"""
    커밋하지 않고 커넥션 반납시에도 따로 에러가 나지 않기 때문에
    트랜잭션 관리를 잘 해줘야 한다.
"""

c3 = connect()
with c3.cursor() as cur:
    cur.execute(
        "INSERT INTO demo_commit VALUES (2, '두번째 데이터')"
    )
# c3.open -> c3 커넥션의 연결상태 확인
closed = not c3.open
c3.close()

c4 = connect()
with c4.cursor() as cur:
    cur.execute(
        "SELECT COUNT(*) AS n FROM demo_commit"
    )
    n_after = cur.fetchone()['n']
c4.close()

print(f" 종료 후 연결 상태 : {closed}")
print(f" 종료 후 데이터 : {n_after}")

"""
    close()를 하지 않아도 with가 종료되면 연결을 자동으로 닫는다.
    자동으로 닫을 시 커밋하지 않고 rollback 후에 닫는다.
"""

c5 = connect()
try :
    with c3.cursor() as cur:
        cur.execute(
            "INSERT INTO demo_commit VALUES (3, '명시적 커밋')"
        )
    c5.commit()
except:
    c5.rollback()
finally :
    c5.close()
closed = not c5.open

c6 = connect()
with c6.cursor() as cur:
    cur.execute(
        "SELECT COUNT(*) AS n FROM demo_commit"
    )
    n_after = cur.fetchone()['n']
c6.close()

print(f" 종료 후 연결 상태 : {closed}")
print(f" 종료 후 데이터 : {n_after}")


# 파라미터 바인딩
# executemany(sql, [(), (), (), ...]) : 같은 sql을 값만 바꿔서 여러 번 전달
with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS demo_param")
    cur.execute("CREATE TABLE demo_param (code VARCHAR(10), price INT)")
    cur.executemany(
        "INSERT INTO demo_param VALUES(%s, %s)",
        [('G0001', 24000), ('G0002', 51000), ('G0003', 10000)],
    )

conn.commit()

"""
    executemany 내부 변수는 타입과 무관한게 항상 %s -> ?
"""

with conn.cursor() as cur:
    cur.execute("SELECT * FROM demo_param WHERE price > %s", (2000,))
    print(f" {len(cur.fetchall())}행")

# 파라미터는 한개를 넘기더라도 튜플로 넣는다.
# 물론 변수가 하나이면 문자열을 그대로 전달해도 동작한다. (하지만 튜플로 써주는 것이 좋다.)
# 다만 변수가 여러 개인데 문자열 하나 전달 시 문자열을 알아서 쪼개서 사용한다. (문제발생 요소)



# DictCursor와 Pandas
plain = pymysql.connect(
    host=HOST, port=PORT, user=USER,
    passwd=PASSWORD, database=NAME, charset="utf8mb4"
)


# cursor의 기본 반환 값은 튜플이다.
with plain.cursor() as cur:
    cur.execute(
        "SELECT * FROM demo_param LIMIT 1"
    )
    print(f" 기본 커서 : {cur.fetchone()}")
plain.close()

with conn.cursor() as cur:
    cur.execute(
        "SELECT * FROM demo_param LIMIT 1"
    )
    print(f" Dict 커서 : {cur.fetchone()}")
# conn.close()

print("="*80)

# SQLAlchemy를 사용하는 가장 큰 이유는 Pandas와의 연계성 때문이다.
# create_engine : 커넥션 풀을 만들어서 관리해주는 engine을 생성
engine = get_engine()

# 만약 가능하다면 DB에서 정렬 후 데이터를 가져오는것이 빠르다.
# dataFrame에서 분석 후 정렬보다 DB에는 인덱싱이라는 개념으로 인해서 정렬이 비교적 더 빠르기 때문이다.
df = pd.read_sql(
    "SELECT * FROM demo_param ORDER BY price DESC", engine
)
print(df.to_string(index=False))


with conn.cursor() as cur:
    for t in ["demo_commit", "demo_param"]:
        cur.execute(f"DROP TABLE IF EXISTS {t}")

conn.commit()
conn.close()
