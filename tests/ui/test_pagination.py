"""
Test Suite: Pagination
Validates pagination controls, page navigation, and known pagination defects.
"""
import logging
import pytest
from pages.discover_page import DiscoverPage
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)


@pytest.mark.pagination
@pytest.mark.regression
class TestPagination:
    """Verify pagination functionality."""

    def test_pagination_visible(self, app_page):
        """
        TC-070: Verify pagination controls are displayed.
        Steps:
            1. Load the discover page
            2. Check for Previous/Next buttons and page numbers
        Expected: Pagination with Previous, page numbers, and Next is visible.
        """
        logger.info("TC-070: Verifying pagination visibility")
        discover = DiscoverPage(app_page)

        assert discover.is_pagination_visible(), "Pagination not visible"
        logger.info("Pagination controls are visible")

        current = discover.get_current_page()
        total = discover.get_total_pages()
        logger.info(f"Current page: {current}, Total pages: {total}")

    def test_default_page_is_one(self, app_page):
        """
        TC-071: Verify default page is page 1.
        Steps:
            1. Load the page
            2. Check the selected/active page number
        Expected: Page 1 is selected by default.
        """
        logger.info("TC-071: Verifying default page")
        discover = DiscoverPage(app_page)
        current = discover.get_current_page()
        assert current == 1, f"Expected page 1, got {current}"
        logger.info("Default page is 1")

    def test_previous_disabled_on_first_page(self, app_page):
        """
        TC-072: Verify Previous button is disabled on page 1.
        Steps:
            1. Ensure we are on page 1
            2. Check Previous button aria-disabled attribute
        Expected: Previous button has aria-disabled='true'.
        """
        logger.info("TC-072: Verifying Previous disabled on page 1")
        discover = DiscoverPage(app_page)

        is_disabled = discover.is_previous_disabled()
        assert is_disabled, "Previous button should be disabled on page 1"
        logger.info("Previous button correctly disabled on page 1")

    def test_navigate_to_next_page(self, app_page):
        """
        TC-073: Verify clicking Next navigates to page 2.
        Steps:
            1. Confirm current page is 1
            2. Click Next button
            3. Verify page changes to 2
        Expected: Current page becomes 2.
        """
        logger.info("TC-073: Navigating to next page")
        discover = DiscoverPage(app_page)

        assert discover.get_current_page() == 1
        discover.go_to_next_page()

        new_page = discover.get_current_page()
        assert new_page == 2, f"Expected page 2, got {new_page}"
        logger.info(f"Successfully navigated to page {new_page}")

    def test_navigate_to_previous_page(self, app_page):
        """
        TC-074: Verify clicking Previous navigates back.
        Steps:
            1. Navigate to page 2
            2. Click Previous button
            3. Verify page returns to 1
        Expected: Current page returns to 1.
        """
        logger.info("TC-074: Navigating back to previous page")
        discover = DiscoverPage(app_page)

        discover.go_to_next_page()
        assert discover.get_current_page() == 2

        discover.go_to_previous_page()
        new_page = discover.get_current_page()
        assert new_page == 1, f"Expected page 1, got {new_page}"
        logger.info("Successfully navigated back to page 1")

    def test_content_changes_on_page_navigation(self, app_page):
        """
        TC-075: Verify content changes between pages.
        Steps:
            1. Get titles on page 1
            2. Navigate to page 2
            3. Get titles on page 2
            4. Compare
        Expected: Different content on different pages.
        """
        logger.info("TC-075: Verifying content changes between pages")
        discover = DiscoverPage(app_page)

        page1_titles = discover.get_card_titles()
        discover.go_to_next_page()
        page2_titles = discover.get_card_titles()

        logger.info(f"Page 1: {page1_titles[:3]}")
        logger.info(f"Page 2: {page2_titles[:3]}")

        assert page1_titles != page2_titles, \
            "Expected different content on page 1 vs page 2"

    def test_navigate_to_specific_page(self, app_page):
        """
        TC-076: Verify clicking a specific page number navigates to it.
        Steps:
            1. Click on page number 3
            2. Verify current page is 3
        Expected: Page 3 is now the active page.
        """
        logger.info("TC-076: Navigating to specific page")
        discover = DiscoverPage(app_page)

        discover.go_to_page(3)
        current = discover.get_current_page()
        assert current == 3, f"Expected page 3, got {current}"
        logger.info(f"Successfully navigated to page {current}")

    def test_pagination_shows_total_pages(self, app_page):
        """
        TC-077: Verify pagination displays total page count.
        Steps:
            1. Get the highest page number visible in pagination
        Expected: Total pages > 1 (large dataset).
        """
        logger.info("TC-077: Checking total pages")
        discover = DiscoverPage(app_page)
        total = discover.get_total_pages()
        logger.info(f"Total pages: {total}")
        assert total > 1, f"Expected multiple pages, got {total}"

    def test_previous_enabled_on_page_2(self, app_page):
        """
        TC-078: Verify Previous button is enabled on page 2.
        Steps:
            1. Navigate to page 2
            2. Check Previous button is enabled
        Expected: Previous button is clickable.
        """
        logger.info("TC-078: Checking Previous enabled on page 2")
        discover = DiscoverPage(app_page)

        discover.go_to_next_page()
        is_disabled = discover.is_previous_disabled()
        assert not is_disabled, "Previous should be enabled on page 2"
        logger.info("Previous button enabled on page 2")


@pytest.mark.pagination
@pytest.mark.negative
class TestPaginationDefects:
    """Test known pagination defects."""

    @pytest.mark.xfail(reason="DEF-002: Pagination fails on last pages")
    def test_last_pages_not_functional(self, app_page):
        """
        TC-079: [KNOWN DEFECT] Last pages may not function properly.
        Steps:
            1. Get total page count
            2. Navigate to a very high page number
            3. Check if content loads
        Expected: Content should load on last page. Known bug DEF-002.
        """
        logger.info("TC-079: [DEFECT] Testing last pages")
        discover = DiscoverPage(app_page)

        total = discover.get_total_pages()
        logger.info(f"Total pages: {total}")

        assert total > 100, f"Expected many pages, got {total}"
        discover.go_to_page(total)
        app_page.wait_for_timeout(3000)
        cards = discover.get_content_cards()
        logger.info(f"Cards on last page ({total}): {len(cards)}")
        assert len(cards) > 0, f"Last page ({total}) shows no content"

    @pytest.mark.xfail(reason="DEF-002: High page numbers don't work")
    def test_high_page_number_navigation(self, app_page):
        """
        TC-080: [KNOWN DEFECT] Navigating to very high page numbers.
        Steps:
            1. Try to navigate to page 57039 (displayed in pagination)
            2. Check if content is returned
        Expected: Content should load on page 57039. Known bug DEF-002.
        """
        logger.info("TC-080: [DEFECT] High page number navigation")
        discover = DiscoverPage(app_page)

        discover.go_to_page(57039)
        app_page.wait_for_timeout(5000)
        cards = discover.get_content_cards()
        logger.info(f"Cards on page 57039: {len(cards)}")
        assert len(cards) > 0, "Page 57039 shows no content"
