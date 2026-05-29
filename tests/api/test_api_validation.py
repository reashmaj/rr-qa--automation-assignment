"""
Test Suite: API Validation
Validates browser API calls, response codes, and data integrity via network interception.
"""
import logging
import json
import pytest
from pages.discover_page import DiscoverPage
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.regression
class TestAPIValidation:
    """Verify API calls made by the application and validate responses."""

    def test_page_load_triggers_api_call(self, page):
        """
        TC-090: Verify page load triggers API call to fetch content.
        Steps:
            1. Set up response interception
            2. Navigate to the page
            3. Capture API responses
        Expected: At least one API call is made on page load.
        """
        logger.info("TC-090: Verifying API call on page load")
        api_responses = []

        def capture(response):
            if "api.themoviedb.org" in response.url:
                api_responses.append({
                    "url": response.url,
                    "status": response.status,
                })

        page.on("response", capture)
        page.goto("https://tmdb-discover.surge.sh/", wait_until="networkidle")
        page.wait_for_timeout(5000)

        logger.info(f"Captured {len(api_responses)} TMDB API responses")
        for r in api_responses:
            logger.info(f"  {r['status']} {r['url'][:100]}")

        assert len(api_responses) > 0, "Expected API calls to TMDB on page load"

    def test_api_response_status_200(self, page):
        """
        TC-091: Verify API responses return HTTP 200.
        Steps:
            1. Intercept API responses
            2. Load the page
            3. Verify all responses have status 200
        Expected: All TMDB API calls return 200 OK.
        """
        logger.info("TC-091: Verifying API response status codes")
        api_responses = []

        def capture(response):
            if "api.themoviedb.org" in response.url:
                api_responses.append({
                    "url": response.url,
                    "status": response.status,
                })

        page.on("response", capture)
        page.goto("https://tmdb-discover.surge.sh/", wait_until="networkidle")
        page.wait_for_timeout(5000)

        for r in api_responses:
            logger.info(f"  {r['status']} {r['url'][:80]}")
            assert r["status"] == 200, \
                f"API call failed: {r['url']} returned {r['status']}"

    def test_api_response_json_structure(self, page):
        """
        TC-092: Verify API response contains expected JSON structure.
        Steps:
            1. Intercept API responses and parse JSON
            2. Verify response has 'results', 'page', 'total_pages' fields
        Expected: Response contains array of results and pagination metadata.
        """
        logger.info("TC-092: Verifying API response structure")
        api_data = []

        def capture(response):
            if "api.themoviedb.org" in response.url:
                try:
                    body = response.json()
                    api_data.append({
                        "url": response.url,
                        "data": body,
                    })
                except Exception:
                    pass

        page.on("response", capture)
        page.goto("https://tmdb-discover.surge.sh/", wait_until="networkidle")
        page.wait_for_timeout(5000)

        assert len(api_data) > 0, "No API JSON responses captured"

        for resp in api_data:
            data = resp["data"]
            if isinstance(data, dict) and "results" in data:
                logger.info(f"Response from: {resp['url'][:80]}")
                logger.info(f"  Keys: {list(data.keys())}")
                logger.info(f"  Results count: {len(data['results'])}")
                logger.info(f"  Page: {data.get('page')}")
                logger.info(f"  Total pages: {data.get('total_pages')}")

                assert "results" in data, "Missing 'results' field"
                assert "page" in data, "Missing 'page' field"
                assert "total_pages" in data, "Missing 'total_pages' field"
                assert isinstance(data["results"], list), "'results' should be an array"
                assert len(data["results"]) > 0, "'results' should not be empty"

    def test_api_result_item_structure(self, page):
        """
        TC-093: Verify individual result items have expected fields.
        Steps:
            1. Get API response results array
            2. Check each item for title, release_date, poster_path
        Expected: Each result has required movie/show fields.
        """
        logger.info("TC-093: Verifying result item structure")
        api_data = []

        def capture(response):
            if "api.themoviedb.org" in response.url:
                try:
                    body = response.json()
                    if isinstance(body, dict) and "results" in body:
                        api_data.append(body)
                except Exception:
                    pass

        page.on("response", capture)
        page.goto("https://tmdb-discover.surge.sh/", wait_until="networkidle")
        page.wait_for_timeout(5000)

        assert len(api_data) > 0, "No API data captured"

        results = api_data[0]["results"]
        for item in results[:3]:
            logger.info(f"  Item keys: {list(item.keys())}")
            # Movies have 'title', TV shows have 'name'
            has_title = "title" in item or "name" in item
            assert has_title, f"Item missing title/name: {item.keys()}"
            assert "poster_path" in item or "backdrop_path" in item, \
                "Item missing image path"
            logger.info(f"  Title: {item.get('title') or item.get('name')}")

    def test_category_change_triggers_new_api_call(self, page):
        """
        TC-094: Verify changing category triggers a new API call.
        Steps:
            1. Load page and count initial API calls
            2. Click on 'Trending' category
            3. Verify new API call is made
        Expected: Category change fetches new data from API.
        """
        logger.info("TC-094: Verifying category change triggers API call")
        api_calls = []

        def capture(response):
            if "api.themoviedb.org" in response.url:
                api_calls.append(response.url)

        page.on("response", capture)
        page.goto("https://tmdb-discover.surge.sh/", wait_until="networkidle")
        page.wait_for_timeout(3000)

        initial_count = len(api_calls)
        logger.info(f"Initial API calls: {initial_count}")

        # Click Trend category
        page.click("a[href='/trend']")
        page.wait_for_timeout(3000)

        new_count = len(api_calls)
        logger.info(f"API calls after category change: {new_count}")
        assert new_count > initial_count, \
            "Expected new API call after category change"

    def test_pagination_includes_page_parameter(self, page):
        """
        TC-095: Verify pagination sends page parameter in API call.
        Steps:
            1. Load page
            2. Click Next to go to page 2
            3. Verify API call includes page=2
        Expected: API request URL contains page parameter.
        """
        logger.info("TC-095: Verifying pagination API parameter")
        api_calls = []

        def capture(response):
            if "api.themoviedb.org" in response.url:
                api_calls.append(response.url)

        page.on("response", capture)
        page.goto("https://tmdb-discover.surge.sh/", wait_until="networkidle")
        page.wait_for_timeout(3000)

        # Click Next
        next_btn = page.query_selector("li.next a")
        if next_btn:
            next_btn.click()
            page.wait_for_timeout(3000)

        page2_calls = [url for url in api_calls if "page=2" in url]
        logger.info(f"API calls with page=2: {len(page2_calls)}")
        for url in page2_calls:
            logger.info(f"  {url[:120]}")

        assert len(page2_calls) > 0, "Expected API call with page=2 parameter"

    def test_no_api_errors_during_browsing(self, page):
        """
        TC-096: Verify no API errors occur during normal browsing flow.
        Steps:
            1. Set up error tracking
            2. Browse through categories and pages
            3. Verify no 4xx/5xx responses
        Expected: All API calls succeed during normal usage.
        """
        logger.info("TC-096: Checking for API errors during browsing")
        errors = []

        def capture(response):
            if "api.themoviedb.org" in response.url and response.status >= 400:
                errors.append({
                    "url": response.url,
                    "status": response.status,
                })

        page.on("response", capture)
        page.goto("https://tmdb-discover.surge.sh/", wait_until="networkidle")
        page.wait_for_timeout(3000)

        # Browse normally
        page.click("a[href='/trend']")
        page.wait_for_timeout(2000)
        page.click("a[href='/new']")
        page.wait_for_timeout(2000)

        # Navigate a page
        next_btn = page.query_selector("li.next a")
        if next_btn:
            next_btn.click()
            page.wait_for_timeout(2000)

        if errors:
            for err in errors:
                logger.error(f"API ERROR: {err['status']} {err['url'][:100]}")
            pytest.fail(f"Found {len(errors)} API errors during browsing")
        else:
            logger.info("No API errors during normal browsing")
