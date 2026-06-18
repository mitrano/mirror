"""Builder-domain helpers for Ariad Refinement Workbench state."""

from __future__ import annotations

from dataclasses import dataclass

from memory.models import _now
from memory.storage.builder_workbench import ChangeRequestRecord, RefinementStoryRecord
from memory.storage.store import Store


@dataclass(frozen=True)
class RefinementStoryOverview:
    story: RefinementStoryRecord
    change_requests: tuple[ChangeRequestRecord, ...]


@dataclass(frozen=True)
class WorkbenchSnapshot:
    storage_state: str
    active_refinement_story: RefinementStoryRecord | None
    active_change_request: ChangeRequestRecord | None
    refinement_story_count: int
    change_request_count: int
    unassigned_change_request_count: int


def create_refinement_story(
    store: Store,
    *,
    journey: str,
    title: str,
    description: str | None = None,
    status: str = "draft",
    source: str = "manual",
    provenance: str | None = None,
) -> RefinementStoryRecord:
    """Create a durable Refinement Story without starting Refinement flow."""
    return store.create_refinement_story(
        journey=journey,
        title=title,
        description=description,
        status=status,
        source=source,
        provenance=provenance,
    )


def capture_change_request(
    store: Store,
    *,
    journey: str,
    title: str,
    body: str,
    refinement_story_id: str | None = None,
    status: str = "captured",
    source: str = "manual",
    provenance: str | None = None,
) -> ChangeRequestRecord:
    """Capture a durable Change Request without activating a CR cycle."""
    return store.create_change_request(
        journey=journey,
        title=title,
        body=body,
        refinement_story_id=refinement_story_id,
        status=status,
        source=source,
        provenance=provenance,
    )


def attach_change_request_to_story(
    store: Store,
    *,
    change_request_id: str,
    refinement_story_id: str,
) -> ChangeRequestRecord:
    """Associate an existing Change Request to a Refinement Story."""
    return store.attach_change_request_to_story(change_request_id, refinement_story_id)


def pull_refinement_story(
    store: Store, *, journey: str, refinement_story_id: str
) -> RefinementStoryOverview:
    """Pull a Refinement Story into active Refinement Work without selecting a CR."""
    overview = get_refinement_story_overview(
        store,
        journey=journey,
        refinement_story_id=refinement_story_id,
    )
    if overview.story.status != "active":
        store.update_refinement_story_status(overview.story.id, "active", pulled_at=_now())
    store.set_refinement_cursor(
        journey=journey,
        active_refinement_story_id=overview.story.id,
        active_change_request_id=None,
        last_refinement_event="refinement_story_pulled",
    )
    return get_refinement_story_overview(
        store,
        journey=journey,
        refinement_story_id=refinement_story_id,
    )


def get_active_refinement_story_overview(
    store: Store, journey: str
) -> RefinementStoryOverview | None:
    """Return the active Refinement Story overview for a journey, if any."""
    cursor = store.get_refinement_cursor(journey)
    if cursor is None or cursor.active_refinement_story_id is None:
        return None
    return get_refinement_story_overview(
        store,
        journey=journey,
        refinement_story_id=cursor.active_refinement_story_id,
    )


def get_refinement_story_overview(
    store: Store, *, journey: str, refinement_story_id: str
) -> RefinementStoryOverview:
    """Return one Refinement Story with its ordered Change Requests."""
    story = store.get_refinement_story(refinement_story_id)
    if story is None:
        raise ValueError("refinement_story_id does not exist")
    if story.journey != journey:
        raise ValueError("refinement_story_id belongs to a different journey")
    return RefinementStoryOverview(
        story=story,
        change_requests=store.list_change_requests(
            journey,
            refinement_story_id=refinement_story_id,
        ),
    )


def get_workbench_snapshot(store: Store, journey: str) -> WorkbenchSnapshot:
    """Return compact Workbench state for Builder Home rendering."""
    stories = store.list_refinement_stories(journey)
    change_requests = store.list_change_requests(journey)
    unassigned = tuple(cr for cr in change_requests if cr.refinement_story_id is None)
    cursor = store.get_refinement_cursor(journey)
    active_story = None
    active_change_request = None
    if cursor and cursor.active_refinement_story_id:
        active_story = store.get_refinement_story(cursor.active_refinement_story_id)
    if cursor and cursor.active_change_request_id:
        active_change_request = store.get_change_request(cursor.active_change_request_id)
    return WorkbenchSnapshot(
        storage_state="implemented",
        active_refinement_story=active_story,
        active_change_request=active_change_request,
        refinement_story_count=len(stories),
        change_request_count=len(change_requests),
        unassigned_change_request_count=len(unassigned),
    )
