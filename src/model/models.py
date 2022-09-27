from typing import Optional, List, Dict, Union

from sqlmodel import Field, SQLModel

from src.utils.tools import DNSToolBox


class Domain(SQLModel, table=True):
    """
    Model class for a specific domain, related to the search records
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    domain_string: str


class DNSRecord(SQLModel, table=True):
    """
    Model class for one specific domain search
    """
    record_id: Optional[int] = Field(default=None, primary_key=True)
    search_used_time: str
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
    domain_id: Optional[int] = Field(default=None, foreign_key="domain.id")


def to_domain(domain: str) -> Optional[Domain]:
    domain = DNSToolBox.parse_raw_domain(domain)
    print(domain)
    if len(domain) <= 0:
        return
    try:
        record = Domain(domain_string=domain)
        print(record)
        return record
    except BaseException as error:
        print(f"{error=}")
        return


def to_DNS_record(domain_search_result: dict) -> Optional[DNSRecord]:
    if len(domain_search_result) != 21:
        return None
    try:
        record = DNSRecord(
            check_time=domain_search_result["check_time"],
            search_used_time=domain_search_result["search_used_time"],
            a=domain_search_result["a"],
            aaaa=domain_search_result["aaaa"],
            mx=domain_search_result["mx"],
            soa=domain_search_result["soa"],
            www=domain_search_result["www"],
            ns=domain_search_result["ns"],
            txt=domain_search_result["txt"],
            ipv4=domain_search_result["ipv4"],
            ipv6=domain_search_result["ipv6"],
            asn=domain_search_result["asn"],
            xfr=domain_search_result["xfr"],
            ptr=domain_search_result["ptr"],
            registrar=domain_search_result["registrar"],
            expiration_date=domain_search_result["expiration_date"],
            srv=domain_search_result["srv"],
            email_exchange_service=domain_search_result["email_exchange_service"],
            o365=domain_search_result["o365"],
            has_https=domain_search_result["has_https"],
            is_blacklisted=domain_search_result["is_blacklisted"]
        )

        return record
    except BaseException as error:
        print(f"{error=}")
        return
