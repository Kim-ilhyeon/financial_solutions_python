"""
    모듈과 패키지
"""
# 모듈은 import

# 모듈 전체를 가져온다
import utils

print(f" 1200원 : {utils.clear_price(' 1200 원')}")

# 필요한 것만 가져오겠다.
from utils import to_code, BASE_URL

print(f" to_code(5910) : {to_code(5910)}")
print(f" BASE_URL : {BASE_URL}")

# 별칭 사용
from utils import clear_price as cp
print(f" clean_price('1200원') : {cp('1200원')}")







