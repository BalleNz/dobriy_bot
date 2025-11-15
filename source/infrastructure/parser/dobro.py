from typing import List, Optional, Dict
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse 
import logging
import json

import httpx
from uuid import UUID, uuid4 
import datetime

from source.application.interface.parser import BaseAPIClient
from source.core.enum.dobro_enum import CategoryType
from source.core.schemas.dobro_schemas import Advert

from datetime import datetime
import re # Для обработки timezone если нужно
def parse_date(rfc3339_str: str) -> Optional[datetime]:
    if not rfc3339_str:
        return None
    rfc3339_str = rfc3339_str.replace('Z', '+00:00')
    try:
        if '.' in rfc3339_str:
            return datetime.strptime(rfc3339_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            return datetime.strptime(rfc3339_str, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        return None


class DobroApiClient(BaseAPIClient):
    def __init__(self, base_url: str = "https://dobro.mail.ru"):
        super().__init__(
            base_url=base_url,
            headers={
                "Content-Type": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/142.0.0.0 Safari/537.36"
                ),
                "X-Requested-With": "XMLHttpRequest",
            },
        )

    def _get_auth_headers(self) -> Dict[str, str]:
        return {}

    async def get_adverts(
        self,
        category: Optional[CategoryType] = None,
        recipient: str = "kids",
        page_size: int = 50,
        max_pages: Optional[int] = None,
    ) -> List[Advert]:
        async with self:  # ← Фикс: используй with для создания/закрытия клиента
            all_adverts: List[Advert] = []
            page = 1
            while True:
                if max_pages and page > max_pages:
                    logging.info(f"Достигнут лимит страниц: {max_pages}")
                    break
                try:
                    response = await self._request(
                        method="GET",
                        endpoint="/api/projects/",
                        params={
                            "page": str(page),
                            "page_size": str(page_size),
                            "recipient": recipient.value.lower(),
                        },
                        expected_status=200,
                    )
                    print(recipient)
                    projects = response.get("object_list", [])
                    if not projects:
                        logging.info(f"Пустая страница {page}. Завершаем.")
                        break
                    new_uuid = uuid4()
                    adverts = [
                            Advert(
                                image=f'https://dobro.mail.ru{item.get("images", {}).get("web_project_list", {}).get("src", "")}',
                                id=item.get('slug'),  # Используем slug как уникальный ID
                                description=item.get('short_description'),
                                title=item.get('name'),
                                url=f'https://dobro.mail.ru/projects/{item.get("slug")}',
                                goal_amount=int(item.get("progress", {}).get("money_total", 0)),
                                money_collected=int(item.get("progress", {}).get("money_collected", 0)),
                                percent=int(item.get("progress", {}).get("percent", 0)),
                                money_left=int(item.get("progress", {}).get("money_left", 0)),
                                city_name=item.get("city", {}).get("name"),
                                fund_name=item.get("fund", {}).get("name"),
                                start_date=parse_date(item.get("start_date", {}).get("rfc3339")),
                                end_date=parse_date(item.get("end_date", {}).get("rfc3339")),
                                is_urgent=item.get("is_urgent", False),
                                lead=item.get('lead'),
                                meta_text=item.get('meta_text'),
                                has_report=item.get("has_report", False)
                            )
                    for item in projects
                    ]
                    
                    all_adverts.extend(adverts)
                    logging.info(f"Страница {page}: +{len(adverts)} объявлений")
                    page += 1
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        logging.info(f"404 на странице {page}. Сбор завершён.")
                        break
                    logging.error(f"HTTP {e.response.status_code if e.response else 'Unknown'} на странице {page}")
                    if e.response:
                        logging.error(f"Response text: {e.response.text}")
                    break
                except Exception as e:
                    logging.error(f"Ошибка парсинга на странице {page}: {e}, response={response}")
                    break
            logging.info(f"Сбор завершён. Всего: {len(all_adverts)} объявлений")
            return all_adverts

    async def generate_donation_link(self, advert: Advert) -> str:
        if not advert.url:
            base_url = f"https://dobro.mail.ru/project/{advert.id}"
        else:
            base_url = advert.url
        parsed = urlparse(base_url)
        query = parse_qs(parsed.query)
        query['action'] = ['help_money']
        new_query = urlencode(query, doseq=True)
        donation_link = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
        return donation_link