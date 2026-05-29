"""
Test Suite: Page Load and Smoke Tests
Validates that the application loads correctly and core UI elements are present.
"""
import logging
import pytest
from pages.discover_page import DiscoverPage
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)


@pytest.mark.smoke
class TestPageLoad:
    """Verify the application loads and displays essential UI elements."""

    def test_page_loads_successfully(self, app_page):
        """
        TC-001: Verify the discover page loads without errors.
        Steps:
            1. Navigate to the base URL
            2. Wait for the page to fully load
            3. Verify the page title is 'Discover'
        Expected: Page loads with title 'Discover'.
        """
        logger.info("TC-001: Verifying page loads successfully")
        assert app_page.title() == "Discover", f"Expected title 'Discover', got '{app_page.title()}'"
        logger.info(f"Page title verified: {app_page.title()}")

    def test_content_cards_displayed(self, app_page):
        """
        TC-002: Verify content cards are displayed on initial load.
        Steps:
            1. Navigate to the discover page
            2. Wait for content to load
            3. Count visible content cards
        Expected: 20 content cards are displayed (grid of 3 columns).
        """
        logger.info("TC-002: Verifying content cards are displayed")
        discover = DiscoverPage(app_page)
        cards = discover.get_content_cards()
        assert len(cards) == 20, f"Expected 20 cards, got {len(cards)}"
        logger.info(f"Verified {len(cards)} content cards displayed")

    def test_card_has_title_and_metadata(self, app_page):
        """
        TC-003: Verify each card displays title, genre, and year.
        Steps:
            1. Get all content cards
            2. For each card, verify title and metadata exist
        Expected: Every card has a title and genre/year metadata.
        """
        logger.info("TC-003: Verifying card content structure")
        discover = DiscoverPage(app_page)
        titles = discover.get_card_titles()
        metadata = discover.get_card_metadata()

        assert len(titles) > 0, "No card titles found"
        assert len(metadata) > 0, "No card metadata found"
        assert len(titles) == len(metadata), "Title/metadata count mismatch"

        for i, (title, meta) in enumerate(zip(titles[:3], metadata[:3])):
            logger.info(f"  Card {i+1}: '{title}' | {meta}")
            assert len(title) > 0, f"Card {i+1} has empty title"
            assert "," in meta, f"Card {i+1} metadata missing genre/year separator"

    def test_card_images_loaded(self, app_page):
        """
        TC-004: Verify card images are loaded from TMDB.
        Steps:
            1. Get all card images
            2. Verify src attribute points to TMDB image server
        Expected: Images load from image.tmdb.org.
        """
        logger.info("TC-004: Verifying card images")
        images = app_page.query_selector_all("img[alt='Movie Poster']")
        assert len(images) > 0, "No movie poster images found"

        for img in images[:5]:
            src = img.get_attribute("src")
            assert "image.tmdb.org" in src, f"Image src not from TMDB: {src}"
        logger.info(f"Verified {len(images)} images from TMDB")

    def test_navigation_categories_present(self, app_page):
        """
        TC-005: Verify navigation categories (Popular, Trend, Newest, Top rated) are displayed.
        Steps:
            1. Get all navigation links
            2. Verify expected categories exist
        Expected: All four category tabs are present.
        """
        logger.info("TC-005: Verifying navigation categories")
        discover = DiscoverPage(app_page)
        categories = discover.get_nav_categories()

        expected = ["Popular", "Trend", "Newest", "Top rated"]
        for cat in expected:
            assert cat in categories, f"Category '{cat}' not found in {categories}"
        logger.info(f"All categories present: {categories}")

    def test_discover_options_panel_present(self, app_page):
        """
        TC-006: Verify the DISCOVER OPTIONS panel is visible with filters.
        Steps:
            1. Look for 'DISCOVER OPTIONS' heading
            2. Verify Type, Genre, Year, Rating sections exist
        Expected: Filter panel with all filter options is displayed.
        """
        logger.info("TC-006: Verifying discover options panel")
        page_text = app_page.text_content("body")

        assert "DISCOVER OPTIONS" in page_text, "DISCOVER OPTIONS panel not found"
        assert "Type" in page_text, "Type filter label not found"
        assert "Genre" in page_text, "Genre filter label not found"
        assert "Year" in page_text, "Year filter label not found"
        assert "Rating" in page_text, "Rating filter label not found"
        logger.info("All filter sections present in DISCOVER OPTIONS panel")

    def test_default_category_is_popular(self, app_page):
        """
        TC-007: Verify the default active category is 'Popular'.
        Steps:
            1. Load the page
            2. Check which category tab is active (white text)
        Expected: 'Popular' is the active category by default.
        """
        logger.info("TC-007: Verifying default category")
        discover = DiscoverPage(app_page)
        active = discover.get_active_category()
        logger.info(f"Active category: '{active}'")
        assert active == "Popular", f"Expected default category 'Popular', got '{active}'"

    def test_default_type_is_movie(self, app_page):
        """
        TC-008: Verify the default content type is 'Movie'.
        Steps:
            1. Load the page
            2. Check the Type dropdown value
        Expected: 'Movie' is selected by default.
        """
        logger.info("TC-008: Verifying default type filter")
        discover = DiscoverPage(app_page)
        current_type = discover.get_current_type()
        logger.info(f"Default type: '{current_type}'")
        assert current_type == "Movie", f"Expected default type 'Movie', got '{current_type}'"
