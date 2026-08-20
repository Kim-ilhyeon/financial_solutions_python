"""
    import하기위한 임시 모듈
    직접 실행할 수도 있고, 다른 파일에서 import할 수도 있다.
"""

BASE_URL = "https://khmain.co.kr"

def clear_price(text):
    """ '1000원'같은 문자열에서 숫자만 뽑아주는 함수 """
    return int(text.replace(",", "").replace("원", "").strip())

def to_code(number):
    """ 종목코드가 숫자로 전달되면 문자열로 만들어서 반환하는 함수 """
    return f" {number:06d}"

print(f" utils 모듈이 로드됨...")

