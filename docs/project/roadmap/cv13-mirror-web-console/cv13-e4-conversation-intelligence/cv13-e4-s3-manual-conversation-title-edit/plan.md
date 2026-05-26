[< Story](index.md)

# Plan — CV13.E4.S3 Manual conversation title edit

## Implementation plan

1. Add `ConversationService.update_title()` with validation.
2. Add `POST /api/conversations/title` for a single conversation title.
3. Add a title edit form on the transcript page.
4. Refresh the transcript payload after save.
5. Add endpoint tests for success and invalid input.
6. Restart the web server and stop at manual validation.

## Design boundaries

- Manual title only.
- No LLM call.
- No message/content mutation.
