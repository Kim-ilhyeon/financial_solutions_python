"""
Extract - 원본을 가져와 그대로 보관한다.
- 여기서 정제하지 않는다.
- 수집처가 바뀌어도 이 파일만 고치면 된다.
"""

import time

import pandas as pd
import requests

from .config import (KHLAB_BASE, STUDENT_ID, MAX_PAGES, PAGE_SIZE,
                     TIMEOUT, DELAY, raw_prices_path, ENCODING)

# 누가 어떤 목적으로 요청하는지를 밝힌다.
HEADERS = {
    "User-Agent": "KHLab-Pipeline/1.0 (교육용 실습)",
    "X-Student-Id": STUDENT_ID,
}


def from_api(logger, max_pages=MAX_PAGES):
    """
    KH-LAB API 에서 수집한다.  

    반환 : (rows, failed)
             rows   - 응답 JSON 의 data 를 이어 붙인 list[dict]
             failed - 못 받아온 페이지 번호 목록
           from_csv 도 같은 모양의 튜플을 돌려준다. 
    """
    rows, failed = [], []

    # [requests.Session] 한 번 연 TCP 연결을 여러 요청이 나눠 쓴다
    with requests.Session() as s:
        s.headers.update(HEADERS)

        for page in range(1, max_pages + 1):
            try:
                # params 로 넘기면 ?page=1&size=100 을 알아서 조립하고 인코딩까지 해 준다.
                resp = s.get(f"{KHLAB_BASE}/api/v1/companies",
                             params={"page": page, "size": PAGE_SIZE},
                             timeout=TIMEOUT)
            except requests.RequestException as e:
                # RequestException 은 연결 실패·타임아웃 등을 모두 아우르는 부모 예외다.
                logger.warning(f"  page {page} 요청 실패: {type(e).__name__}")
                failed.append(page)
                continue          # ★ 멈추지 않는다. 이 페이지만 포기하고 다음으로 간다.

            if resp.status_code != 200:
                logger.warning(f"  page {page} 상태코드 {resp.status_code}")
                failed.append(page)
                continue

            body = resp.json()                 # 응답 본문(JSON 문자열)을 dict 로 바꾼다
            items = body.get("data") or []
            if not items:
                logger.info(f"  page {page} 0건 - 종료")
                break              

            rows.extend(items)     # append 는 리스트를 통째로 한 칸에 넣고, extend 는 풀어서 잇는다
            logger.info(f"  page {page} {len(items)}건 (누적 {len(rows)})")
            time.sleep(DELAY)      

    if failed:
        logger.warning(f"  실패한 페이지: {failed}")

    return rows, failed


def from_csv(logger, path=None):
    """
    CSV 에서 읽는다. API 가 불안정하거나 오프라인일 때 쓴다.
    """
    path = path or raw_prices_path()

    df = pd.read_csv(path, encoding=ENCODING, dtype=str, keep_default_na=False)
    logger.info(f"  {path} 에서 {len(df):,}행 읽음")

    # [to_dict("records")] DataFrame 을 행 단위 dict 의 리스트로 바꾼다
    return df.to_dict("records"), []
