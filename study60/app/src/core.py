from settings import settings
import httpx
import json
import re
import logging
from pydantic import BaseModel, Field
from langchain.tools import tool
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Query(BaseModel):
  input: str

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

def get_app_state(request: Request):
  return request.app.state

@asynccontextmanager
async def lifespan(app: FastAPI):
  try:
    llm = ChatOllama(
      model=settings.ollama_model_name, 
      base_url=settings.ollama_base_url, 
      format="json",
      temperature=0
    )
    schema = MovieListResponse.model_json_schema()
    system_message = (
      f"당신은 영화 정보 전문가입니다. 반드시 search_movie_info 도구를 사용해 정보를 찾으세요. "
      f"응답은 반드시 다음 JSON 스키마를 따르는 순수한 JSON 객체여야 합니다: {schema}. "
      f"설명이나 인사말 없이 JSON만 출력하세요."
    )
    app.state.agent_executor = create_react_agent(llm, tools, prompt=system_message)
    
    logger.info("Agent Session Created Successfully!")
    yield
  except Exception as e:
    logger.error(f"초기화 중 오류 발생: {e}")
  finally:
    logger.info("Finalizing shutdown...")
