"""설정 - 환경변수와 상수를 한 곳에 모은다."""

import os
import sys

# 이 파일은 pipeline/ 안에 있는데, 쓰려는 _db.py 는 그 한 칸 위(11_database/)에 있다.
# insert(0, ...) 로 맨 앞에 끼워 넣으면 어디서 실행하든 _db 를 찾아낸다.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# noqa: E402 는 "import 가 파일 맨 위에 있지 않다" 는 린터 경고를 끄는 표시다.
#   위의 sys.path 조작이 먼저 끝나야 이 import 가 성공하므로 순서를 바꿀 수 없다.
from _db import (connect, get_engine, KHLAB_BASE, STUDENT_ID,   # noqa: E402
                 data_path, prices_path, raw_prices_path, ENCODING)

# Extract 방식 : "api" 또는 "csv"
# 수집처가 바뀌어도 이 값만 바꾸면 된다. Transform·Load 는 그대로다.
SOURCE = os.getenv("PIPELINE_SOURCE", "csv")

MAX_PAGES = int(os.getenv("PIPELINE_MAX_PAGES", 5))   # API 를 몇 페이지까지 훑을 것인가
PAGE_SIZE = 100        # 한 페이지에 몇 건을 달라고 할 것인가
CHUNK_SIZE = 5_000     # 몇 행씩 묶어 DB 에 보낼 것인가 
TIMEOUT = 5            # 응답을 몇 초까지 기다릴 것인가
DELAY = 1.0            # 요청 사이에 몇 초를 쉴 것인가 

# 로그는 logs/ 에 날짜별로 쌓인다.
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
