import logging
from playwright.sync_api import Page, Response

logger = logging.getLogger(__name__)


class APIHelper:
    """Helper class to intercept and validate browser API calls."""

    def __init__(self, page: Page):
        self.page = page
        self.captured_requests = []
        self.captured_responses = []
        self._setup_listeners()

    def _setup_listeners(self):
        self.page.on("request", self._on_request)
        self.page.on("response", self._on_response)

    def _on_request(self, request):
        if self._is_api_call(request.url):
            logger.debug(f"API Request: {request.method} {request.url}")
            self.captured_requests.append({
                "url": request.url,
                "method": request.method,
                "headers": dict(request.headers),
            })

    def _on_response(self, response: Response):
        if self._is_api_call(response.url):
            logger.debug(f"API Response: {response.status} {response.url}")
            self.captured_responses.append({
                "url": response.url,
                "status": response.status,
                "method": response.request.method,
            })

    def _is_api_call(self, url: str) -> bool:
        api_patterns = [
            "api.themoviedb.org",
            "tmdb",
        ]
        return any(pattern in url.lower() for pattern in api_patterns)

    def get_requests(self) -> list:
        return self.captured_requests

    def get_responses(self) -> list:
        return self.captured_responses

    def get_failed_responses(self) -> list:
        return [r for r in self.captured_responses if r["status"] >= 400]

    def get_successful_responses(self) -> list:
        return [r for r in self.captured_responses if 200 <= r["status"] < 300]

    def assert_api_called(self, url_pattern: str):
        matching = [r for r in self.captured_requests if url_pattern in r["url"]]
        assert len(matching) > 0, f"Expected API call matching '{url_pattern}' but none found"
        logger.info(f"Verified API call to: {url_pattern}")

    def assert_response_status(self, url_pattern: str, expected_status: int):
        matching = [r for r in self.captured_responses if url_pattern in r["url"]]
        assert len(matching) > 0, f"No response found matching '{url_pattern}'"
        actual_status = matching[-1]["status"]
        assert actual_status == expected_status, (
            f"Expected status {expected_status} for '{url_pattern}', got {actual_status}"
        )
        logger.info(f"Verified response status {expected_status} for: {url_pattern}")

    def clear(self):
        self.captured_requests.clear()
        self.captured_responses.clear()

    def wait_for_api_response(self, url_pattern: str, timeout: int = 15000):
        logger.info(f"Waiting for API response matching: {url_pattern}")
        with self.page.expect_response(
            lambda response: url_pattern in response.url,
            timeout=timeout
        ) as response_info:
            pass
        response = response_info.value
        logger.info(f"Received response: {response.status} {response.url}")
        return response
