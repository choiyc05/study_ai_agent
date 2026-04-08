# from src import step01, step02, step03, step04, step05, step06, step07, step08, step09, step10, step11, step12, step13, step14
# import asyncio

# stream_modes = [
#   "updates", # 각 상태 업데이트 시점마다 전체 상태를 반환
#   "values", # 각 상태 업데이트 시점마다 변경된 필드와 값만 반환
#   "messages", # 각 상태 업데이트 시점마다 메시지 필드의 변경된 메시지만 반환
# ]

# def main():
#   print("Hello from app!")
#   # print("Step 1 실행: TypedDict 사용")
#   # step01.run()
#   # print("Step 2 실행: Pydantic 사용")
#   # step02.run()
#   # print("Step 3 실행: LangGraph 사용하여 그래프 이미지 저장")
#   # step03.run()
#   # print("Step 4 실행: 간단한 챗봇 노드(Node) 만들기")
#   # step04.run()
#   # print("Step 5 실행: 조건부 엣지 사용")
#   # step05.run()
#   # print("Step 6 실행: 대화메시지 상태 업데이트")
#   # step06.run()
#   # print("Step 7 실행: 대화메시지 상태 누적 업데이트")
#   # step07.run()
#   # print("Step 8 실행: 비동기 대화메시지 상태 누적 업데이트")
#   # asyncio.run(step08.run())
#   # print("Step 9 실행: 스트리밍 모드로 대화메시지 상태 누적 업데이트")
#   # step09.run(stream_modes[0])
#   # step09.run(stream_modes[1])
#   # step09.run(stream_modes[2])
#   # print("Step 10 실행: 노드와 엣지 연결하기")
#   # step10.run()
#   # print("Step 11 실행: 한번에 노드 연결하기")
#   # step11.run()
#   # print("Step 12 실행: 병렬 그래프 사용")
#   # step12.run()
#   # print("Step 13 실행: Fan-in과 Fan-out 패턴 구현하기")
#   # step13.run()
#   # print("Step 14 실행: 조건에 따른 반복 처리 구현하기")
#   # step14.run()

# if __name__ == "__main__":
#   main()


## 
import sys
import asyncio
from src import (
    step01, step02, step03, step04, step05, step06, step07, 
    step08, step09, step10, step11, step12, step13, step14
)

# 스텝 번호와 실행 함수를 매핑합니다. 
# step08처럼 asyncio.run이 필요한 경우 람다(lambda)로 감싸서 통일감을 줍니다.
step_map = {
    1: ("TypedDict 사용", step01.run),
    2: ("Pydantic 사용", step02.run),
    3: ("LangGraph 그래프 이미지 저장", step03.run),
    4: ("간단한 챗봇 노드 만들기", step04.run),
    5: ("조건부 엣지 사용", step05.run),
    6: ("대화메시지 상태 업데이트", step06.run),
    7: ("대화메시지 상태 누적 업데이트", step07.run),
    8: ("비동기 대화메시지 상태 누적 업데이트", lambda: asyncio.run(step08.run())),
    9: ("스트리밍 (모든 모드)", lambda: [step09.run(m) for m in ["updates", "values", "messages"]]),
    9.1: ("스트리밍 (updates)", lambda: step09.run("updates")),
    9.2: ("스트리밍 (values)", lambda: step09.run("values")),
    9.3: ("스트리밍 (messages)", lambda: step09.run("messages")),
    10: ("노드와 엣지 연결하기", step10.run),
    11: ("한번에 노드 연결하기", step11.run),
    12: ("병렬 그래프 사용", step12.run),
    13: ("Fan-in과 Fan-out 패턴 구현", step13.run),
    14: ("조건에 따른 반복 처리 구현", step14.run),
}

def main():
    # 터미널 인자 읽기 (파일명 제외)
    args = sys.argv[1:]
    
    if not args:
        print("실행할 스텝 번호를 입력해주세요. (예: python main.py 1 3 10)")
        return

    for arg in args:
        try:
            step_num = float(arg) if "." in arg else int(arg)
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