from typing import Optional

from sqlmodel import Field, SQLModel

from src.utils.log.log import exception, LOGGER
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
    #  After serializing, all data are bytes
    record_id: Optional[int] = Field(default=None, primary_key=True)
    domain_name: str
    search_used_time: str
    check_time: str
    a: bytes  # str
    aaaa: bytes  # str
    mx: bytes  # str
    soa: bytes  # str
    www: bytes  # str
    ns: bytes  # List[str]
    txt: bytes  # List[str]
    ipv4: bytes  # List[str]
    ipv6: bytes  # List[str]
    asn: bytes  # Dict[str, Union[str]]
    xfr: bytes  # List[str]
    ptr: bytes  # str
    registrar: bytes  # str
    expiration_date: bytes  # str
    srv: bytes  # dict[str, Union[str]]
    email_exchange_service: bytes  # str
    o365: bytes  # dict[str, Union[str]]
    has_https: bytes  # bool
    is_blacklisted: bytes  # bool
    domain_id: Optional[int] = Field(default=None, foreign_key="domain.id")


@exception(LOGGER)
def to_domain(domain: str) -> Optional[Domain]:
    """
    The helper function for turning the domain string into a Domain class

    :param domain: The checked domain string
    :type: str

    :return: The Domain class or None if something unexpected happen
    :rtype: Optional[Domain]
    """
    domain = DNSToolBox.parse_raw_domain(domain)
    if len(domain) <= 0:
        return
    try:
        record = Domain(domain_string=domain)
        return record
    except BaseException as error:
        LOGGER.exception(msg=f"Domain string transform error: {error}")
        # print(f"{error=}")
        return


@exception(LOGGER)
def to_DNS_record(domain_search_result: dict) -> Optional[DNSRecord]:
    """
    The helper function for turning the domain string into a Domain class

    :param domain_search_result: The result for the DNS search
    :type: dict

    :return: The DNSRecord class or None if something unexpected happen
    :rtype: Optional[Domain]
    """

    if len(domain_search_result) != 22:
        return None
    try:
        record = DNSRecord(
            domain_name=domain_search_result["domain_name"],
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
        LOGGER.exception(msg=f"Domain Record transform error: {error}")
        # print(f"{error=}")
        return
