"""
Asynchronous HTTP transport engine for RubiFlow using aiohttp.
"""

from typing import Any, Dict, Optional
import aiohttp

from .exceptions import NetworkError


class AsyncTransport:
    """Manages high-performance HTTP connections and connection pooling."""

    def __init__(self, timeout_seconds: float = 20.0):
        self.timeout_seconds = timeout_seconds
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        """Returns or creates the underlying aiohttp ClientSession."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=100,
                ttl_dns_cache=300,
                enable_cleanup_closed=True,
            )
            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={"Content-Type": "application/json; charset=utf-8"},
            )
        return self._session

    async def post_json(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Performs a POST request with JSON payload."""
        session = await self.get_session()
        try:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    text = await response.text()
                    raise NetworkError(f"HTTP {response.status}: {text}")
                return await response.json()
        except aiohttp.ClientError as exc:
            raise NetworkError(f"Network transport error connecting to {url}: {exc}") from exc

    async def close(self) -> None:
        """Closes the underlying aiohttp session and connector."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
