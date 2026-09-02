
# # 파라미터 바인딩
# # executemany(sql, [(), (), (), ...]) : 같은 sql을 값만 바꿔서 여러 번 전달
# with conn.cursor() as cur:
#     cur.execute("DROP TABLE IF EXSIST demo_param")
#     cur.execute("CREATE TABLE demo_param (code VARCHAR(10), price INT)")
#     cur.execute()

