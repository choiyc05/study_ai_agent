from settings import settings
from src.save_image import save_graph_image
import logging
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool, create_swarm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = ChatOllama(
  model=settings.ollama_model_name,
  base_url=settings.ollama_base_url,
  streaming=True,
)

def search(query: str) -> dict:
  """
  Search the web for a query.
  Args:
    query: query string
  """
  logger.info(f"'{query}'에 대한 검색 작업 수행 중...")
  return {"results": f"검색 결과 for '{query}'"}

def find_emotion(situation: str, emotion: str) -> dict:
  """
  If the user makes emotional, Separate the problem situation from the user’s emotions.
  Args:
    situation: problem situation string
    emotion: user's emotion string
  """
  logger.info("감정과 상황을 분리하는 작업 수행 중...")
  return {"situation": situation, "emotion": emotion}

t_agent = create_react_agent(
  llm,
  [search, create_handoff_tool(agent_name="Fagent", description="사용자가 감정적이거나 자학적인 발언을 하는 경우, Fagent로 이관하십시오.")],
  prompt="당신은 MBTI에서 T 기능을 담당하는 에이전트입니다. 질문에 합리적이고 논리적으로 답변해야 합니다.",
  name="Tagent",
)

f_agent = create_react_agent(
  llm,
  [find_emotion, create_handoff_tool(agent_name="Tagent", description="사용자가 질문을 하거나 해결책을 필요로 하는 경우, Tagent로 연결하세요. Tagent가 합리적이고 논리적인 답변을 제공할 수 있습니다.")],
  prompt="당신은 MBTI에서 F 기능을 담당하는 에이전트입니다. 질문에 공감하고 감정적으로 답변해야 합니다.",
  name="Fagent",
)

def run():
  try:
    checkpointer = InMemorySaver()
    workflow = create_swarm(
        [t_agent, f_agent],
        default_active_agent="Fagent"
    )
    graph = workflow.compile(checkpointer=checkpointer)
    save_graph_image(graph)

    config = {"configurable": {"thread_id": "test_session_123"}}
    while True:
      try:
        user_input = input("🧑‍💻 User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
          logger.info("Goodbye!")
          break

        # turn = graph.invoke(
        #   {"messages": [{"role": "user", "content": user_input}]},
        #   config,
        # )
        # messages = turn['messages']
        # last_message = messages[-1]
        # logger.info(last_message.content)

        # stream_mode="updates"는 노드가 완료될 때마다 그 결과를 실시간으로 던져줍니다.
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
            stream_mode="messages",
        ):
            for node_name, output in event.items():
                # 에이전트가 답변을 생성했을 때만 출력
                if "messages" in output:
                    last_msg = output["messages"][-1]
                    
                    # 도구 호출(Tool Call) 메시지는 제외하고 실제 답변만 출력
                    if last_msg.content:
                        print(f"\n[🤖 {node_name}]: {last_msg.content}")
                        
                # 이관(Handoff)이 일어날 경우 알림 출력
                elif "active_agent" in output:
                    print(f"\n🔄 시스템: 에이전트가 {output['active_agent']}로 교체되었습니다.")

      except:
        break
  except Exception as e:
    logger.error(f"실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
  run()
