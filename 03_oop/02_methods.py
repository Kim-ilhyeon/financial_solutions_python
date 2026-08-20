"""
    메서드 종류
    - 인스턴스 메소드(self)
    - 클래스 메서드 (@classmmethod, cls)
    - 정적 메서드 (@staticmethod)
"""

class Account:
    bank_name = "KH은행"
    MIN_DEPOSIT = 1000

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    # 인스턴스 메서드 : 객체의 데이터를 다움 (첫번째 인자가 self)
    def deposit(self, amount):
        self.balance += amount
        return self.balance

    # 클래스 메서드 : 클래스 제차레르 다룸. (첫번째 인자가 cls)
    @classmethod
    def from_dict(cls, data):
        """ 딕셔너리로부터 객체를 생성하는 메소드 """
        return cls(data["owner"], data.get("balance", 0))

    # 정적 메소드 : 객체, 클래스와 무관한 유팅함수
    @staticmethod
    def is_valid_amount(amount):
        return amount >= Account.MIN_DEPOSIT

acc = Account("김일현", 10000)
print(f" 인스턴스 메서드 : deposit(1500) -> {acc.deposit(1500)}")

raw = {"owner" : "김이현", "balance" : 50000}
acc2 = Account.from_dict(raw)

print(f" 클래스 메서드로 생성 : from_dict() -> {acc2.owner} {acc2.balance}")
print(f" 정적 메서드로 생성 : is_valid_amount() -> {Account.is_valid_amount(500)}")
print(f" 정적 메서드로 생성 : is_valid_amount() -> {Account.is_valid_amount(1500)}")

# from_dict와 같이 클래스 메소드로 왜 생성자를 만들까?
response = [
    {"owner" : "김일현", "balance" : 50000},
    {"owner" : "김이현"},
    {"owner" : "김삼현", "balance" : 30000},
]

accounts = [Account.from_dict(item) for item in response]

for a in accounts:
    print(f" {a.owner} {a.balance}원")

# 딕셔너리 구조를 자연스럽게 넘겨서 생성할 수 있다.
# 데이터 구조가 변경되거나 하면 메소드를 수정하거나 새로 정의해서 대응이 가능하다.

class VipAccount(Account):
    bank_name = "KH은행 VIP"

v = VipAccount.from_dict({"owner" : "김일현", "balance" : 120000})
print(f" VipAccount.from_dict() : {type(v)}")
print(f" bank_name : {v.bank_name}")

# 상속구조에서 class메소드의 cls매개변수를 동적으로 사용할 수 있는 이점이 있다.
