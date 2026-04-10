from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  ollama_base_url: str = "http://localhost:11434"
  ollama_model_name: str = "gemma4:e4b"
  graph_image_path: str = "images"
  movie_api_url: str = "https://www.omdbapi.com/"
  movie_api_key: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )

settings = Settings()