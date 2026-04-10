from langchain.tools import tool
from src.core import Query, logger
from settings import settings
import httpx
import json
import re
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Depends
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

class MoiveItem(BaseModel):
  imdbID: str = Field(description="영화의 고유 ID")
  Title: str = Field(description="영화 제목")
  Poster: str = Field(description="영화 포스터 URL")
  Year: str = Field(description="영화 개봉 연도")
  Type: str = Field(description="영화 유형")

class MovieListResponse(BaseModel):
  movies: list[MoiveItem] = Field(description="검색된 영화들의 리스트")
  count: int = Field(description="검색된 영화의 총 개수")
      
@tool
async def search_moive_info(query: str) -> str:
  """
    영화 제목(query)을 입력받아 검색된 영화들의 리스트를 JSON 형식의 문자열로 반환하는 도구입니다.
    반환 형식은 [{"imdbID": ..., "Title": ..., "Poster": ..., "Year": ..., "Type": ... }] 또는 {"error": "에러 메시지"} 형태입니다.
  """
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(
        settings.movie_api_url,
        params={"s": query, "apikey": settings.movie_api_key},
        timeout=10.0
      )
      response.raise_for_status()
      data = response.json()

      if data.get("Response") == "True":
        search_results = data.get("Search", [])
        formatted_data = [
          {
            "imdbID": movie.get("imdbID"),
            "Title": movie.get("Title"),
            "Poster": movie.get("Poster"),
            "Year": movie.get("Year"),
            "Type": movie.get("Type"),
          } for movie in search_results
        ]
        return json.dumps(formatted_data, ensure_ascii=False)
      else:
        return json.dumps({"error": f"'{query}'에 대한 영화 검색 결과가 없습니다."}, ensure_ascii=False)

    except httpx.HTTPStatusError as e:
      logger.error(f"API 요청 오류: {e.response.status_code}")
      return json.dumps({"error": "영화 서버 응답 오류가 발생했습니다."}, ensure_ascii=False)
    except Exception as e:
      logger.error(f"예상치 못한 오류: {str(e)}")
      return json.dumps({"error": "네트워크 연결이 원활하지 않습니다."}, ensure_ascii=False)

tools = [search_moive_info]

def extract_json(text: str) -> dict:
  match = re.search(r"(\{.*\})", text, re.DOTALL)
  if match:
    return json.loads(match.group(1))
  return json.loads(text)

def create_agent():
  try:
    llm = ChatOllama(
      model=settings.ollama_model_name,
      base_url=settings.ollama_base_url
    )
    schema = MoiveListResponse.model_json_schema()
    system_message = (
      f"당신은 영화 정보 전문가입니다. 반드시 search_moive_info 도구를 사용하여 영화 정보를 검색해야 합니다."
      f"응답은 반드시 다음 JSON schema를 따르는 순수한 JSON 객체여야 합니다: {schema} "
      f"설명이나 인사말 없이 JSON만 출력하세요."
    )
    return create_react_agent(llm, tools, prompt=system_message)
  except Exception as e:
    logger.error(f"에이전트 생성 중 오류: {str(e)}")
    return None

router = APIRouter(
  prefix="/step03",
  tags=["AI Agent와 외부 API 연동"],
)

@router.post("/chat")
async def chat(query: Query):
  try:
    agent = create_agent()
    if agent is None:
      raise HTTPException(status_code=500, detail="에이전트 생성에 실패했습니다.")
    inputs = {"messages": [("user", query.input)]}
    result = await agent.ainvoke(inputs)
    raw_content = result["messages"][-1].content
    json_data = extract_json(raw_content)
    validated_data = MovieListResponse(**json_data)
    return validated_data.model_dump()   
  except Exception as e:    
    logger.error(f"예상치 못한 오류: {str(e)}")
    raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다.")