"""
DB 접속 공통 모듈.

접속 정보는 .env 에서만 읽는다. 코드에 비밀번호가 없다.
매 파일에서 connect() 또는 get_engine() 을 부르면 된다.

경로도 여기서 잡는다.
"""

import os

import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine

# .env 파일을 읽어 os.environ 에 채워 넣는다
load_dotenv()

# os.getenv("KEY", 기본값) : 환경변수가 없으면 기본값을 돌려준다.
HOST = os.getenv("DB_HOST", "127.0.0.1")
PORT = int(os.getenv("DB_PORT", 3306))   
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")

# KH-LAB API 
KHLAB_BASE = os.getenv("KHLAB_BASE", "https://khlab.oneground.ai.kr")
STUDENT_ID = os.getenv("STUDENT_ID", "student01")

# __file__ 은 '지금 이 파일(_db.py)의 경로' 다.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ENCODING = "utf-8-sig"
KHLAB_DATASETS = f"{KHLAB_BASE}/datasets"


def connect(autocommit=False):
    """
    MySQL 에 연결후 커넥션을 반환하는 함수

    autocommit 은 기본이 False 다.
      Spring 의 @Transactional 처럼 알아서 커밋해 주는 것이 없다.
      commit() 을 부르지 않으면 데이터가 사라진다. 에러도 나지 않는다.
    """

    #MySQL 에 연결한다. DDL 과 UPSERT 처럼 세밀한 제어가 필요할 때 쓴다.
    return pymysql.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD, database=NAME,
        charset="utf8mb4",
        autocommit=autocommit,
        # cursorclass=DictCursor : 결과를 튜플이 아니라 dict 로 받는다.
        cursorclass=pymysql.cursors.DictCursor,
    )


def get_engine():
    """
    SQLAlchemy 엔진을 만들어 반환한다.
    mysql+pymysql://사용자:비밀번호@호스트:포트/DB이름

    SQLAlchemy 가 pymysql 을 대체하는 것이 아니라, 그 위에서 도구로 쓴다.
    """
    url = (
        f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
        "?charset=utf8mb4"
    )
    # pool_pre_ping : 풀에서 커넥션을 꺼낼 때 "아직 살아 있나" 를 한 번 찔러 본다.
    return create_engine(url, pool_pre_ping=True)


def data_path(name):
    """data/ 안의 파일 경로. 작은 파일은 항상 로컬에서 읽는다."""
    return os.path.join(DATA_DIR, name)


def prices_path():
    """
    일별 시세 90,000행(정제본)의 경로 또는 URL.
    """
    local = data_path("prices.csv")
    if os.path.exists(local):
        return local
    return f"{KHLAB_DATASETS}/prices.csv"


def raw_prices_path():
    """일별 시세(오염본)의 경로 또는 URL. 정책은 prices_path 와 같다."""
    local = data_path("raw-prices.csv")
    if os.path.exists(local):
        return local
    return f"{KHLAB_DATASETS}/raw-prices.csv"
