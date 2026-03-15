import json
import os
from kafka import KafkaConsumer
from langchain_groq import ChatGroq

consumer = KafkaConsumer(
    "rag-requests",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP","kafka:9092"),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="rag-workers",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

print("Worker started")

for message in consumer:

    data = message.value
    question = data["user_input"]

    response = llm.invoke(question)

    print("Answer:", response.content)