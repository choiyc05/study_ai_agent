import mariadb
from settings import settings
from fastapi.responses import RedirectResponse

conn_params = {
  "user" : settings.mariadb_user,
  "password" : settings.mariadb_password,
  "host" : settings.mariadb_host,
  "database" : settings.mariadb_database,
  "port" : settings.mariadb_port
}

def getList():
    try:
        # DB 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM db_to_air.`jobs`"
                cur.execute(sql)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result
    except mariadb.Error as e:
        print(f"MariaDB Error : {e} 행")
    return []

def jobSet(type: bool = False, jobNo: list[int] = []):
    try:
        # DB 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:         
                if isinstance(jobNo, (list, tuple)):
                    keys = ",".join(map(str, jobNo)) 
                else:
                    keys = jobNo     
                sql = f"""
                    UPDATE db_to_air.jobs 
                    SET `useYn` = {type}
                    WHERE `no` IN ({keys});
                    """
                cur.execute(sql)
                conn.commit()
                return {"status": True}
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")
        return {"status": False, "error": e}

def etl(data: dict):
    print("db_air => db_to_air 데이터 이관 작업 시작")
    result = False
    where = ""
    year = data["year"]
    month = data["month"]
    table = data["table"]
    no = data["no"]
    try:
        # DB 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                if year > 0 and month > 0:
                    where = f"WHERE `년도` = {year} AND `월` = {month}"
                sql1 = f"DELETE FROM db_to_air.`{table}` {where};"
                sql2 = f"INSERT INTO db_to_air.`{table}` SELECT * FROM db_air.`{table}` {where};"
                sql3 = f"SELECT COUNT(*) AS CNT FROM db_to_air.`{table}` {where};"
                # SQL 실행
                print("SQL 실행")
                cur.execute(sql1)
                cur.execute(sql2)
                conn.commit()
                # 작업된 행수 
                cur.execute(sql3)
                row = cur.fetchone()
                print(f"{table} 적재 : {row[0]} 행 완료!")
                # jobs 테이블에 로그 남기기
                sql4 = f"UPDATE db_to_air.`jobs` SET `cnt`={row[0]}, `modDate` = now() WHERE `no` = {no}"
                cur.execute(sql4)
                conn.commit()
                result = True
    except mariadb.Error as e:
        print(f"MariaDB Error : {e} 행")
    return result

def jobs(useYn: tuple):
    try:
        # DB 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:         
                if isinstance(useYn, (list, tuple)):
                    keys = ",".join(map(str, useYn))      
                sql = f"""
                    SELECT `no`, `table`, `year`, `month` 
                    FROM db_to_air.jobs 
                    WHERE useYn IN ({keys});
                    """
                cur.execute(sql)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result
    except mariadb.Error as e:
        print(f"MariaDB Error : {e} 행")
    return []


