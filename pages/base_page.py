import logging
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="networkidle")

    def wait_for_element(self, selector: str, timeout: int = 10000):
        logger.debug(f"Waiting for element: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)

    def click(self, selector: str):
        logger.debug(f"Clicking element: {selector}")
        self.page.click(selector)

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector) or ""

    def get_all_texts(self, selector: str) -> list:
        return self.page.locator(selector).all_text_contents()

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def screenshot(self, path: str):
        logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path)

    def intercept_api_calls(self, url_pattern: str) -> list:
        """Intercept and collect API calls matching the pattern."""
        responses = []

        def handle_response(response):
            if url_pattern in response.url:
                responses.append(response)

        self.page.on("response", handle_response)
        return responses
