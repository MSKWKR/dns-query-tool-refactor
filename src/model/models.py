from typing import Optional, List

from sqlmodel import Field, SQLModel


class Domain(SQLModel, table=True):
    """
    Model class for a specific domain, related to the search records
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    domain_string: str = Field(index=True)


class DNSRecord(SQLModel, table=True):
    """
    Model class for one specific domain search
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
