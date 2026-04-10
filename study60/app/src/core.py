from typing import Optional
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
import aiomysql  # 비동기 MySQL 드라이버

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
  Plot: Optional[str] = Field(description="영화 줄거리", default=None)

class MovieListResponse(BaseModel):
  movies: list[MoiveItem] = Field(description="검색된 영화들의 리스트")
  count: int = Field(description="검색된 영화의 총 개수")
      
async def get_db_conn():
    return await aiomysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        db='edu',
        autocommit=True
    )

@tool
async def search_moive_info(query: str) -> str:
  """
    영화 제목(query)을 입력받아 검색된 영화들의 리스트를 JSON 형식의 문자열로 반환하는 도구입니다.
    반환 형식은 [{"imdbID": ..., "title": ..., "poster": ..., "year": ..., "type": ... }] 또는 {"error": "에러 메시지"} 형태입니다.
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
            "title": movie.get("Title"),
            "poster": movie.get("Poster"),
            "year": movie.get("Year"),
            "type": movie.get("Type"),
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

@tool
async def movie_info(query: str) -> str:
  """
    영화 ID(imdbID)를 입력받아 검색된 영화의 상세 정보를 JSON 형식의 문자열로 반환하는 도구입니다.
    반환 형식은 [{"imdbID": ..., "title": ..., "poster": ..., "year": ..., "type": ..., "plot": ... }] 형태입니다.
  """
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(
        settings.movie_api_url,
        params={"i": query, "plot": "full", "apikey": settings.movie_api_key},
        timeout=10.0
      )
      response.raise_for_status()
      data = response.json()

      if data.get("Response") == "True":
        formatted_data = [
          {
            "imdbID": data.get("imdbID"),
            "title": data.get("Title"),
            "poster": data.get("Poster"),
            "year": data.get("Year"),
            "type": data.get("Type"),
            "plot": data.get("Plot"),
          }
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

@tool
async def save_db_movie_info(movie_data: dict) -> str:
  """
  이 도구는 영화 상세 정보를 데이터베이스에 저장합니다.
  입력값은 반드시 movie_info 도구에서 받은 딕셔너리 객체여야 합니다.
  """
  try:
    # AI가 문자열로 줬을 경우를 대비한 안전 장치
    if isinstance(movie_data, str):
      movie = json.loads(movie_data)
    else:
      movie = movie_data
    
    # 리스트일 경우 첫 번째 요소 추출
    if isinstance(movie, list):
      movie = movie[0]

    async with await get_db_conn() as conn:
      async with conn.cursor() as cur:
          sql = """
              INSERT INTO movie (imdbID, title, poster, year, type, plot)
              VALUES (%s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE
                  title = VALUES(title),
                  poster = VALUES(poster),
                  year = VALUES(year),
                  type = VALUES(type),
                  plot = VALUES(plot);
          """
          params = (
              movie.get('imdbID'),
              movie.get('title'),
              movie.get('poster'),
              movie.get('year'),
              movie.get('type'),
              movie.get('plot')
          )
          await cur.execute(sql, params)

    
    return json.dumps({"success": True, "message": f"{movie.get('title')} 저장/업데이트 완료"}, ensure_ascii=False)
  except Exception as e:
        logger.error(f"DB 저장 중 오류: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

tools = [search_moive_info, movie_info, save_db_movie_info]

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
      f"당신은 영화 정보 전문가입니다. 반드시 search_movie_info, movie_info 중 하나를 사용해 정보를 찾으세요. "
      f"영화 검색 시에는 search_movie_info 도구를 사용하여 영화 제목으로 검색하고, 영화의 상세 정보가 필요할 때는 movie_info 도구를 사용하여 imdbID로 검색해야 합니다."
      f"'movie_info' 호출 직후, 반드시 해당 데이터를 'save_db_movie_info'에 전달하여 저장하세요."
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
