import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel


class Domain(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    domain_string: str = Field(index=True)
    # shouldn't be List, change later
    dns_record: List['DNSRecord']


class DNSRecord(SQLModel, table=True):
    check_time: datetime.datetime
    a: str
    aaaa: str
    mx: str
    soa: str
    www: str
    ns: str
    txt: str
    ipv4: str
    ipv6: str
    asn: str
    xfr: str
    ptr: str
    registrar: str
    expiration_date: str
    srv: str
    email_exchange_service: str
    has_https: str
    is_blacklisted: str
