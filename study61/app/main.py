import sys
from src import step01, step02, step03
step_map = {
    1: ("step01", step01.run),
    2: ("step02", step02.run),
    3: ("step03", step03.run),
    # 4: ("step04", step04.run),
}


def main():
  # 터미널 인자 읽기 (파일명 제외)
    args = sys.argv[1:]
    
    if not args:
        print("실행할 스텝 번호를 입력해주세요. (예: python main.py 3)")
        return

    for arg in args:
        try:
            step_num = int(arg)
            if step_num in step_map:
                title, func = step_map[step_num]
                print(f"\n" + "="*40)
                print(f"🚀 Step {step_num} 실행: {title}")
                print("="*40)
                
                # 함수 실행
                func()
            else:
                print(f"❌ Step {step_num}은 아직 정의되지 않았습니다.")
        except ValueError:
            print(f"❗ '{arg}'은(는) 올바른 숫자가 아닙니다.")

if __name__ == "__main__":
  main()


# from src import step01, step02

# def main():
#   print("Hello from app!")
#   # step01.run()
#   step02.run()

# if __name__ == "__main__":
#   main()
