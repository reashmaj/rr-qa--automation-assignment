# Defect Report

## Summary
The following defects were identified during testing of https://tmdb-discover.surge.sh/

---

## DEF-001: Direct URL Access with Slugs Fails

**Severity:** Medium  
**Priority:** High  
**Status:** Open  
**Category:** Navigation / Routing

**Description:**  
Accessing the website using specific URL slugs (e.g., `/popular`, `/trending`, `/newest`, `/top-rated`) results in the page not loading correctly. The application appears to be a Single Page Application (SPA) that does not handle server-side routing.

**Steps to Reproduce:**
1. Open a browser
2. Navigate directly to `https://tmdb-discover.surge.sh/popular`
3. Observe the page

**Expected Result:** The page should load and display content for the "Popular" category.

**Actual Result:** Page may display blank content, an error, or fail to render the expected content.

**Impact:** Users who bookmark category-specific URLs or share links will encounter broken pages. Search engine crawling is also affected.

**Suggested Fix:** Implement proper client-side route handling with fallback to index.html (SPA routing configuration on the hosting platform).

---

## DEF-002: Pagination Fails on Last Pages

**Severity:** Medium  
**Priority:** Medium  
**Status:** Open  
**Category:** Pagination

**Description:**  
Pagination works correctly for the first few pages, but the last few pages may not function properly. Content may fail to load or display incorrectly.

**Steps to Reproduce:**
1. Navigate to `https://tmdb-discover.surge.sh/`
2. Scroll to pagination controls
3. Navigate to the last available page (or a high page number)
4. Observe the content

**Expected Result:** Content should display on all pages, including the last pages.

**Actual Result:** Last few pages show empty content or fail to load data.

**Impact:** Users browsing through all available content cannot access the last portion of results.

**Suggested Fix:** Add validation for total page count, handle edge cases in pagination logic, implement graceful error handling for out-of-range pages.

---

## DEF-003: Page Refresh on Category Slug Loses State

**Severity:** Low  
**Priority:** Medium  
**Status:** Open  
**Category:** State Management

**Description:**  
When a user navigates to a category (which updates the URL) and then refreshes the page, the application may lose the current state and display blank or default content.

**Steps to Reproduce:**
1. Navigate to `https://tmdb-discover.surge.sh/`
2. Select "Trending" category
3. Observe the URL change
4. Press F5 or Ctrl+R to refresh
5. Observe the page state

**Expected Result:** Page should reload and display the "Trending" category content.

**Actual Result:** Page may show blank content or revert to a broken state.

**Impact:** Users who refresh the page after navigating lose their current view.

---

## DEF-004: No Empty State Message (Potential)

**Severity:** Low  
**Priority:** Low  
**Status:** To Verify  
**Category:** UX

**Description:**  
When filters are applied that return no results, the application may not display an appropriate "No results found" message, leaving users with a blank area.

**Steps to Reproduce:**
1. Navigate to `https://tmdb-discover.surge.sh/`
2. Search for a non-existent title (e.g., "xyznonexistent12345")
3. Observe the content area

**Expected Result:** A user-friendly "No results found" message should be displayed.

**Actual Result:** Content area may appear blank without any feedback.

**Impact:** Poor user experience; users don't know if the search is still loading or if there are truly no results.

---

## Environment
- **Browser:** Chromium (via Playwright)
- **OS:** macOS
- **Date:** 2026-05-26
- **URL:** https://tmdb-discover.surge.sh/
