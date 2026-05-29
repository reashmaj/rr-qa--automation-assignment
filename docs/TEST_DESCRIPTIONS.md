# Test Case Descriptions

## Overview
This document describes the test cases for the TMDB Discover demo website (https://tmdb-discover.surge.sh/).
The test suite covers functional testing of filtering, pagination, API validation, and known defects.

---

## 1. Page Load & Smoke Tests

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-001 | Verify page loads successfully without errors | High | Smoke |
| TC-002 | Verify content cards are displayed on initial load | High | Smoke |
| TC-003 | Verify API calls are made when the page loads | High | Smoke |
| TC-004 | Verify navigation/category elements are present | High | Smoke |

### TC-001: Page Loads Successfully
**Precondition:** Internet connection available  
**Steps:**
1. Navigate to https://tmdb-discover.surge.sh/
2. Wait for the page to fully load (networkidle)
3. Verify the page title is not empty

**Expected Result:** Page loads within 30 seconds with no console errors.

### TC-002: Content Cards Displayed
**Precondition:** Page is loaded  
**Steps:**
1. Wait for dynamic content to render
2. Query for content card elements
3. Count the number of visible cards

**Expected Result:** At least 1 content card is visible.

---

## 2. Category Tests

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-010 | Verify all categories are visible (Popular, Trending, Newest, Top Rated) | High | Functional |
| TC-011 | Verify selecting 'Popular' category loads popular content | High | Functional |
| TC-012 | Verify selecting 'Trending' category loads trending content | High | Functional |
| TC-013 | Verify selecting 'Newest' category loads newest content | High | Functional |
| TC-014 | Verify selecting 'Top Rated' category loads top rated content | High | Functional |
| TC-015 | Verify switching categories changes content | Medium | Functional |
| TC-016 | Verify category selection triggers correct API call | Medium | API |

### TC-015: Category Switching Changes Content
**Precondition:** Page is loaded with default content  
**Steps:**
1. Capture titles of currently displayed content cards
2. Click a different category tab (e.g., "Trending")
3. Wait for content to update
4. Capture new titles

**Expected Result:** Content cards change after category switch.

---

## 3. Filter Tests

### Title/Search Filter

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-020 | Verify search input field exists | High | Functional |
| TC-021 | Verify searching by title filters content | High | Functional |
| TC-022 | Verify clearing search restores original content | Medium | Functional |
| TC-023 | Verify search with no results shows empty state | Medium | Negative |

### Type Filter (Movies/TV Shows)

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-030 | Verify type filter exists | High | Functional |
| TC-031 | Verify selecting 'Movies' shows only movies | High | Functional |
| TC-032 | Verify selecting 'TV Shows' shows only TV shows | High | Functional |

### Year Filter

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-040 | Verify year filter exists | Medium | Functional |
| TC-041 | Verify filtering by year shows correct content | Medium | Functional |

### Rating Filter

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-050 | Verify rating filter exists | Medium | Functional |
| TC-051 | Verify filtering by rating shows correctly rated content | Medium | Functional |

### Genre Filter

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-060 | Verify genre filter exists | High | Functional |
| TC-061 | Verify filtering by Action genre | Medium | Functional |
| TC-062 | Verify filtering by Comedy genre | Medium | Functional |
| TC-063 | Verify filtering by Drama genre | Medium | Functional |

---

## 4. Pagination Tests

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-070 | Verify pagination controls are visible | High | Functional |
| TC-071 | Verify 'Next' button navigates to next page | High | Functional |
| TC-072 | Verify 'Previous' button navigates to previous page | High | Functional |
| TC-073 | Verify content changes on page navigation | High | Functional |
| TC-074 | Verify API includes page parameter | Medium | API |
| TC-075 | Verify 'Previous' is disabled on page 1 | Medium | Boundary |
| TC-076 | [KNOWN DEFECT] Last pages may not function | Low | Negative |

---

## 5. Negative / Edge Case Tests

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-080 | [KNOWN DEFECT] Direct slug access (/popular) fails | Medium | Negative |
| TC-081 | [KNOWN DEFECT] Direct slug access (/trending) fails | Medium | Negative |
| TC-082 | [KNOWN DEFECT] Direct slug access (/newest) fails | Medium | Negative |
| TC-083 | [KNOWN DEFECT] Direct slug access (/top-rated) fails | Medium | Negative |
| TC-084 | [KNOWN DEFECT] Page refresh on category loses content | Medium | Negative |
| TC-085 | Rapid filter changes should not crash app | Low | Stress |
| TC-086 | Special characters in search (XSS, SQL injection) | Medium | Security |
| TC-087 | Empty state handling | Medium | UX |
| TC-088 | Browser back button functionality | Low | Navigation |

---

## 6. API Validation Tests

| ID | Test Case | Priority | Type |
|----|-----------|----------|------|
| TC-090 | Verify initial API call returns 200 | High | API |
| TC-091 | Verify API response contains expected data structure | High | API |
| TC-092 | Verify no failed API calls during normal usage | High | API |
| TC-093 | Verify API includes pagination parameter on page change | Medium | API |
| TC-094 | Verify API request headers are correct | Low | API |

---

## Test Design Techniques Used

1. **Equivalence Partitioning** - Grouping categories, genres, and content types into representative test cases
2. **Boundary Value Analysis** - Testing first page, last page, page transitions
3. **Error Guessing** - XSS attempts, SQL injection strings, rapid actions
4. **State Transition Testing** - Category switches, pagination navigation, browser history
5. **Decision Table Testing** - Filter combinations and their expected results
6. **Exploratory Testing** - Discovering defects through ad-hoc interactions

## Test Prioritization

- **High Priority:** Core functionality (page load, content display, basic filtering)
- **Medium Priority:** Advanced filters, API validation, known defects
- **Low Priority:** Edge cases, stress scenarios, cosmetic issues
