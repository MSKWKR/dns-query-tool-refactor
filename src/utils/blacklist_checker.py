import base64
import configparser
import json

import pydnsbl
import requests

from src.utils.log.log import exception, LOGGER


class BlackListChecker:
    """
    BlackListChecker is a tool checking whether the given url is being blacklisted
    """

    def __init__(self):
        self._domain_checker = pydnsbl.DNSBLDomainChecker()

        self.config = configparser.ConfigParser()
        # we don't have to close the opened .ini file, configparser took care of that
        self.config.read('../apikeys.ini')

    # Python Domain Name System Blacklists
    @exception(LOGGER)
    def search_dnsbl(self, url: str) -> any:
        """
        Util checking pydnsbl

        :param url: A url or a domain string
        :type: str

        :return: The result for search pydnsbl
        :rtype: any
        """
        dnsbl_result = self._domain_checker.check(url)
        return dnsbl_result

    @exception(LOGGER)
    def search_virus_total(self, url: str) -> json:
        """
        Util to get a URL analysis report from virustotal

        :param url: A url or a domain string to check
        :type: str

        :return: The json format of the API call result
        :rtype: json
        """
        # url_id is the URL identifier or base64 representation of URL to scan (w/o padding)
        url_id = base64.urlsafe_b64encode(f"{url}".encode()).decode().strip("=")
        virus_total_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        virus_total_key = self.config['API Keys']['virustotal_api_key']

        headers = {
            "Accept": "application/json",
            'x-apikey': virus_total_key
        }
        response = requests.get(
            virus_total_url,
            headers=headers
        )

        return response.json()

    @exception(LOGGER)
    def is_black_listed_pydnsbl(self, url: str) -> bool:
        """
        Checks the result of search_dnsbl()

        :param url: A url or a domain string to check
        :type: str

        :return: The result of pydnsbl, True if blacklisted
        :rtype: bool
        """
        pydnsbl_result = self.search_dnsbl(url)
        return pydnsbl_result.blacklisted

    # ---------------------------- Virus Total Result -------------------------------------
    @exception(LOGGER)
    def site_status_virus_total(self, url) -> any:
        """
        Util function checking Virus Total in order to get whether the given is black listed,
        returns two dictionaries, the first being all provider status and the second being the blacklisted provider

        :param url: A url or a domain string to check
        :type: str

        :return: The result after checking with Virus Total
        :rtype: tuple(dict, dict)
        """
        site_statuses = {}
        black_listed_provider = {}
        try:
            virus_total_result = self.search_virus_total(url)
            for provider in virus_total_result["data"]["attributes"]["last_analysis_results"]:
                site_result = virus_total_result["data"]["attributes"]["last_analysis_results"][provider]
                site_status = site_result["result"]
                # All providers status
                site_statuses[provider] = site_status
                # Black Listed providers
                if site_status not in ("clean", "unrated"):
                    black_listed_provider[provider] = site_status
        except KeyError as error:
            LOGGER.exception(msg=f"Virus total key error: {error}")
            # print(f"{error=}")

        return site_statuses, black_listed_provider

    @exception(LOGGER)
    def is_black_listed_virus_total(self, url) -> bool:
        """
        Util function checking Virus Total in order to get whether the given is black listed
        :param url: A url or a domain string to check
        :type: str

        :return: The result after checking with Virus Total, True if blacklisted
        :rtype: bool
        """
        black_listed_provider = self.site_status_virus_total(url)[1]
        # print(black_listed_provider)
        return len(black_listed_provider) != 0

    def is_black_listed(self, url: str) -> bool:
        """
        For the time being, checks pydnsbl and virus total whether the given site is blacklisted
        :param url: A url or a domain string to check
        :type: str

        :return: True if blacklisted by any security provider
        :rtype: bool
        """
        return self.is_black_listed_virus_total(url) or self.is_black_listed_pydnsbl(url)
