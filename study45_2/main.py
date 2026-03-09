from fastapi import FastAPI
from etlTest import etl, jobs, getList, jobSet

app = FastAPI(title="ETL TEST")

@app.get("/")
def read_root():
  return {"ETL": "test"}

@app.get("/getlist")
def joblist():
  data = getList()
  if data:
    return {"status": True, "list": data}
  return {"status": False}

@app.post("/set")
def setJob(type: bool = False, jobNo: list[int] = []):
  result = jobSet(type, jobNo)
  if result["status"]:
    updated_data = getList()
    return {"status": True, "list": updated_data}
  return result
  
@app.get("/run")
def etlrun():
  useYn = tuple([1])
  for row in jobs(useYn):
    if row:
      etl(row)
  return {"status": True}
