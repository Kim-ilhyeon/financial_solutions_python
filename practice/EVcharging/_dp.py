"""
    DB 접속 공통 모듈
"""

import os, pymysql

from dotenv import load_dotenv
from sqlalchemy import create_engine

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ENCODING = "utf-8-sig"

# .env파일을 읽어서 os.environ에 채워 넣는다.
load_dotenv()

HOST = os.getenv("DB_HOST", "127.0.0.1")
PORT = int(os.getenv("DB_PORT", 3306))   
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")

# connection을 반환하는 함수
def connect(autocommit=False):
    """ MySQL에 연결 후 커넥션을 반환하는 함수 """

    # MySQL에 연결
    return pymysql.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD, database=NAME,
        charset="utf8mb4",
        autocommit=autocommit,
        # cursorclass=DictCursor : 결과를 튜플이 아니라 dict 로 받는다.
        cursorclass=pymysql.cursors.DictCursor,
    )


# SQLAlchemy의 엔진을 반환
def get_engine():
    """ SQLAlchemy의 엔진을 반환하는 함수 """
    url = (
        f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
        "?charset=utf8mb4"
    )
    # pool_pre_ping : 풀에서 커넥션을 꺼낼 때 "아직 살아 있나" 를 한 번 찔러 본다.
    return create_engine(url, pool_pre_ping=True)


def data_path(name):
    """data/ 안의 파일 경로. 작은 파일은 항상 로컬에서 읽는 함수"""
    return os.path.join(DATA_DIR, name)

def regions_path():
    """ 지역 정보 데이터를 불러오는 함수 """
    local = data_path("regions.csv")
    if os.path.exists(local):
        return local
    print(f"{'='*50} {local}데이터를 불러오지 못했습니다. {'='*50}")

def raw_stations_path():
    """ 충전소 데이터를 불러오는 함수 """
    local = data_path("raw-stations.csv")
    if os.path.exists(local):
        return local
    print(f"{'='*50} {local}데이터를 불러오지 못했습니다. {'='*50}")
    

def raw_charging_logs_path():
    """ 충전 기록 데이터를 불러오는 함수 """
    local = data_path("raw-charging-logs.csv")
    if os.path.exists(local):
        return local
    print(f"{'='*50} {local}데이터를 불러오지 못했습니다. {'='*50}")