from pprint import pprint
from typing import Optional

import requests


# https://rapidapi.com/collection/whois-api

def ip2_whois(domain: str) -> Optional[str]:
    # ip2 whois api
    # https://api.ip2whois.com/v2?key=587C732B90DBBA0CC68714C2C3993EA7&domain=example.com

    ip2_api_key = "587C732B90DBBA0CC68714C2C3993EA7"
    ip2_whois_url = "https://api.ip2whois.com/v2"
    query_string = {"key": {ip2_api_key}, "domain": {domain}}
    response = requests.get(ip2_whois_url, params=query_string)
    if response.status_code == 200:
        return response.json()


def whois_lookup(domain: str) -> Optional[str]:
    url = "https://zozor54-whois-lookup-v1.p.rapidapi.com/"

    querystring = {"domain": domain, "format": "json"}

    headers = {
        "X-RapidAPI-Key": "c4595d8af2msh0bbdbb706113fabp1ab0cfjsnb5b9e64dc3d3",
        "X-RapidAPI-Host": "zozor54-whois-lookup-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.text


#   ------------------ https://main.whoisxmlapi.com/ -------------------------------
def whois_api(domain) -> Optional[str]:
    whoisxml_api_key = "at_KmobLtt3Yaw4LMj4BeFriDsHr9foZ"
    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    query_string = {"apiKey": whoisxml_api_key, "domainName": domain, "outPutFormat": "JSON"}
    response = requests.get(url, params=query_string)

    if response.status_code == 200:
        return response.json()


def dns_lookup_api(domain) -> Optional[str]:
    whoisxml_api_key = "at_KmobLtt3Yaw4LMj4BeFriDsHr9foZ"
    url = "https://www.whoisxmlapi.com/whoisserver/DNSService?"
    query_string = {"apiKey": whoisxml_api_key, "domainName": domain, "outPutFormat": "JSON", "type": "_all"}
    response = requests.get(url, params=query_string)

    if response.status_code == 200:
        return response.text


def whois_reputation(domain) -> Optional[str]:
    whoisxml_api_key = "at_KmobLtt3Yaw4LMj4BeFriDsHr9foZ"
    url = "https://domain-reputation.whoisxmlapi.com/api/v2"
    query_string = {"apiKey": whoisxml_api_key, "domainName": domain, "outPutFormat": "JSON"}
    response = requests.get(url, params=query_string)

    if response.status_code == 200:
        return response.text


def main():
    domain = "freedom.net.tw"
    # pprint(ip2_whois(domain))
    # pprint(whois_lookup(domain))
    # pprint(dns_lookup_api(domain))
    pprint(whois_api(domain))
    # pprint(whois_reputation(domain))


if __name__ == "__main__":
    main()
