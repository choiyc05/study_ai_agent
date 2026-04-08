# from src import step01, step02, step03, step04

# def main():
#   print("Hello from app!")
#   # print("Step 1 실행: 챗봇 그래프 구축 및 이미지 저장")
#   # step01.run()
#   # print("Step 2 실행: 할일 목록 관리 그래프 구축 및 사용자 입력 처리")
#   # step02.run()
#   # print("Step 3 실행: 원하는 형태로 결과 만들기 - 구조화된 출력 활용하기")
#   # step03.run()
#   # print("Step 4 실행: 문법 교정과 번역기능이 있는 챗봇 구축하기")
#   # step04.run()

# if __name__ == "__main__":
#   main()


##
import sys
from src import step01, step02, step03, step04

# 스텝 번호와 실행 함수를 매핑합니다. 
# step08처럼 asyncio.run이 필요한 경우 람다(lambda)로 감싸서 통일감을 줍니다.
step_map = {
    1: ("챗봇 그래프 구축 및 이미지 저장", step01.run),
    2: ("할일 목록 관리 그래프 구축 및 사용자 입력 처리", step02.run),
    3: ("원하는 형태로 결과 만들기 - 구조화된 출력 활용하기", step03.run),
    4: ("문법 교정과 번역기능이 있는 챗봇 구축하기", step04.run),

}

def main():
    # 터미널 인자 읽기 (파일명 제외)
    args = sys.argv[1:]
    
    if not args:
        print("실행할 스텝 번호를 입력해주세요. (예: python main.py 1 3 10)")
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