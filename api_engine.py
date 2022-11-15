from typing import Optional

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
def home():
    return {"message": "welcome to dnsengine"}


@app.get("/results/{domain_name}")
def search_dns_record(domain_name: str, srv: Optional[str] = None):
    if srv == 'srv':
        result = get_records(domain_string=domain_name, want_srv=True)
    else:
        result = get_records(domain_string=domain_name)
    # FastAPI automatically returns Content-Type: Application/json
    return result
