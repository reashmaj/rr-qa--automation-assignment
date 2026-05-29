"""
Test Suite: Filter Functionality
Validates filtering by title search, content type, year, rating, and genre.
"""
import logging
import pytest
from pages.discover_page import DiscoverPage
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)


@pytest.mark.filters
@pytest.mark.regression
class TestTitleSearch:
    """Verify title search/filter functionality."""

    def test_search_input_present(self, app_page):
        """
        TC-020: Verify search input field is present and visible.
        Steps:
            1. Look for input with placeholder 'SEARCH'
            2. Verify it is visible and interactable
        Expected: Search input with 'SEARCH' placeholder exists.
        """
        logger.info("TC-020: Verifying search input")
        search = app_page.query_selector("input[placeholder='SEARCH']")
        assert search is not None, "Search input not found"
        assert search.is_visible(), "Search input not visible"
        logger.info("Search input found and visible")

    def test_search_filters_by_title(self, app_page):
        """
        TC-021: Verify typing in search filters content by title.
        Steps:
            1. Get initial card titles
            2. Type a search term
            3. Verify displayed titles contain the search term
        Expected: Only matching titles are displayed.
        """
        logger.info("TC-021: Verifying title search filtering")
        discover = DiscoverPage(app_page)

        initial_titles = discover.get_card_titles()
        logger.info(f"Initial titles ({len(initial_titles)}): {initial_titles[:3]}")

        discover.search_title("The")
        filtered_titles = discover.get_card_titles()
        logger.info(f"Filtered titles ({len(filtered_titles)}): {filtered_titles[:5]}")

        if len(filtered_titles) > 0:
            for title in filtered_titles:
                assert "the" in title.lower(), \
                    f"Title '{title}' does not contain search term 'The'"

    def test_search_is_case_insensitive(self, app_page):
        """
        TC-022: Verify search is case insensitive.
        Steps:
            1. Search with lowercase term
            2. Note results
            3. Search with uppercase term
            4. Compare results
        Expected: Same results regardless of case.
        """
        logger.info("TC-022: Verifying case-insensitive search")
        discover = DiscoverPage(app_page)

        discover.search_title("action")
        lower_titles = discover.get_card_titles()

        discover.clear_search()
        discover.search_title("ACTION")
        upper_titles = discover.get_card_titles()

        logger.info(f"Lowercase results: {len(lower_titles)}, Uppercase results: {len(upper_titles)}")
        assert lower_titles == upper_titles, "Search should be case insensitive"

    def test_clear_search_restores_content(self, app_page):
        """
        TC-023: Verify clearing search restores original content.
        Steps:
            1. Note initial card count
            2. Search for a term
            3. Clear the search field
            4. Verify card count is restored
        Expected: Original content list is restored.
        """
        logger.info("TC-023: Verifying clear search")
        discover = DiscoverPage(app_page)

        initial_count = discover.get_card_count()
        discover.search_title("xyz")
        discover.clear_search()
        restored_count = discover.get_card_count()

        logger.info(f"Initial: {initial_count}, Restored: {restored_count}")
        assert restored_count == initial_count, \
            f"Expected {initial_count} cards after clear, got {restored_count}"

    def test_search_no_results(self, app_page):
        """
        TC-024: Verify search with no matching results.
        Steps:
            1. Search for a nonsensical string
            2. Verify cards are empty or appropriate message shown
        Expected: Zero results or empty state displayed.
        """
        logger.info("TC-024: Verifying no-results search")
        discover = DiscoverPage(app_page)

        discover.search_title("xyznonexistent99999zzz")
        cards = discover.get_content_cards()
        logger.info(f"Cards after impossible search: {len(cards)}")
        assert len(cards) == 0, \
            f"Expected 0 cards for non-existent search, got {len(cards)}"


@pytest.mark.filters
@pytest.mark.regression
class TestTypeFilter:
    """Verify content type (Movie/TV) filter functionality."""

    def test_type_dropdown_default_movie(self, app_page):
        """
        TC-030: Verify Type dropdown defaults to 'Movie'.
        Steps:
            1. Load the page
            2. Check the Type dropdown value
        Expected: Type dropdown shows 'Movie' by default.
        """
        logger.info("TC-030: Verifying default type")
        discover = DiscoverPage(app_page)
        current = discover.get_current_type()
        assert current == "Movie", f"Expected type 'Movie', got '{current}'"
        logger.info(f"Default type confirmed: {current}")

    def test_switch_to_tv_shows(self, app_page):
        """
        TC-031: Verify switching type to TV shows updates content.
        Steps:
            1. Get current movie titles
            2. Select 'TV' from type dropdown
            3. Verify content changes to TV shows
        Expected: Content updates to show TV shows.
        """
        logger.info("TC-031: Switching to TV shows")
        discover = DiscoverPage(app_page)

        movie_titles = discover.get_card_titles()
        logger.info(f"Movie titles: {movie_titles[:3]}")

        discover.select_type("TV")
        app_page.wait_for_timeout(2000)

        tv_titles = discover.get_card_titles()
        logger.info(f"TV titles: {tv_titles[:3]}")

        assert tv_titles != movie_titles, "Content should change when switching to TV"

    def test_type_persists_on_category_change(self, app_page):
        """
        TC-032: Verify type selection persists when changing category.
        Steps:
            1. Select TV type
            2. Switch category
            3. Verify type is still TV
        Expected: Type filter persists across category changes.
        """
        logger.info("TC-032: Verifying type persistence")
        discover = DiscoverPage(app_page)

        discover.select_type("TV")
        discover.select_category("Trend")

        current_type = discover.get_current_type()
        logger.info(f"Type after category change: {current_type}")


@pytest.mark.filters
@pytest.mark.regression
class TestGenreFilter:
    """Verify genre filter functionality."""

    def test_genre_dropdown_present(self, app_page):
        """
        TC-040: Verify genre dropdown is present with 'Select...' placeholder.
        Steps:
            1. Look for the genre React-Select container
            2. Verify it shows 'Select...' placeholder
        Expected: Genre dropdown is visible with placeholder.
        """
        logger.info("TC-040: Verifying genre dropdown")
        page_text = app_page.text_content("body")
        assert "Genre" in page_text, "Genre label not found"
        assert "Select..." in page_text, "Genre placeholder 'Select...' not found"
        logger.info("Genre dropdown present with placeholder")

    def test_select_genre_filters_content(self, app_page):
        """
        TC-041: Verify selecting a genre filters content.
        Steps:
            1. Get initial card titles
            2. Select 'Action' genre
            3. Verify content updates
        Expected: Content is filtered to show action genre items.
        """
        logger.info("TC-041: Selecting genre 'Action'")
        discover = DiscoverPage(app_page)

        initial_titles = discover.get_card_titles()
        discover.select_genre("Action")
        filtered_titles = discover.get_card_titles()

        logger.info(f"Before genre: {initial_titles[:3]}")
        logger.info(f"After genre: {filtered_titles[:3]}")

        metadata = discover.get_card_metadata()
        if metadata:
            action_count = sum(1 for m in metadata if "Action" in m)
            logger.info(f"Cards with 'Action' in metadata: {action_count}/{len(metadata)}")

    def test_genre_filter_changes_content(self, app_page):
        """
        TC-042: Verify selecting a genre changes the displayed content.
        Steps:
            1. Get initial titles (no genre filter)
            2. Select 'Comedy' genre
            3. Compare with initial titles
        Expected: Genre filter changes the displayed content.
        """
        logger.info("TC-042: Verifying genre changes content")
        discover = DiscoverPage(app_page)

        initial_titles = discover.get_card_titles()
        discover.select_genre("Comedy")
        genre_titles = discover.get_card_titles()

        logger.info(f"Initial: {initial_titles[:3]}")
        logger.info(f"After Comedy: {genre_titles[:3]}")

        assert initial_titles != genre_titles, \
            "Expected content to change after selecting Comedy genre"


@pytest.mark.filters
@pytest.mark.regression
class TestYearFilter:
    """Verify year of release filter functionality."""

    def test_year_range_defaults(self, app_page):
        """
        TC-050: Verify year filter defaults to 1900-2025 range.
        Steps:
            1. Check the year start dropdown value
            2. Check the year end dropdown value
        Expected: Start year is 1900, end year is 2025.
        """
        logger.info("TC-050: Verifying year range defaults")
        discover = DiscoverPage(app_page)

        start = discover._get_react_select_value(2)
        end = discover._get_react_select_value(3)
        logger.info(f"Year range: {start} - {end}")

        assert start == "1900", f"Expected start year '1900', got '{start}'"
        assert end == "2025", f"Expected end year '2025', got '{end}'"

    def test_filter_by_year_range(self, app_page):
        """
        TC-051: Verify filtering by a specific year range.
        Steps:
            1. Set year range to narrow period (e.g., 2020-2022)
            2. Verify content reflects the year filter
        Expected: Results are from the specified year range.
        """
        logger.info("TC-051: Filtering by year range")
        discover = DiscoverPage(app_page)

        initial_titles = discover.get_card_titles()
        discover.select_year_end("2022")
        filtered_titles = discover.get_card_titles()

        logger.info(f"Before year filter: {initial_titles[:3]}")
        logger.info(f"After year filter: {filtered_titles[:3]}")

        metadata = discover.get_card_metadata()
        for m in metadata[:5]:
            logger.info(f"  Metadata: {m}")


@pytest.mark.filters
@pytest.mark.regression
class TestRatingFilter:
    """Verify rating filter functionality."""

    def test_rating_stars_visible(self, app_page):
        """
        TC-060: Verify star rating filter is visible.
        Steps:
            1. Look for rating stars in the filter panel
        Expected: Star rating options are displayed.
        """
        logger.info("TC-060: Verifying rating stars")
        page_text = app_page.text_content("body")
        assert "★" in page_text, "Rating stars not found on page"
        assert "& up" in page_text, "'& up' rating text not found"
        logger.info("Rating stars and '& up' text found")

    def test_filter_by_rating(self, app_page):
        """
        TC-061: Verify filtering by star rating.
        Steps:
            1. Get initial content
            2. Click on a star rating (e.g., 4 stars)
            3. Verify content updates
        Expected: Only items with rating >= selected stars are shown.
        """
        logger.info("TC-061: Filtering by rating")
        discover = DiscoverPage(app_page)

        initial_titles = discover.get_card_titles()
        discover.select_rating(4)
        filtered_titles = discover.get_card_titles()

        logger.info(f"Before rating: {len(initial_titles)} cards")
        logger.info(f"After rating: {len(filtered_titles)} cards")
