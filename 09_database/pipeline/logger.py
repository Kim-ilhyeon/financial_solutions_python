"""
로깅 설정.

print 를 쓰지 않는 이유
  · 레벨 구분이 없다
  · 화면에만 남는다 - 자동 실행되는 프로그램에는 화면이 없다
  · 시각을 직접 붙여야 한다
  · 끄려면 코드를 지워야 한다
"""

import logging
import os
from datetime import datetime

from .config import LOG_DIR


def setup(name="pipeline", level=logging.INFO):
    """
    화면과 파일에 동시에 기록하는 로거를 만들어 돌려준다.

    로깅의 구조는 세 조각이다.
      Logger    - 코드가 말을 거는 창구.  logger.info("...") 를 부르는 그것.
      Handler   - 그 말을 어디로 내보낼 것인가. 화면(Stream) / 파일(File)
      Formatter - 어떤 서식으로 찍을 것인가. 시각·레벨·내용
    Logger 하나에 Handler 를 둘 붙였기 때문에 한 번의 info() 가 두 곳에 남는다.
    """
    # exist_ok=True : 폴더가 이미 있어도 에러를 내지 않는다. 없으면 만든다.
    os.makedirs(LOG_DIR, exist_ok=True)

    # 파일명을 날짜로 두면 하루치가 한 파일에 모인다. (20260902.log)
    path = os.path.join(LOG_DIR, f"{datetime.now():%Y%m%d}.log")

    # [logging.getLogger] 이름표가 붙은 로거를 가져온다
    logger = logging.getLogger(name)

    # [setLevel] 이 레벨보다 낮은 기록은 버린다
    logger.setLevel(level)

    # 핸들러를 비우고 시작한다.
    logger.handlers.clear()

    # [Formatter] 한 줄을 어떤 모양으로 찍을지 정한다
    fmt = logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s", "%H:%M:%S")

    # [StreamHandler] 화면(표준 출력)으로 내보낸다
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    # [FileHandler] 파일에 덧붙여 쓴다
    file = logging.FileHandler(path, encoding="utf-8")
    file.setFormatter(fmt)
    logger.addHandler(file)

    return logger
