[< Story](index.md)

# Plan — CV13.E4.S2 Conversation card linking and navigation

## Implementation plan

1. Use existing conversation card ids/hrefs to expose a clickable target in Workspace.
2. Add click and keyboard handling for conversation cards.
3. Route to the S1 transcript page with `#conversation/<id>` history.
4. Ensure the transcript back action returns to Workspace.
5. Add focused test coverage for conversation card link metadata.
6. Restart the web server and stop at manual validation.

## Design boundaries

- Navigation only.
- No mutation.
- No LLM call.
