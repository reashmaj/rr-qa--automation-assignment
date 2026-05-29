import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class DiscoverPage(BasePage):
    URL = "https://tmdb-discover.surge.sh/"

    # Navigation - using href attributes for specificity
    NAV_LINKS = "nav > ul.list-none > li > a"
    NAV_POPULAR = "nav a[href='/popular']"
    NAV_TREND = "nav a[href='/trend']"
    NAV_NEWEST = "nav a[href='/new']"
    NAV_TOP_RATED = "nav a[href='/top']"
    ACTIVE_NAV = "nav > ul > li.text-white > a"

    # Content Cards - using direct child combinator
    CARDS_GRID = ".grid.grid-cols-3"
    CARD_ITEM = ".grid.grid-cols-3 > div"
    CARD_TITLE = "p.text-blue-500.font-bold"
    CARD_META = "p.text-gray-500.font-light"
    CARD_IMAGE = "img[alt='Movie Poster']"

    # Search - using name attribute
    SEARCH_INPUT = "input[name='search']"

    # React-Select Dropdowns - using unique IDs
    TYPE_DROPDOWN = "#react-select-2-input"
    GENRE_DROPDOWN = "#react-select-3-input"
    YEAR_START_DROPDOWN = "#react-select-4-input"
    YEAR_END_DROPDOWN = "#react-select-5-input"

    # React-Select - scoped using stable input IDs
    REACT_SELECT_OPTION = "div[id*='react-select'][id*='option']"
    REACT_SELECT_MENU = "div[role='listbox']"

    # Pagination - using aria-label attributes
    PAGINATION_PREV = "a[aria-label='Previous page']"
    PAGINATION_NEXT = "a[aria-label='Next page']"
    PAGINATION_SELECTED = "a[aria-current='page']"
    PAGINATION_ITEMS = "li a[role='button']"
    PAGINATION_BREAK = "li.break"

    # Rating stars
    RATING_SECTION = "text=Ratings"

    # Filter labels
    DISCOVER_OPTIONS = "text=DISCOVER OPTIONS"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self):
        logger.info("Loading Discover page")
        self.navigate(self.URL)
        self.page.locator(self.CARD_ITEM).first.wait_for()

    def get_nav_categories(self) -> list:
        logger.info("Getting navigation categories")
        categories = self.page.locator(self.NAV_LINKS).all_text_contents()
        logger.info(f"Found categories: {categories}")
        return categories

    def get_active_category(self) -> str:
        active = self.page.locator(self.ACTIVE_NAV)
        if active.count() > 0:
            return active.first.text_content().strip()
        return ""

    def select_category(self, category_name: str):
        logger.info(f"Selecting category: {category_name}")
        category_map = {
            "Popular": self.NAV_POPULAR,
            "Trend": self.NAV_TREND,
            "Newest": self.NAV_NEWEST,
            "Top rated": self.NAV_TOP_RATED,
        }
        selector = category_map.get(category_name, f"nav a:has-text('{category_name}')")
        self.page.locator(selector).click()
        self.page.locator(self.CARD_ITEM).first.wait_for()

    def get_content_cards(self) -> list:
        logger.info("Getting content cards")
        locator = self.page.locator(self.CARD_ITEM)
        cards = locator.all()
        logger.info(f"Found {len(cards)} content cards")
        return cards

    def get_card_count(self) -> int:
        return self.page.locator(self.CARD_ITEM).count()

    def get_card_titles(self) -> list:
        titles = self.page.locator(f"{self.CARD_ITEM} {self.CARD_TITLE}").all_text_contents()
        logger.info(f"Card titles ({len(titles)}): {titles[:5]}...")
        return titles

    def get_card_metadata(self) -> list:
        return self.page.locator(f"{self.CARD_ITEM} {self.CARD_META}").all_text_contents()

    # Search
    def search_title(self, title: str):
        logger.info(f"Searching for title: '{title}'")
        search = self.page.locator(self.SEARCH_INPUT)
        search.click()
        search.fill(title)
        self.page.wait_for_timeout(2000)

    def clear_search(self):
        logger.info("Clearing search input")
        self.page.locator(self.SEARCH_INPUT).fill("")
        self.page.wait_for_timeout(2000)

    def get_search_value(self) -> str:
        return self.page.locator(self.SEARCH_INPUT).input_value()

    # React-Select interactions
    def _open_react_select(self, input_id: str):
        self.page.locator(input_id).click()
        self.page.wait_for_timeout(500)

    def _select_react_option(self, option_text: str):
        self.page.locator(f"{self.REACT_SELECT_OPTION}:has-text('{option_text}')").first.click()
        self.page.wait_for_timeout(2000)

    def _get_react_select_value(self, input_id: str) -> str:
        container = self.page.locator(f"div:has({input_id})")
        value_el = container.locator("div[class*='-singleValue']")
        if value_el.count() > 0:
            return value_el.first.text_content().strip()
        return ""

    def select_type(self, content_type: str):
        logger.info(f"Selecting type: {content_type}")
        self._open_react_select(self.TYPE_DROPDOWN)
        self._select_react_option(content_type)

    def get_current_type(self) -> str:
        return self._get_react_select_value(self.TYPE_DROPDOWN)

    def select_genre(self, genre: str):
        logger.info(f"Selecting genre: {genre}")
        self._open_react_select(self.GENRE_DROPDOWN)
        self._select_react_option(genre)

    def get_current_genre(self) -> str:
        return self._get_react_select_value(self.GENRE_DROPDOWN)

    def select_year_start(self, year: str):
        logger.info(f"Selecting year start: {year}")
        self._open_react_select(self.YEAR_START_DROPDOWN)
        self._select_react_option(year)

    def select_year_end(self, year: str):
        logger.info(f"Selecting year end: {year}")
        self._open_react_select(self.YEAR_END_DROPDOWN)
        self._select_react_option(year)

    # Ratings
    def select_rating(self, stars: int):
        logger.info(f"Selecting rating: {stars} stars")
        rating_links = self.page.locator("a:has-text('★')")
        if stars <= rating_links.count():
            rating_links.nth(stars - 1).click()
            self.page.wait_for_timeout(2000)
        else:
            logger.warning(f"Rating {stars} stars not clickable")

    # Pagination
    def get_current_page(self) -> int:
        selected = self.page.locator(self.PAGINATION_SELECTED)
        if selected.count() > 0:
            text = selected.first.text_content().strip()
            try:
                return int(text)
            except ValueError:
                return 1
        return 1

    def get_total_pages(self) -> int:
        texts = self.page.locator(self.PAGINATION_ITEMS).all_text_contents()
        numbers = [int(t.strip()) for t in texts if t.strip().isdigit()]
        return max(numbers) if numbers else 1

    def go_to_next_page(self):
        logger.info("Clicking Next page")
        next_btn = self.page.locator(self.PAGINATION_NEXT)
        if next_btn.get_attribute("aria-disabled") == "true":
            logger.warning("Next button is disabled")
            return False
        next_btn.click()
        self.page.wait_for_timeout(3000)
        return True

    def go_to_previous_page(self):
        logger.info("Clicking Previous page")
        prev_btn = self.page.locator(self.PAGINATION_PREV)
        if prev_btn.get_attribute("aria-disabled") == "true":
            logger.warning("Previous button is disabled")
            return False
        prev_btn.click()
        self.page.wait_for_timeout(3000)
        return True

    def go_to_page(self, page_num: int):
        logger.info(f"Navigating to page {page_num}")
        self.page.locator(f"a[aria-label='Page {page_num}']").click()
        self.page.wait_for_timeout(3000)

    def is_pagination_visible(self) -> bool:
        return self.page.locator(self.PAGINATION_PREV).is_visible()

    def is_previous_disabled(self) -> bool:
        return self.page.locator(self.PAGINATION_PREV).get_attribute("aria-disabled") == "true"

    def is_next_disabled(self) -> bool:
        return self.page.locator(self.PAGINATION_NEXT).get_attribute("aria-disabled") == "true"
