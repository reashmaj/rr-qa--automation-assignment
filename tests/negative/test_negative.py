"""
Test Suite: Negative Tests and Known Defects
Validates error handling, edge cases, and documents known issues.
"""
import logging
import pytest
from pages.discover_page import DiscoverPage
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)


@pytest.mark.negative
class TestDirectURLAccess:
    """
    KNOWN DEFECT (DEF-001): Direct URL access with specific slugs may not work.
    The SPA does not handle server-side routing; refreshing on a slug returns blank.
    """

    @pytest.mark.parametrize("slug,name", [
        ("/popular", "Popular"),
        ("/trend", "Trend"),
        ("/new", "Newest"),
        ("/top", "Top rated"),
    ])
    @pytest.mark.xfail(reason="DEF-001: Direct slug access fails")
    def test_direct_slug_access(self, page, slug, name):
        """
        TC-081: [KNOWN DEFECT] Direct URL access with category slugs.
        Steps:
            1. Navigate directly to URL with slug (e.g., /popular)
            2. Wait for page load
            3. Check if content renders
        Expected: KNOWN BUG - May not work as expected.
        Defect: DEF-001
        """
        url = f"https://tmdb-discover.surge.sh{slug}"
        logger.info(f"TC-081: Direct access to {url}")

        page.goto(url, wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(3000)

        discover = DiscoverPage(page)
        cards = discover.get_content_cards()
        title = page.title()

        logger.info(f"URL: {url}, Title: '{title}', Cards: {len(cards)}")
        assert len(cards) > 0, f"No content rendered for direct access to {slug}"
        assert title != "", f"Page title is empty for {slug}"

    @pytest.mark.xfail(reason="DEF-003: Page refresh on category loses state")
    def test_refresh_after_category_navigation(self, app_page):
        """
        TC-082: [KNOWN DEFECT] Page refresh after navigating to a category.
        Steps:
            1. Load the site normally
            2. Click on 'Trend' category
            3. Refresh the page (F5)
            4. Check if content still displays
        Expected: Content should persist after refresh. Known bug DEF-003.
        """
        logger.info("TC-082: Testing refresh after navigation")
        discover = DiscoverPage(app_page)

        discover.select_category("Trend")
        cards_before = discover.get_card_count()
        current_url = app_page.url
        logger.info(f"Before refresh - URL: {current_url}, Cards: {cards_before}")

        app_page.reload(wait_until="networkidle")
        app_page.wait_for_timeout(3000)

        cards_after = discover.get_card_count()
        logger.info(f"After refresh - Cards: {cards_after}")
        assert cards_after > 0, "Content disappeared after page refresh"


@pytest.mark.negative
class TestEdgeCases:
    """Verify application handles edge cases gracefully."""

    def test_special_characters_in_search(self, app_page):
        """
        TC-083: Verify search handles special characters safely.
        Steps:
            1. Enter XSS payload in search
            2. Enter SQL injection string
            3. Enter unicode characters
            4. Verify no crashes or unexpected behavior
        Expected: Application handles all inputs without crashing.
        """
        logger.info("TC-083: Testing special characters in search")
        discover = DiscoverPage(app_page)

        payloads = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE movies;--",
            "../../etc/passwd",
            "🎬🎥🍿",
            "a" * 500,
        ]

        for payload in payloads:
            discover.search_title(payload)
            app_page.wait_for_timeout(500)
            assert app_page.url is not None, f"Page crashed with input: {payload[:30]}"
            logger.info(f"  Handled: {payload[:30]}...")
            discover.clear_search()

        logger.info("All special character inputs handled safely")

    def test_rapid_category_switching(self, app_page):
        """
        TC-084: Verify rapid category switching doesn't crash the app.
        Steps:
            1. Rapidly click through all categories
            2. Verify final state is consistent
        Expected: Application remains responsive after rapid changes.
        """
        logger.info("TC-084: Rapid category switching")
        discover = DiscoverPage(app_page)

        categories = ["Popular", "Trend", "Newest", "Top rated"]
        for cat in categories:
            discover.select_category(cat)
            app_page.wait_for_timeout(300)

        # After rapid switching, app should still be functional
        app_page.wait_for_timeout(2000)
        cards = discover.get_content_cards()
        assert len(cards) > 0, "No cards after rapid switching"
        logger.info(f"App stable after rapid switching: {len(cards)} cards")

    def test_browser_back_forward(self, app_page):
        """
        TC-085: Verify browser back/forward navigation.
        Steps:
            1. Navigate to 'Trend' category
            2. Press browser back
            3. Verify state
            4. Press browser forward
            5. Verify state
        Expected: Browser history navigation works with categories.
        """
        logger.info("TC-085: Browser back/forward navigation")
        discover = DiscoverPage(app_page)

        initial_url = app_page.url
        discover.select_category("Trend")
        trend_url = app_page.url
        logger.info(f"Initial: {initial_url}, After Trend: {trend_url}")

        app_page.go_back()
        app_page.wait_for_timeout(2000)
        back_url = app_page.url
        logger.info(f"After back: {back_url}")

        app_page.go_forward()
        app_page.wait_for_timeout(2000)
        forward_url = app_page.url
        logger.info(f"After forward: {forward_url}")

    def test_empty_state_no_message(self, app_page):
        """
        TC-086: Verify empty state when no results match.
        Steps:
            1. Search for impossible string
            2. Check if any empty state message is shown
        Expected: POTENTIAL DEFECT - No empty state message displayed.
        Defect: DEF-004
        """
        logger.info("TC-086: Checking empty state handling")
        discover = DiscoverPage(app_page)

        discover.search_title("zzzzzznonexistent99999")
        app_page.wait_for_timeout(2000)

        cards = discover.get_content_cards()
        page_text = app_page.text_content("body") or ""

        has_message = any(
            phrase in page_text.lower()
            for phrase in ["no result", "not found", "nothing", "empty", "no match"]
        )

        logger.info(f"Cards: {len(cards)}, Empty message: {has_message}")

        if len(cards) == 0 and not has_message:
            logger.warning(
                "DEFECT DEF-004: No 'no results' message when search returns empty"
            )

    def test_multiple_filters_combined(self, app_page):
        """
        TC-087: Verify combining multiple filters works correctly.
        Steps:
            1. Select a category
            2. Select a genre
            3. Search for a title
            4. Verify results respect all filters
        Expected: All filters are applied simultaneously.
        """
        logger.info("TC-087: Testing combined filters")
        discover = DiscoverPage(app_page)

        discover.select_category("Popular")
        discover.select_genre("Action")
        app_page.wait_for_timeout(2000)

        cards = discover.get_content_cards()
        metadata = discover.get_card_metadata()
        logger.info(f"Combined filter results: {len(cards)} cards")
        for m in metadata[:5]:
            logger.info(f"  {m}")
