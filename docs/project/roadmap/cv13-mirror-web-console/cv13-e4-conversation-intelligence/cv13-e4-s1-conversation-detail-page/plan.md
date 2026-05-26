[< Story](index.md)

# Plan — CV13.E4.S1 Conversation detail page

## Implementation plan

1. Add a read-only conversation detail endpoint.
2. Serialize conversation metadata and ordered messages without exposing raw database internals.
3. Add a transcript renderer in the web app.
4. Support direct hash navigation for `#conversation/<id>`.
5. Add focused API tests.
6. Stop at manual browser validation.

## Design boundaries

- The page is read-only.
- It does not retitle or call an LLM.
- Workspace card linking remains CV13.E4.S2.
