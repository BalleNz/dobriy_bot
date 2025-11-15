from typing import List, Optional, Dict
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse 
import logging
import json

import httpx
from uuid import UUID, uuid4 

from source.application.interface.parser import BaseAPIClient
from source.core.enum.dobro_enum import CategoryType
from source.core.schemas.dobro_schemas import Advert



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
                    adverts = [Advert(
                        image=f'https://dobro.mail.ru{item.get("images").get("web_project_list").get("src", "")}',
                        id=new_uuid,
                        description=item.get('short_description'),
                        title=item.get('name'),
                        url=f'https://dobro.mail.ru/projects/{item.get("slug")}',
                        goal_amount=int(item.get("progress", {}).get("money_total", 0))
                    )
                    for item in projects]
                    
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