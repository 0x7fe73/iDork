import requests
from ..exceptions import *
from bs4 import BeautifulSoup
from typing import List, Optional, Union

# ./idork/search/google.py
# Author: 0x7fe73
# Date: 04/02/2022

class Google:
    def __init__(self, user_agent: Optional[str] = None, proxy_url: Optional[str] = None):
        self.proxy_url: Optional[str] = proxy_url
        self.url_list: List[str] = []
        self.headers: Dict[str, str] = {"user-agent": user_agent}

    def search(self, query: Optional[str]=None, lang: str="en", results: int=5) -> List[str]:
        if not query:
            raise MissingArgumentError("Missing Argument: \"query\"")
        
        params, proxies = dict(q=query, lang=lang, num=results), dict(http=self.proxy_url)
        resp = requests.get("https://www.google.com/search", params=params, proxies=proxies, headers=self.headers)
        self._parse_resp(resp.text)
        
        return self._url_list

    def _parse_resp(self, html: str) -> None:
        soup = BeautifulSoup(html, "html.parser")
        find = soup.find_all("div", attrs={"class": "g"})

        for se in find:
            link = se.find('a', href=True)
            title = se.find('h3')
            if link and title:self.url_list.append(link['href'])