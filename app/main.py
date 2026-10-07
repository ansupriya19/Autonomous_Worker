from fastapi import FastAPI
from pydantic import BaseModel
from .db import health
from .worker import run
app=FastAPI(title='Enterprise AI Task Worker',version='1.3')
class Req(BaseModel):task:str
@app.get('/health')
def h():return health()
@app.post('/task')
def task(r:Req):return run(r.task)
