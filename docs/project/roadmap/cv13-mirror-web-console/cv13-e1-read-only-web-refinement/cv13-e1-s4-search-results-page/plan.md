[< Story](index.md)

# Plan — CV13.E1.S4 Search results page

## Design

This story converts the search affordance into a first useful read-only page. The implementation remains intentionally modest: lexical matching over recent memories only.

Implementation:

- update the header search markup from disabled input to a form;
- add submit handling in `app.js`;
- add `GET /api/surface/search?q=<query>`;
- extend `SearchSurface.search()` to search recent memory summaries when a `MemoryService` is available;
- render the page with the same `SearchResults`/`SearchResultItem` card grammar already used by memory category drilldown;
- use browser history so Back returns to the previous page.

## Tests

- add focused `SearchSurface` coverage for lexical memory results and empty query/results;
- add web route serialization coverage;
- keep browser validation through `node --check`.

## Risk

The main risk is expectation-setting. This is a first result page, not full Mirror search. Copy should say results are from retained memories so the surface does not imply complete coverage of conversations, journeys, identity, or docs.
