from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  mariadb_user: str = "root"
  mariadb_password: str = "1234"
  mariadb_host: str = "192.168.0.204"
  # app3_2는 localhost로 했음
  mariadb_database: str = "edu"
  # app3_2는 test로 했음
  mariadb_port: int = "3306"
  save_melon_50_sql : str = """
        INSERT INTO melonCrawl (id, title, album, img, cnt)
        VALUES ("{id}", "{title}", "{album}", "{img}", "{cnt}" )
        """

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
  )

settings = Settings()
