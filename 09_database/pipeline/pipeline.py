"""
전체 흐름.

이 파일만 읽어도 무슨 일이 일어나는지 알 수 있어야 한다.
"""

import sys
import time

from . import extract, transform, load
from .config import SOURCE
from .logger import setup


def run(source=SOURCE):
    logger = setup()
    t0 = time.perf_counter()

    logger.info("=" * 58)
    logger.info(f" 파이프라인 시작  (source={source})")
    logger.info("=" * 58)

    # ── Extract ────────────────────────────────────────────
    logger.info("[Extract]")
    t = time.perf_counter()
    if source == "api":
        records, failed = extract.from_api(logger)
    else:
        records, failed = extract.from_csv(logger)

    if not records:
        logger.error("  수집 결과가 비어 있습니다. 중단합니다.")
        return False

    logger.info(f"  {len(records):,}건 수집  ({time.perf_counter() - t:.1f}초)")
    if failed:
        # 실패 목록을 남겨두면 나중에 그것만 다시 돌릴 수 있다
        logger.warning(f"  실패 {len(failed)}건: {failed}")

    # ── Transform ──────────────────────────────────────────
    logger.info("[Transform]")
    t = time.perf_counter()
    df = transform.clean_prices(records, logger)
    transform.validate(df, logger)
    logger.info(f"  완료  ({time.perf_counter() - t:.1f}초)")

    # ── Load ───────────────────────────────────────────────
    logger.info("[Load]")
    try:
        ins, upd, elapsed = load.to_db(df, logger)
    except Exception as e:
        # 적재 실패는 멈춘다. 반쪽짜리 데이터가 더 위험하다.
        logger.error(f"  적재 실패: {type(e).__name__}: {e}")
        return False

    logger.info(f"  입력 {len(df):>8,}행")
    logger.info(f"  신규 {ins:>8,}행")
    logger.info(f"  갱신 {upd:>8,}행")
    logger.info(f"  소요 {elapsed:>8.1f}초")

    logger.info("[Verify]")
    ok = load.verify(df, logger)

    logger.info("=" * 58)
    logger.info(f" {'완료' if ok else '검증 실패'}  총 {time.perf_counter() - t0:.1f}초")
    logger.info("=" * 58)
    return ok


if __name__ == "__main__":
    # 종료 코드로 성공·실패를 알린다. 0 이 성공, 0 이 아니면 실패다.
    sys.exit(0 if run() else 1)
