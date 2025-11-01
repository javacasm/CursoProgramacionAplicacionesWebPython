from fastapi import FastAPI
from celery import Celery
import redis
import logging

app = FastAPI()
celery = Celery('tasks', broker='redis://redis:6379/0')
r = redis.Redis(host='redis', port=6379, db=0)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def compute_sum(numbers):
    return sum(numbers)

@app.get("/health")
async def health():
    try:
        r.ping()
        return {"status": "healthy"}
    except:
        logger.error("Redis unavailable")
        return {"status": "unhealthy"}, 500

@app.post("/compute")
async def compute(numbers: list[int]):
    task = compute_sum.delay(numbers)
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task = compute_sum.AsyncResult(task_id)
    if task.ready():
        return {"result": task.get()}
    return {"status": "pending"}