from typing import Optional, List

from sqlmodel import Field, SQLModel


class Domain(SQLModel):
    """
    Model class for a specific domain
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    domain_string: str = Field(index=True)


class DNSRecord(SQLModel):
    """
    Model class for a specific domain search
    """
    check_time: str
    a: str
    aaaa: str
    mx: str
    soa: str
    www: str
    ns: List[str]
    txt: List[str]
    ipv4: List[str]
    ipv6: List[str]
    asn: dict[str:List[str]]
    xfr: List[str]
    ptr: str
    registrar: str
    expiration_date: str
    srv: dict[str: List[str]]
    email_exchange_service: str
    o365: dict[str: List[str]]
    has_https: bool
    is_blacklisted: bool
    domain_id: Optional[int] = Field(default=None, foreign_key="Domain.id")
