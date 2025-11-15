from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
import asyncio
import httpx
from source.core.config.dobro_config import ParserConfig as get_settings

settings = get_settings()

class BaseAPIClient(ABC):
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._headers = headers or {}
        self._timeout = timeout or settings.REQUEST_TIMEOUT
        self._client: Optional[httpx.AsyncClient] = None  

    async def __aenter__(self):
        await self._ensure_client() 
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._client:
            await self._client.aclose()
            self._client = None  

    async def _ensure_client(self):
        """Создаёт _client, если None (для вызова без with)"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers=self._headers,
                timeout=self._timeout,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            )
            logging.info("Created httpx.AsyncClient")

    @abstractmethod
    def _get_auth_headers(self) -> Dict[str, str]:
        pass

    async def _request(
        self,
        method: str,
        endpoint: str,
        expected_status: int = 200,
        **kwargs,
    ) -> Dict[str, Any]:
        await self._ensure_client() 
        url = f"{self._base_url}{endpoint}"
        headers = {**self._headers, **self._get_auth_headers()}
        kwargs.setdefault("headers", {})
        kwargs["headers"].update(headers)
        attempt = 0
        while attempt < settings.MAX_RETRIES:
            try:
                response = await self._client.request(method.upper(), url, **kwargs)
                if response.status_code in (500, 502, 503, 504):
                    raise httpx.HTTPStatusError(
                        message="Server error", request=response.request, response=response
                    )
                if response.status_code != expected_status:
                    response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise
                if e.response and e.response.status_code >= 500: 
                    attempt += 1
                    if attempt < settings.MAX_RETRIES:
                        await asyncio.sleep(settings.BACKOFF_FACTOR * (2 ** (attempt - 1))) 
                        continue
                logging.error(f"HTTP {e.response.status_code if e.response else 'Unknown'} на {method} {endpoint}")
                if e.response: 
                    logging.error(f"Response text: {e.response.text}")
                return {}
            except Exception as e:
                logging.error(f"Ошибка запроса: {e}")
                return {}
        return {}