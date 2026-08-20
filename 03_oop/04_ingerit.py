"""
    상속과 다형성
    - 상속과 super()
    - 오버라이딩
    - 다형성
    - 덕 타이핑
    - 다중상속...?
"""

# 상속과 super()
class Account:

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("잔액이 부족합니다.")
            return

        self.balance -= amount
        return amount

    def info (self):
        return f"[{self.owner}] 잔액 : {self.balance:,}원"


class SavingAccount(Account):
    # 자식의 __init__을 만들면 반드시 super().__init__()호출이 필요하다.
    def __init__ (self, owner, balance=0, rate=0.03):
        super().__init__(owner, balance)    # 부모의 생성자를 호출
        # 내 필드가 필요하면 그 뒤에 작성
        self.rate = rate

    def add_interest(self):
        interest = int(self.balance * self.rate)
        self.balance += interest
        return interest

    def info(self):             # 오버라이딩 : 부모로부터 상속받은 메소드를 재정의한다.
        return f"{super().info()} / 이율 : {self.rate:.1%}"

s = SavingAccount("김일현", 1000000)
print(f" 이자 지급 : {s.add_interest():,}원")
print(f" info : {s.info()}")

print()

# 다형성
class CheckingAccount(Account):
    FEE = 500

    def withdraw(self, amount):
        total = amount + self.FEE
        if total > self.balance:
            print("잔액이 부족합니다.")
            return

        self.balance -= total

        return amount

    def info(self):
        return f"{super().info()} / 출금 수수료 {self.FEE}원"

accounts = [
    Account("김일현", 50000),
    SavingAccount("김이현", 100000),
    CheckingAccount("김삼현", 2000000),
]

for acc in accounts:
    print(f" {acc.info()}")

# 같은 info() 호출인데 객체마다 다른 결과를 보여주고 있다.

print()

# 덕 타이핑 : 오리처럼 걷고 오리처럼 울면, 그것은 오리이다.
# 상속 관계가 없어도 같은 이름의 메소드만 있으면 동일하게 취급된다.

class CsvExporter:
    def export(self, data):
        return f" csv로 {len(data)}건 저장"
    
class JsonExporter:
    def export(self, data):
        return f" json로 {len(data)}건 저장"

data = [1, 2, 3]
for exporter in [CsvExporter(), JsonExporter()]:
    print(f" {exporter.export(data)}")

print("Java였다면 공통 인터페이스를 구현한 다음, 인터페이스를 참조변수로 사용")
print("파이썬은 동일한 메소드를 가지고 있는가?만 판단해서 실행할 수 있다.")

class Loggable:
    def log(self, msg):
        return f"[LOG] {msg}"

class Serializable:
    def to_dict(self):
        return self.__dict__    # __dict__ : 해당 인스턴스가 가진 모든 필드 변수와 그 값을 딕셔너리 형태로 반환

class Product(Loggable, Serializable):
    def __init__ (self, name, price):
        self.name = name
        self.price = price

p = Product("동결건조딸기", 4000)
print(f" {p.log('상품 생성')}")
print(f" dict : {p.to_dict()}")

# 다중 상속은 메소드 충돌 시 추적이 어렵고, 부모쪽의 변수 제어가 쉽지 않아서 제한적으로 사용한다.
