import os
from typing import Any

import httpx
from dotenv import load_dotenv
from httpx import Response, Timeout

from constants import (
    MAX_ATTEMPTS,
    DEFAULT_TIMEOUT,
    READ_TIMEOUT,
)
from enums import HTTPMethods
from exceptions import ServiceError, ClientError
from utils import retry

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")


class BaseClient:

    def __init__(self, base_url: str, headers: dict[str, Any] | None = None) -> None:
        self._base_url = base_url
        self._headers = headers or {}

    def update_headers(self, data: dict[str, Any]) -> None:
        if isinstance(self._headers, dict):
            self._headers |= data
        else:
            self._headers = data

    @retry(
        max_attempts=MAX_ATTEMPTS,
        wait_seconds=10.0,
        retry_on=(ServiceError,),
        return_none_on_failure=True,
    )
    def _make_request(
        self,
        method: HTTPMethods,
        url: str,
        **kwargs: Any,
    ) -> Response:

        with httpx.Client(
            base_url=self._base_url,
            headers=self._headers,
            timeout=Timeout(DEFAULT_TIMEOUT, read=READ_TIMEOUT),
        ) as client:
            response = client.request(
                method=method,
                url=url,
                **kwargs,
            )

            if response.status_code >= 300:
                if response.status_code == 429 or response.status_code >= 500:
                    raise ServiceError(
                        status_code=response.status_code,
                        detail=response.text,
                    )
                raise ClientError(
                    status_code=response.status_code,
                    detail=response.text,
                )

            return response

    def _get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        return self._make_request(
            method=HTTPMethods.GET,
            url=url,
            params=params,
            **kwargs,
        )


class CoinGeckoClient(BaseClient):

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key: str | None = None) -> None:
        headers = {}
        if api_key:
            headers["x-cg-demo-api-key"] = api_key

        super().__init__(base_url=self.BASE_URL, headers=headers)

    def get_coins_list(
        self,
        vs_currency: str = "usd",
        order: str = "volume_desc",
        per_page: int = 100,
        page: int = 1,
        **kwargs: Any,
    ) -> Response:
        params = {
            "vs_currency": vs_currency,
            "order": order,
            "per_page": per_page,
            "page": page,
            **kwargs,
        }

        return self._get("/coins/markets", params=params)

    def get_coin_info(
        self,
        coin_id: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        return self._get(f"/coins/{coin_id}", params=params, **kwargs)

    def get_coin_tickers_info(
        self,
        coin_id: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        return self._get(f"/coins/{coin_id}/tickers", params=params, **kwargs)


cg_client = CoinGeckoClient(api_key=COINGECKO_API_KEY)
