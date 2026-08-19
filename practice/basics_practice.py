"""
TODO 부분을 직접 채워서 완성하세요.
"""

BASE_YEAR = 2026


while True:
    print()
    print("=" * 46)
    print(" 교안 1 PRACTICE")
    print("=" * 46)
    print(" 1. 나이 계산기")
    print(" 2. 가격 문자열 정제")
    print(" 3. 학점 판정")
    print(" 4. 별 찍기")
    print(" 5. 종목별 등락 출력")
    print(" 6. 숫자 맞추기 게임")
    print(" q. 종료")
    print("-" * 46)

    menu = input("번호 선택 > ").strip()

    # =====================================================================
    # PRACTICE 1. 나이 계산기
    #   출생연도를 입력받아 만 나이와 성인 여부를 출력 (기준연도 2026)
    #
    #   [출력 예시]
    #     출생연도를 입력하세요: 2001
    #     2001년생은 2026년 기준 만 25세, 성인입니다.
    #
    #   [힌트] input()은 문자열을 돌려준다. 뺄셈을 하려면 무엇이 필요할까?
    #          "성인" / "미성년자" 는 삼항 연산으로 한 줄에 쓸 수 있다.
    # =====================================================================
    if menu == "1":
        print("\n[ 1. 나이 계산기 ]")

        # TODO: 출생연도를 입력받아 정수로 변환
        birth_year = int(input("출생연도를 입력하시오 : "))

        # TODO: 만 나이 계산
        exact_age = BASE_YEAR - birth_year

        # TODO: 삼항 연산으로 성인 여부 판정 (19세 이상이면 성인)
        is_adult = "성인" if exact_age >= 19 else "미성년자"

        # TODO: f-string으로 결과 출력
        print(f"{birth_year}년생은 {BASE_YEAR}년 기준 만 {exact_age}세, {is_adult}입니다.")

    # =====================================================================
    # PRACTICE 2. 가격 문자열 정제
    #   "  2,480,000 원 " -> 숫자만 추출 -> 부가세 10% 포함 -> 천단위 콤마
    #
    #   [출력 예시]
    #     최종 금액  : 2,728,000원
    #
    #   [힌트] strip() / replace() 를 어떤 순서로 쓸지 생각해 볼 것.
    #          '원'을 지우고 나면 공백이 남는다. 한 번에 하려 하지 말고
    #          단계마다 print로 확인하며 붙여나갈 것.
    #          천단위 콤마는 f"{값:,}" 형식.
    # =====================================================================
    elif menu == "2":
        print("\n[ 2. 가격 문자열 정제 ]")

        raw_price = "  2,480,000 원 "
        print(f"원본       : [{raw_price}]")

        # TODO: 단계별로 정제해 정수 price 만들기
        price_str = raw_price.strip()
        print(f"price : [{price_str}]")
        price_split = price_str.split(" ")
        print(f"price.split : [{price_split}]")

        price_replace = price_split[0].replace(',', '')

        price = int(price_replace)

        # TODO: 부가세 10%를 포함한 total 계산
        total = int(price + price * 0.1)

        # TODO: 천단위 콤마 형식으로 출력
        result = f"{price:,}"
        print(f"최종 금액 : {result} 원")

    # =====================================================================
    # PRACTICE 3. 학점 판정
    #   A(90~) / B(80~) / C(70~) / D(60~) / F(~59)
    #   0~100 범위를 벗어나면 "잘못된 입력"
    #
    #   [힌트] 범위 검사를 먼저 할 것.
    #          조건은 '좁은 것부터' 써야 한다. 순서를 뒤집으면 95점이 D가 된다.
    # =====================================================================
    elif menu == "3":
        print("\n[ 3. 학점 판정 ]")

        # TODO: 점수 입력받기
        score = int(input("점수를 입력하시오 : "))

        if 0 <= score <= 100:
            if score >= 90:
                grade = "A"
            elif score >= 80:
                grade = "B"
            elif score >= 70:
                grade = "C"
            elif score >= 60:
                grade = "D"
            else:
                grade = "F"
            print(f"당신의 학점은 {grade}입니다.")
        else : 
            print(f"잘못된 입력")
        # TODO: 범위 검사 후 학점 판정

    # =====================================================================
    # PRACTICE 4. 별 찍기
    #   n=4 일 때
    #      *
    #     ***
    #    *****
    #   *******
    #
    #   [힌트] i번째 줄의 공백 개수와 별 개수를 각각 n, i로 표현해 볼 것.
    #          문자열 * 정수 는 '반복'이다. ("*" * 3  ->  "***")
    # =====================================================================
    elif menu == "4":
        print("\n[ 4. 별 찍기 ]")

        # TODO: n 입력받기
        n = int(input("숫자 입력 : "))
        # 공백 : n - 1
        # 별 갯수 : i * 2 - 1 (1, 3, 5, 7...)
        width = 2 * n - 1

        # TODO: 반복문으로 삼각형 출력
        for i in range(1, n+1):
            stars = "*" * (2*i-1)
            print(f"{stars :^{width}}")

        # 문자열 * 정수는 반복의 개념이다. -> 다른 언어였다면 반복문을 사용해서 찍어줘야 한다.

    # =====================================================================
    # PRACTICE 5. 종목별 등락 출력
    #   "1. 삼성전자: 71,200원 (상승)" 형식
    #   전일 대비 상승/하락/보합 표시
    #
    #   [힌트] zip()으로 세 리스트를 묶고, enumerate(..., start=1)로 번호를 붙인다.
    #          range(len(...)) 로 인덱스를 직접 돌리지 말 것.
    # =====================================================================
    elif menu == "5":
        print("\n[ 5. 종목별 등락 출력 ]\n")

        stocks = ["삼성전자", "SK하이닉스", "NAVER", "카카오"]
        today = [71200, 185000, 198000, 42150]
        yesterday = [70500, 185000, 201000, 43000]

        # TODO: zip + enumerate로 순회하며 형식에 맞게 출력
        for i, (name, now, prev) in enumerate(zip(stocks, today, yesterday), start=1):
            if now-prev > 0:
                diff = "상승"
            elif now-prev < 0:
                diff = "하락"
            else:
                diff = "보합"

            print(f"{i}. {name}: {now:,}원 ({diff})")


    # =====================================================================
    # PRACTICE 6. 숫자 맞추기 게임
    #   1~100 사이의 정답을 정해두고 while로 입력받아 힌트 제공
    #   맞히면 시도 횟수를 출력하고 종료
    #
    #   [힌트] while True + break 구조.
    #          Python에는 ++ 연산자가 없다. count += 1 을 쓴다.
    # =====================================================================
    elif menu == "6":
        print("\n[ 6. 숫자 맞추기 게임 ]")

        answer = 73
        tries = 0

        # TODO: while 반복문으로 게임 구현
        while True:
            input_answer = int(input("정답 : ").split())
            tries += 1
            if input_answer == answer:
                break
            elif input_answer > answer:
                print("더 작은 수를 입력하세요.")
            elif input_answer < answer:
                print("더 큰 수를 입력하세요.")


        print(f"정답입니다.\n시도 횟수는 {tries}번입니다.")

    elif menu == "q":
        print("\n종료합니다.")
        break

    else:
        print("\n잘못된 선택입니다. 1~6 또는 q를 입력하세요.")