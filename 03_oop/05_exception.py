"""
    예외 처리
    - try / except / else / finally
    - raise와 사용자 정의 예외 (Java에서의 Throw)
"""

def divide(text):
    try :
        num = int(text)
        result = 100 / num
    except ValueError:
        print(f" {text} -> 숫자가 아니다.")
    except ZeroDivisionError:
        print(f" {text} -> 0으로 나눌 수 없다.")
    except Exception as e:
        print(f" {text} -> {e}")
    else:   # 예외가 아닐때에만 실행
        print(f" {text} --> {result}")
    finally:
        pass # 항상 실행

for t in ["abc", "4", "0"]:
    divide(t)

# raise와 사용자 정의 예외
class NoBalanceError(Exception):
    """ 잔액 부족 예외 """
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f" 잔액 부족 : 현재-{balance}, 요청-{amount}")

class InvalidAmountError(ValueError):
    """ 금액이 잘못된 경우 """

class Account:

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("출금액은 0보다 커야 합니다.")

        if amount > self.balance:
            raise NoBalanceError(self.balance, amount)
            return

        self.balance -= amount
        return amount

    def info (self):
        return f"[{self.owner}] 잔액 : {self.balance:,}원"


acc = Account("김일현", 40000)
for amount in [5000, 50000, -100]:
    try:
        acc.withdraw(amount)
    except NoBalanceError as e:
        print(f"  [잔액부족] {e}")
    except InvalidAmountError as e:
        print(f"[출금액 오류] {e}")
    else:
        print(f" 출금 성공!!")
    finally:
        pass
