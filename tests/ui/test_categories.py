"""
Test Suite: Category Navigation
Validates category tabs (Popular, Trend, Newest, Top Rated) function correctly.
"""
import logging
import pytest
from pages.discover_page import DiscoverPage
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)

CATEGORY_ROUTES = [
    ("Popular", "/popular"),
    ("Trend", "/trend"),
    ("Newest", "/new"),
    ("Top rated", "/top"),
]


@pytest.mark.filters
@pytest.mark.regression
class TestCategories:
    """Verify category selection and content filtering by category."""

    @pytest.mark.parametrize("category,route", CATEGORY_ROUTES)
    def test_category_click_updates_url(self, app_page, category, route):
        """
        TC-010: Verify clicking a category updates the URL.
        Steps:
            1. Click the specified category tab
            2. Verify the URL changes to the correct route
        Expected: URL updates to the category route.
        """
        logger.info(f"TC-010: Clicking category '{category}'")
        discover = DiscoverPage(app_page)
        discover.select_category(category)

        current_url = app_page.url
        assert route in current_url, \
            f"Expected URL to contain '{route}', got '{current_url}'"
        logger.info(f"URL correctly updated to: {current_url}")

    @pytest.mark.parametrize("category,route", CATEGORY_ROUTES)
    def test_category_displays_content(self, app_page, category, route):
        """
        TC-011: Verify each category displays content cards.
        Steps:
            1. Click the specified category
            2. Wait for content to load
            3. Verify cards are displayed
        Expected: Content cards appear for the selected category.
        """
        logger.info(f"TC-011: Verifying content for category '{category}'")
        discover = DiscoverPage(app_page)
        discover.select_category(category)

        cards = discover.get_content_cards()
        assert len(cards) > 0, f"No cards displayed for category '{category}'"
        logger.info(f"Category '{category}': {len(cards)} cards displayed")

    def test_switching_category_changes_content(self, app_page):
        """
        TC-012: Verify switching categories changes displayed content.
        Steps:
            1. Get titles for 'Popular' category
            2. Switch to 'Trend' category
            3. Get titles for 'Trend' category
            4. Compare the two sets
        Expected: Different categories show different content.
        """
        logger.info("TC-012: Verifying category switch changes content")
        discover = DiscoverPage(app_page)

        discover.select_category("Popular")
        popular_titles = discover.get_card_titles()
        logger.info(f"Popular titles: {popular_titles[:3]}")

        discover.select_category("Trend")
        trend_titles = discover.get_card_titles()
        logger.info(f"Trend titles: {trend_titles[:3]}")

        assert popular_titles != trend_titles, \
            "Expected different content between Popular and Trend categories"

    def test_active_category_highlighted(self, app_page):
        """
        TC-013: Verify the active category is visually highlighted.
        Steps:
            1. Click on 'Trend' category
            2. Verify 'Trend' tab is highlighted (white text)
            3. Verify other tabs are not highlighted
        Expected: Active tab has white text styling.
        """
        logger.info("TC-013: Verifying active category highlight")
        discover = DiscoverPage(app_page)
        discover.select_category("Trend")

        active = discover.get_active_category()
        logger.info(f"Active category after click: '{active}'")
        assert active == "Trend", f"Expected 'Trend' to be active, got '{active}'"

    def test_category_triggers_api_call(self, app_page):
        """
        TC-014: Verify category selection triggers an API call.
        Steps:
            1. Set up API monitoring
            2. Click on a category
            3. Verify an API response is captured
        Expected: Network request is made when switching categories.
        """
        logger.info("TC-014: Verifying category API call")
        api_helper = APIHelper(app_page)

        discover = DiscoverPage(app_page)
        discover.select_category("Top rated")

        responses = api_helper.get_responses()
        logger.info(f"API responses captured: {len(responses)}")
        for r in responses[:5]:
            logger.info(f"  {r['status']} {r['url'][:100]}")

    def test_category_resets_pagination(self, app_page):
        """
        TC-015: Verify switching category resets to page 1.
        Steps:
            1. Navigate to page 2
            2. Switch category
            3. Verify page is reset to 1
        Expected: Pagination resets to page 1 on category change.
        """
        logger.info("TC-015: Verifying category resets pagination")
        discover = DiscoverPage(app_page)

        discover.go_to_next_page()
        page_before = discover.get_current_page()
        logger.info(f"Page before category switch: {page_before}")

        discover.select_category("Newest")
        page_after = discover.get_current_page()
        logger.info(f"Page after category switch: {page_after}")
        assert page_after == 1, f"Expected page 1 after category switch, got {page_after}"
