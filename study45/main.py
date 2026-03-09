import mariadb
from settings import settings

conn_params = {
  "user" : settings.mariadb_user,
  "password" : settings.mariadb_password,
  "host" : settings.mariadb_host,
  "database" : settings.mariadb_database,
  "port" : settings.mariadb_port
}

def etl():
    print("db_air 에서 db_to_air 데이터 이관 작업")
    result = False
    try:
        # db 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                sql=f"""
                insert into db_to_air.`비행`
                select * from db_air.`비행` where `월`=10;
                """
                cur.execute(sql)
                conn.commit()
                print(f"이관 완료! : {cur.rowcount}행 처리됨")
                result = True
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")
    return result

def etl2(year: int, month: int):
    print("이관 작업 시작")
    result = False
    try:
        # db 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                # DB 비우기
                # cur.execute("TRUNCATE TABLE `db_to_air`.`비행`")
                sql = f"""
                    DELETE FROM db_to_air.`비행` 
                    WHERE `년도`={year} AND `월`={month};
                    """
                cur.execute(sql)
                
                # 데이터 이관 
                sql = f"""
                    INSERT INTO db_to_air.`비행`
                    SELECT * FROM db_air.`비행` 
                    WHERE `년도`={year} AND `월`={month};
                    """
                cur.execute(sql)

                # DB에 들어간 행 수 조회
                sql = f"""
                    SELECT count(*) cnt FROM db_to_air.`비행`
                    WHERE `년도`={year} AND `월`={month};
                    """
                cur.execute(sql)
                data = cur.fetchone()

                conn.commit()
                result = True
                print(f"이관 완료! 이동된 행수 : {data[0]}행")
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")
    return result

def etl3(year: int, month: int):
    print("이관 작업 시작")
    result = False
    try:
        # db 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                where = f"WHERE `년도` = {year} AND `월` = {month}"
                sql1 = f"""DELETE FROM db_to_air.`비행` 
                        {where};
                        """
                sql2 = f"""INSERT INTO db_to_air.`비행`
                        SELECT * FROM db_air.`비행`
                        {where};
                        """
                sql3 = f"""
                        SELECT count(*) cnt 
                        FROM db_to_air.`비행` 
                        {where};
                        """
                # DB 비우기, INSERT, SELECT
                cur.execute(sql1)
                cur.execute(sql2)
                cur.execute(sql3)
                data = cur.fetchone()

                conn.commit()
                result = True
                print(f"이관 완료 : 이관된 행수 : {data[0]}")
    except mariadb.Error as e:
        print(f"MariaDB Error : {e} 행")
    return result

def etl4(table: str):
    print(f"{table} 테이블 이관 시작!")
    result = False
    try:
        # db 연결 시작
        with mariadb.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                where = f"FROM db_air.`{table}`"
                sql1 = f"TRUNCATE TABLE db_to_air.`{table}`;"
                sql2 = f"INSERT INTO db_to_air.`{table}` SELECT * {where};"
                sql3 = f"SELECT COUNT(*) AS CNT {where};"
                # DB 비우기, INSERT, SELECT
                cur.execute(sql1)
                cur.execute(sql2)
                conn.commit()

                cur.execute(sql3)
                data = cur.fetchone()

                result = True
                print(f"{table} 이관된 행수 : {data[0]}")
    except mariadb.Error as e:
        print(f"MariaDB Error : {e} 행")
    return result

def etl5(table: str, year: int = 0, month: int = 0):
    print("db_air => db_to_air 데이터 이관 작업 시작")
    result = False
    where = ""
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
                result = True
                print(f"{table} 적재 : {row[0]} 행 완료!")
    except mariadb.Error as e:
        print(f"MariaDB Error : {e} 행")
    return result

def etl6(data: dict):
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

if __name__ == "__main__":
    useYn = tuple([0])
    for row in jobs(useYn):
        if row:
            print(row)
            etl6(row)
            # etl5(row["table"], row["year"], row["month"])
    # etl()
    # etl2(1987, 11)
    # etl3(1987, 12)
    # etl5("비행", 1987, 10)
    # etl5("운반대")
    # etl5("항공사")


