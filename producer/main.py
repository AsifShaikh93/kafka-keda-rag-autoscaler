from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import os

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP","kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "rag-requests"

class QueryRequest(BaseModel):
    user_input: str
    session_id: str


@app.post("/query")
async def query(req: QueryRequest):

    producer.send(TOPIC, req.dict())

    return {
        "status": "queued",
        "message": "request sent to processing queue"
    }