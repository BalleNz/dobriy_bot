import logging
import time
from typing import Dict, Any
from curl_cffi import requests
from curl_cffi.requests import CurlHttpError

from dobriy_bot.source.core.config.parser_dobro import Config
from dobriy_bot.source.application.interface.parser import BaseAPIClient
 


class DobroApiClient(BaseAPIClient):
    def _get_auth_headers():

        return {
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://dobro.mail.ru/projects/?recipient=kids',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'accept': 'application/json',
            'baggage': 'sentry-environment=production,sentry-release=Ja9r848idT4145Mz9FK0j,sentry-public_key=45d2de925f9945be9bc7f68c1b6bcd03,sentry-trace_id=9f347c78b71f4421b70aa1ddbde89478',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sentry-trace': '9f347c78b71f4421b70aa1ddbde89478-bb2075c150120a91-0',
        }
    

    def get_adv(category: str):
        ...


    def get_url(amount: str, adv_id: str) -> str:
        ...