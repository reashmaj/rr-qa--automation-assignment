import pytest
import logging
import allure
from playwright.sync_api import Page, BrowserContext

logger = logging.getLogger(__name__)

BASE_URL = "https://tmdb-discover.surge.sh/"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


@pytest.fixture
def app_page(page: Page) -> Page:
    logger.info(f"Navigating to {BASE_URL}")
    page.goto(BASE_URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    logger.info("Page loaded successfully")
    return page


@pytest.fixture
def api_context(context: BrowserContext):
    """Provide access to intercepted API requests."""
    api_requests = []

    def handle_request(request):
        if "api.themoviedb.org" in request.url or "tmdb" in request.url.lower():
            api_requests.append({
                "url": request.url,
                "method": request.method,
                "headers": request.headers,
            })

    context.on("request", handle_request)
    yield api_requests


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to Allure report on test failure."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("app_page") or item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
