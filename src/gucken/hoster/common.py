from abc import abstractmethod
from dataclasses import dataclass

from httpx import AsyncClient, HTTPError


@dataclass
class DirectLink:
    url: str
    headers: dict[str, str] = None

    async def check_is_working(self) -> bool:
        try:
            async with AsyncClient(verify=False) as client:
                response = await client.head(self.url, follow_redirects=True, headers=self.headers)
                return response.is_success
        except HTTPError:
            return False

    def __str__(self):
        return self.url

    def has_headers(self) -> bool:
        if self.headers is not None:
            return True
        return False


@dataclass
class Hoster:
    url: str
    requires_headers: bool = False

    @abstractmethod
    async def get_direct_link(self) -> DirectLink:
        raise NotImplementedError
