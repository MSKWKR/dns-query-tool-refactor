from typing import Optional, List, Dict, Union

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
    record_id: Optional[int] = Field(default=None, primary_key=True)
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
    asn: Dict[str, Union[str]]
    xfr: List[str]
    ptr: str
    registrar: str
    expiration_date: str
    srv: dict[str, Union[str]]
    email_exchange_service: str
    o365: dict[str, Union[str]]
    has_https: bool
    is_blacklisted: bool
    domain_id: Optional[int] = Field(default=None, foreign_key="Domain.id")
