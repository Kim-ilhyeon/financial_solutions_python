"""
환경 준비 확인  (수업 전 각자 실행)

이 파일은 준비가 끝났는지 확인하는 용도다.
아래 5가지를 순서대로 점검하고, 실패한 항목의 해결 방법을 알려준다.

  ① 패키지 설치
  ② .env 파일
  ③ MySQL 접속
  ④ 문자셋 (utf8mb4)
  ⑤ 권한 (테이블 생성/삭제)

전부 통과하면 수업 준비가 끝난 것이다.
"""

import os
import sys

OK = "  [ OK ]"
NG = "  [ 실패 ]"

results = []


def check(name, fn):
    """점검 항목 하나를 실행하고 결과를 기록한다."""
    print(f"\n{'=' * 60}")
    print(f" {name}")
    print("=" * 60)
    try:
        fn()
        results.append((name, True))
    except Exception as e:
        print(f"{NG} {type(e).__name__}: {e}")
        results.append((name, False))


# =====================================================================
def step1_packages():
    """① 패키지가 설치되어 있는가"""
    need = {
        "pymysql": "MySQL 드라이버",
        "sqlalchemy": "DB 추상화 계층 (Pandas 연동)",
        "dotenv": "환경변수 로딩",
        "pandas": "데이터 처리",
        "requests": "API 호출 (교안 19)",
    }
    missing = []
    for mod, desc in need.items():
        try:
            m = __import__(mod)
            ver = getattr(m, "__version__", "")
            print(f"{OK} {mod:<14}{ver:<12}{desc}")
        except ImportError:
            print(f"{NG} {mod:<14}{'':<12}{desc}")
            missing.append(mod)

    if missing:
        # 패키지 목록은 프로젝트 루트에 하나로 모여 있다. 이 파일은 11_database 안에서 돌므로 ../ 다.
        raise RuntimeError(
            f"설치되지 않은 패키지: {missing}\n"
            "         해결: pip install -r ../requirements.txt"
        )


# =====================================================================
def step2_env():
    """② .env 파일이 있고 값이 채워져 있는가"""
    from dotenv import load_dotenv

    if not os.path.exists(".env"):
        raise FileNotFoundError(
            ".env 파일이 없습니다.\n"
            "         해결: cp .env.example .env   (Windows: copy .env.example .env)\n"
            "               그다음 DB_PASSWORD 를 본인 비밀번호로 바꾸세요."
        )

    load_dotenv()

    required = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    for key in required:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} 가 비어 있습니다.")
        # 비밀번호는 화면에 그대로 찍지 않는다
        shown = "*" * len(value) if "PASSWORD" in key else value
        print(f"{OK} {key:<14}{shown}")

    if "여기에" in os.getenv("DB_PASSWORD", ""):
        raise ValueError(
            "DB_PASSWORD 가 예시값 그대로입니다.\n"
            "         .env 를 열어 본인 비밀번호로 바꾸세요."
        )

    # .gitignore 확인 - 실수로 커밋되는 것을 막는다.
    #   이 프로젝트는 .gitignore 를 루트에 하나만 둔다. 이 파일은 11_database 안에서
    #   돌기 때문에 현재 폴더와 그 위 폴더를 차례로 본다.
    for candidate in (".gitignore", os.path.join("..", ".gitignore")):
        if os.path.exists(candidate):
            with open(candidate, encoding="utf-8") as f:
                if ".env" in f.read():
                    print(f"{OK} .gitignore  에 .env 등록됨  ({candidate})")
                else:
                    print(f"{NG} {candidate} 에 .env 가 없습니다! 반드시 추가하세요.")
            break
    else:
        # for 문이 break 없이 끝났을 때만 실행되는 else 다. 후보를 다 못 찾았다는 뜻이다.
        print(f"{NG} .gitignore 를 찾지 못했습니다. 프로젝트 루트에서 실행 중인지 확인하세요.")


# =====================================================================
def step3_connect():
    """③ MySQL 에 접속되는가"""
    import pymysql
    from dotenv import load_dotenv

    load_dotenv()

    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )
    except pymysql.err.OperationalError as e:
        code = e.args[0]
        hint = {
            1044: f"'{os.getenv('DB_NAME')}' DB 에 접근 권한이 없거나 DB 가 없습니다. "
                  "SETUP.md 2단계를 확인하세요.",
            1045: "비밀번호가 틀렸습니다. .env 의 DB_PASSWORD 를 확인하세요.",
            1049: f"'{os.getenv('DB_NAME')}' DB 가 없습니다. SETUP.md 의 2단계를 실행하세요.",
            2003: "MySQL 서버가 실행 중이 아닙니다. 서비스를 시작하세요.",
        }.get(code, "SETUP.md 를 확인하세요.")
        raise RuntimeError(f"{e}\n         → {hint}")
    except UnicodeEncodeError:
        # 비밀번호에 한글이 들어간 경우 여기로 온다
        raise RuntimeError(
            "접속 정보에 한글이 들어 있습니다.\n"
            "         → DB 비밀번호·사용자명은 영문·숫자·기호로만 만드세요.\n"
            "           한글 비밀번호는 드라이버가 처리하지 못합니다."
        )

    with conn.cursor() as cur:
        cur.execute("SELECT VERSION()")
        print(f"{OK} 서버 버전   {cur.fetchone()[0]}")
        cur.execute("SELECT DATABASE()")
        print(f"{OK} 현재 DB     {cur.fetchone()[0]}")
    conn.close()

    # SQLAlchemy 도 확인한다 (Pandas 연동에 필요)
    from sqlalchemy import create_engine, text

    url = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        "?charset=utf8mb4"
    )
    engine = create_engine(url)
    with engine.connect() as c:
        c.execute(text("SELECT 1"))
    print(f"{OK} SQLAlchemy  엔진 생성 및 접속 성공")


# =====================================================================
def step4_charset():
    """④ 문자셋이 utf8mb4 인가"""
    import pymysql
    from dotenv import load_dotenv

    load_dotenv()
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"), charset="utf8mb4",
    )

    with conn.cursor() as cur:
        cur.execute("SELECT @@character_set_database, @@collation_database")
        charset, collation = cur.fetchone()
        print(f"{OK} 문자셋      {charset}")
        print(f"{OK} 콜레이션    {collation}")

        if charset != "utf8mb4":
            conn.close()
            raise ValueError(
                f"문자셋이 '{charset}' 입니다. utf8mb4 여야 합니다.\n"
                "         MySQL 의 utf8 은 3바이트까지만 지원하는 반쪽짜리입니다.\n"
                "         해결: ALTER DATABASE khlab CHARACTER SET utf8mb4 "
                "COLLATE utf8mb4_unicode_ci;"
            )

        # 한글과 이모지를 실제로 넣어 본다
        cur.execute("DROP TABLE IF EXISTS _charset_test")
        cur.execute("CREATE TABLE _charset_test (txt VARCHAR(50))")
        cur.execute("INSERT INTO _charset_test VALUES (%s)", ("가온전자 📈",))
        conn.commit()

        cur.execute("SELECT txt FROM _charset_test")
        got = cur.fetchone()[0]
        cur.execute("DROP TABLE _charset_test")
        conn.commit()

    conn.close()

    if got == "가온전자 📈":
        print(f"{OK} 한글·이모지 저장/조회 정상  ('{got}')")
    else:
        raise ValueError(f"문자가 깨졌습니다: '{got}'")


# =====================================================================
def step5_privileges():
    """⑤ 테이블을 만들고 지울 권한이 있는가"""
    import pymysql
    from dotenv import load_dotenv

    load_dotenv()
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"), charset="utf8mb4",
    )

    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS _perm_test")
        cur.execute("""
            CREATE TABLE _perm_test (
                id   INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(10),
                UNIQUE KEY uk_code (code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print(f"{OK} CREATE TABLE (UNIQUE 제약 포함)")

        cur.execute("INSERT INTO _perm_test (code) VALUES (%s)", ("G0001",))
        conn.commit()
        print(f"{OK} INSERT / COMMIT")

        # UPSERT 가 동작하는지 (교안 18의 핵심)
        cur.execute(
            "INSERT INTO _perm_test (code) VALUES (%s) "
            "ON DUPLICATE KEY UPDATE code = VALUES(code)",
            ("G0001",),
        )
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM _perm_test")
        n = cur.fetchone()[0]
        print(f"{OK} UPSERT 동작 확인 (같은 키 2번 넣고 {n}행)")

        cur.execute("DROP TABLE _perm_test")
        conn.commit()
        print(f"{OK} DROP TABLE")

    conn.close()

    if n != 1:
        raise ValueError(f"UPSERT 후 행이 {n}개입니다. 1개여야 합니다.")


# =====================================================================
if __name__ == "__main__":
    print("=" * 60)
    print(" 실습 환경 점검")
    print("=" * 60)
    print(f"  Python {sys.version.split()[0]}")
    print(f"  작업 폴더 {os.getcwd()}")

    check("① 패키지 설치", step1_packages)
    check("② .env 파일", step2_env)
    check("③ MySQL 접속", step3_connect)
    check("④ 문자셋 (utf8mb4)", step4_charset)
    check("⑤ 권한 (CREATE / INSERT / UPSERT / DROP)", step5_privileges)

    print("\n" + "=" * 60)
    print(" 결과")
    print("=" * 60)
    for name, ok in results:
        print(f"  {'통과' if ok else '실패'}   {name}")

    passed = sum(ok for _, ok in results)
    print(f"\n  {passed} / {len(results)} 항목 통과")

    if passed == len(results):
        print("\n  준비가 끝났습니다.")
    else:
        print("\n  실패한 항목의 안내를 따라 해결한 뒤 다시 실행하세요.")
        sys.exit(1)
