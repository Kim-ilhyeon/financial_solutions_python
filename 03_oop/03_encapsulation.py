"""
    캡슐화
    - _name / __name 네이밍
    - 이름 맹글링
    - @property으로 getter/setter만들기
    

    특징
    - 정보은닉 : 객체 내부의 데이터를 마음대로 접근할 수 없게 만드는 것.
    - 데이터와 기능의 결합 : 객체의 데이터와 데이터를 다루는 메소드를 한 번에 모아서 관리를 한다.
"""

# _name / __name 네이밍 -> 파이썬은 private이 없음
class Account:

    def __init__(self, owner, balance=0):
        self.owner = owner          # public
        self._bank_code = "004"     # protected
        self.__balance = balance    # private : 이름 맹글링 적용됨

acc = Account("김일현", 10000)
print(f" acc.owner : {acc.owner}")
print(f" acc._bank_code : {acc._bank_code}")        # 에러안남 -> 약속

# print(acc.__balance) -> no attribute '__balance'에러가 발생

print(f"실제 이름 : {[k for k in vars(acc)]}")
print(f"_Account__balance : {acc._Account__balance}")

# 이름 맹글링
# : __name으로 인스턴스 변수 작성 시 접근을 막기 위해서 이름을 _class명__name형태로 변형시킨다.
# (우회해서 접근은 가능하지만 사용 금지)

print()

# @property - 속성처럼 사용 가능한 어노테이션

class SafeAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self):
        """ acc.balance로 읽을 때 자동으로 호출됨 = getter와 같은 역할 """
        return self.__balance

    @balance.setter
    def balance(self, value):
        """ setter : acc.balance = ...로 사용하면 자동 호출됨 """
        if value < 0:
            self.__balance = 0
            return
        
        self.__balance = value

    @property
    def info(self):
        return f"{self.owner} : {self.__balance}원"

acc = SafeAccount("김일현", 20000)
print(f" acc.balance = {acc.balance}")
acc.balance = 1000
print(f" acc.balance = {acc.balance}")
print(f" acc.info = {acc.info}")

