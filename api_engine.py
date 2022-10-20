from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.fetcher import get_records

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"message": "welcome to dnsengine"}


@app.get("/results/{domain_name}")
async def search_dns_record(domain_name: str):
    result = get_records(domain_string=domain_name)
    # FastAPI automatically returns Content-Type: Application/json
    return result
