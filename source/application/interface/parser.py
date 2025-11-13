# core/clients/base_api_client.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TypeVar, Generic
from curl_cffi import requests
from curl_cffi.requests import CurlHttpError
import logging
import time
from dobriy_bot.source.core.config.parser_dobro import Config as settings


T = TypeVar("T")


class BaseAPIClient(ABC, Generic[T]):
    """
    Абстрактный базовый клиент для API с retry, логированием и типизацией.
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._headers = headers or {}
        self._timeout = timeout or settings.request_timeout
        self._session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(self._headers)
        session.timeout = self._timeout
        return session

    @abstractmethod
    def _get_auth_headers(self) -> Dict[str, str]:
        pass

    def _request(
        self,
        method: str,
        endpoint: str,
        expected_status: int = 200,
        **kwargs,
    ) -> Dict[str, Any]:
        url = f"{self._base_url}{endpoint}"
        auth_headers = self._get_auth_headers()
        final_headers = {**self._headers, **auth_headers}
        kwargs.setdefault("headers", {})
        kwargs["headers"].update(final_headers)

        attempt = 0
        last_error = None

        while attempt < settings.max_retries:
            try:
                response = self._session.request(
                    method=method.upper(),
                    url=url,
                    timeout=self._timeout,
                    **kwargs,
                )

                # Явно проверяем 5xx для retry
                if response.status_code in (500, 502, 503, 504):
                    raise CurlHttpError(response=response)

                if response.status_code != expected_status:
                    response.raise_for_status()

                return response.json()

            except (requests.CurlError, CurlHttpError) as e:
                last_error = e
                status = getattr(e, "status_code", None)
                is_retryable = status is None or 500 <= status <= 504

                self._log_error(method, endpoint, e, attempt)

                if is_retryable and attempt < settings.max_retries - 1:
                    sleep_time = settings.backoff_factor * (2 ** attempt)
                    logging.info(f"Повтор через {sleep_time:.2f}с... ({attempt + 1}/{settings.max_retries})")
                    time.sleep(sleep_time)
                    attempt += 1
                    continue
                else:
                    return self._handle_final_failure(e)

            except Exception as e:
                last_error = e
                self._log_error(method, endpoint, e, attempt)
                return self._handle_final_failure(e)

        return self._handle_final_failure(last_error)

    def _log_error(self, method: str, endpoint: str, error: Exception, attempt: int):
        logging.error(
            f"API ошибка [{method} {endpoint}] попытка {attempt + 1}/{settings.max_retries}: {error}"
        )
        if hasattr(error, "response") and error.response:
            try:
                details = error.response.json()
                logging.error(f"Детали: {details}")
            except ValueError:
                logging.error("Тело ответа не JSON")

    def _handle_final_failure(self, error: Exception) -> Dict[str, Any]:
        logging.error(f"Исчерпаны попытки. Последняя ошибка: {error}")
        return {}

    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._request("POST", endpoint, expected_status=200, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._request("DELETE", endpoint, **kwargs)