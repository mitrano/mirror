"""Tests for Builder Workbench domain helpers."""

from memory.builder.workbench import (
    attach_change_request_to_story,
    capture_change_request,
    close_refinement_story,
    coherence_refinement_story,
    complete_change_request,
    confirm_change_request,
    create_refinement_story,
    discard_change_request,
    get_active_refinement_story_overview,
    get_refinement_story_overview,
    get_workbench_snapshot,
    mark_change_request_implemented,
    plan_change_request,
    pull_refinement_story,
    recommend_next_change_request,
    review_refinement_story,
    select_change_request,
    validate_change_request,
)
from memory.builder.workbench_surfaces import (
    render_change_request_captured_surface,
    render_change_request_discarded_surface,
    render_refinement_flow_event_surface,
    render_refinement_story_overview_surface,
    render_refinement_story_progress_surface,
    render_refinement_story_pulled_surface,
)


def test_workbench_snapshot_reports_empty_durable_storage(store):
    snapshot = get_workbench_snapshot(store, "mirror")

    assert snapshot.storage_state == "implemented"
    assert snapshot.active_refinement_story is None
    assert snapshot.active_change_request is None
    assert snapshot.refinement_story_count == 0
    assert snapshot.change_request_count == 0
    assert snapshot.unassigned_change_request_count == 0


def test_workbench_snapshot_reports_counts_and_active_records(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    unassigned = capture_change_request(
        store,
        journey="mirror",
        title="Show roadmap after Done",
        body="Render a roadmap-position surface after Done.",
    )
    attached = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
    )
    attached = attach_change_request_to_story(
        store,
        change_request_id=attached.id,
        refinement_story_id=story.id,
    )
    store.set_refinement_cursor(
        journey="mirror",
        active_refinement_story_id=story.id,
        active_change_request_id=attached.id,
        last_refinement_event="captured",
    )

    snapshot = get_workbench_snapshot(store, "mirror")

    assert snapshot.storage_state == "implemented"
    assert snapshot.active_refinement_story == story
    assert snapshot.active_change_request == attached
    assert snapshot.refinement_story_count == 1
    assert snapshot.change_request_count == 2
    assert snapshot.unassigned_change_request_count == 1
    assert unassigned.refinement_story_id is None


def test_pull_refinement_story_sets_cursor_without_active_cr(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )

    overview = pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)

    cursor = store.get_refinement_cursor("mirror")
    assert cursor is not None
    assert cursor.active_refinement_story_id == story.id
    assert cursor.active_change_request_id is None
    assert cursor.last_refinement_event == "refinement_story_pulled"
    assert overview.story.status == "active"
    active = get_active_refinement_story_overview(store, "mirror")
    assert active == overview


def test_refinement_story_pulled_surface_uses_consistent_simplified_shape(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    overview = pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)

    rendered = render_refinement_story_pulled_surface(journey="mirror", overview=overview)

    assert "<<<ARIAD:REFINEMENT_STORY_PULLED>>>" in rendered
    assert "RS Flow: ◉ Pull → ○ Select CR" in rendered
    assert "RS001: Builder lifecycle refinement" in rendered
    assert "Pulled" in rendered
    assert "This Refinement Story entered active Refinement Work." in rendered
    assert "change requests (#1)" in rendered
    assert "🟨 CR001: Plan safety [captured]" in rendered
    assert "journey" not in rendered
    assert "status" not in rendered
    assert "active refinement cursor" not in rendered
    assert "active CR: none" not in rendered
    assert "boundary" not in rendered


def test_discard_change_request_removes_only_captured_inactive_cr(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Mistaken CR",
        body="Captured by mistake.",
        refinement_story_id=story.id,
    )

    discard = discard_change_request(
        store,
        journey="mirror",
        change_request_id=cr.id,
        reason="Duplicate capture",
    )

    assert discard.change_request.id == cr.id
    assert discard.refinement_story == story
    assert discard.reason == "Duplicate capture"
    assert store.get_change_request(cr.id) is None
    rendered = render_change_request_discarded_surface(discard)
    assert "<<<ARIAD:CHANGE_REQUEST_DISCARDED>>>" in rendered
    assert "CR001: Mistaken CR" in rendered
    assert "Duplicate capture" in rendered
    assert "RS001: Builder lifecycle refinement" in rendered


def test_discard_change_request_rejects_active_or_non_captured_cr(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Active CR",
        body="Already selected.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)
    select_change_request(store, journey="mirror", change_request_id=cr.id)

    import pytest

    with pytest.raises(ValueError, match="only captured Change Requests can be discarded"):
        discard_change_request(
            store,
            journey="mirror",
            change_request_id=cr.id,
            reason="Mistake",
        )


def test_change_request_flow_transitions_in_order_and_clears_active_cr(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)

    selected = select_change_request(store, journey="mirror", change_request_id=cr.id)
    confirmed = confirm_change_request(store, journey="mirror", change_request_id=cr.id)
    planned = plan_change_request(
        store, journey="mirror", change_request_id=cr.id, summary="Plan it"
    )
    implemented = mark_change_request_implemented(
        store, journey="mirror", change_request_id=cr.id, evidence="Implemented elsewhere"
    )
    validated = validate_change_request(
        store, journey="mirror", change_request_id=cr.id, evidence="Validated state"
    )
    done = complete_change_request(store, journey="mirror", change_request_id=cr.id, notes="Done")

    assert selected.previous_status == "captured"
    assert confirmed.event == "change_request_confirmed"
    assert planned.new_status == "planned"
    assert implemented.new_status == "implemented"
    assert validated.new_status == "validated"
    assert done.new_status == "done"
    selected_rendered = render_refinement_flow_event_surface(selected)
    assert "🟪 CR001 SELECTED" in selected_rendered
    assert "Scope confirmation" in selected_rendered
    assert "My understanding:" in selected_rendered
    assert "- Plan safety" in selected_rendered
    assert "Preserve human-authored plan details." in selected_rendered
    assert "Before I plan or implement, confirm:" in selected_rendered
    assert "1. Is this the right scope?" in selected_rendered
    assert "2. Is anything out of scope?" in selected_rendered
    assert "3. What validation evidence will satisfy you?" in selected_rendered
    assert "This Change Request entered the active CR cycle." not in selected_rendered

    rendered = render_refinement_flow_event_surface(planned)
    assert "CR Cycle: ✓ Confirm → ◉ Plan → ○ Implement" in rendered
    assert "RS Flow:" not in rendered
    assert "🟦 CR001 PLANNED" in rendered
    assert "CR001: Plan safety" not in rendered
    assert "Plan it" in rendered
    assert "Scope confirmation" not in rendered
    assert "Refinement Story" in rendered
    assert "RS001: Builder lifecycle refinement" in rendered
    assert "current CR phase" not in rendered
    assert "implementation files changed" not in rendered
    assert "next conversational move" not in rendered
    cursor = store.get_refinement_cursor("mirror")
    assert cursor is not None
    assert cursor.active_change_request_id is None
    assert store.get_change_request(cr.id).outcome_notes == "Done"


def test_change_request_can_implement_after_confirmation_without_separate_plan(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)
    select_change_request(store, journey="mirror", change_request_id=cr.id)

    import pytest

    with pytest.raises(ValueError, match="confirmed Change Request is required"):
        mark_change_request_implemented(
            store,
            journey="mirror",
            change_request_id=cr.id,
            plan="Compact route",
            evidence="Implemented directly",
        )

    confirm_change_request(store, journey="mirror", change_request_id=cr.id)
    implemented = mark_change_request_implemented(
        store,
        journey="mirror",
        change_request_id=cr.id,
        plan="Compact route",
        evidence="Implemented directly",
    )

    assert implemented.previous_status == "active"
    assert implemented.new_status == "implemented"
    rendered = render_refinement_flow_event_surface(implemented)
    assert "🟧 CR001 IMPLEMENTED" in rendered
    assert "Implementation plan: Compact route" in rendered
    assert "evidence: Implemented directly" in rendered
    assert store.get_change_request(cr.id).status == "implemented"


def test_change_request_validation_can_close_with_done_note(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Validation close",
        body="Close after validation acceptance.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)
    select_change_request(store, journey="mirror", change_request_id=cr.id)
    confirm_change_request(store, journey="mirror", change_request_id=cr.id)
    mark_change_request_implemented(
        store,
        journey="mirror",
        change_request_id=cr.id,
        evidence="Implemented",
    )

    done = validate_change_request(
        store,
        journey="mirror",
        change_request_id=cr.id,
        evidence="Navigator accepted",
        close=True,
        notes="Closed from validation",
    )

    assert done.event == "change_request_done"
    assert done.previous_status == "implemented"
    assert done.new_status == "done"
    rendered = render_refinement_flow_event_surface(done)
    assert "◻ CR001 DONE" in rendered
    assert "Validation evidence: Navigator accepted" in rendered
    assert "Done note:" in rendered
    assert "Closed from validation" in rendered
    cursor = store.get_refinement_cursor("mirror")
    assert cursor is not None
    assert cursor.active_change_request_id is None
    assert cursor.last_refinement_event == "change_request_done"
    updated = store.get_change_request(cr.id)
    assert updated.status == "done"
    assert updated.completed_at is not None


def test_render_refinement_story_progress_surface_shows_bar_and_next_cr(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    done_cr = capture_change_request(
        store,
        journey="mirror",
        title="Done CR",
        body="Already done.",
        refinement_story_id=story.id,
    )
    next_cr = capture_change_request(
        store,
        journey="mirror",
        title="Next CR",
        body="Next work.",
        refinement_story_id=story.id,
    )
    remaining_cr = capture_change_request(
        store,
        journey="mirror",
        title="Remaining CR",
        body="Remaining work.",
        refinement_story_id=story.id,
    )
    store.update_change_request_status(done_cr.id, "done")
    overview = get_refinement_story_overview(store, journey="mirror", refinement_story_id=story.id)

    rendered = render_refinement_story_progress_surface(
        story=overview.story,
        change_requests=overview.change_requests,
        next_change_request=store.get_change_request(next_cr.id),
    )

    assert "<<<ARIAD:REFINEMENT_STORY_PROGRESS>>>" in rendered
    assert "RS001 PROGRESS" in rendered
    assert "Builder lifecycle refinement" in rendered
    assert "🟩🟥🟥 1/3 done" in rendered
    assert "🟩 done   🟦 next   🟥 remaining" in rendered
    assert "🟩 CR001: Done CR" in rendered
    assert "🟦 CR002: Next CR" in rendered
    assert "🟥 CR003: Remaining CR" in rendered
    assert "Next CR recommendation: CR002" in rendered
    assert remaining_cr.id not in rendered


def test_recommend_next_change_request_after_closure(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    done_cr = capture_change_request(
        store,
        journey="mirror",
        title="Done CR",
        body="Already done.",
        refinement_story_id=story.id,
    )
    next_cr = capture_change_request(
        store,
        journey="mirror",
        title="Next CR",
        body="Next work.",
        refinement_story_id=story.id,
    )
    later_cr = capture_change_request(
        store,
        journey="mirror",
        title="Later CR",
        body="Later work.",
        refinement_story_id=story.id,
    )
    store.update_change_request_status(done_cr.id, "done")
    store.update_change_request_status(later_cr.id, "parked")

    recommendation = recommend_next_change_request(
        store,
        journey="mirror",
        refinement_story_id=story.id,
    )

    assert recommendation == store.get_change_request(next_cr.id)


def test_change_request_flow_rejects_invalid_order(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)

    import pytest

    with pytest.raises(ValueError, match="active Change Request is required"):
        plan_change_request(store, journey="mirror", change_request_id=cr.id, summary="Too soon")


def test_refinement_story_review_coherence_close_flow(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)
    select_change_request(store, journey="mirror", change_request_id=cr.id)
    confirm_change_request(store, journey="mirror", change_request_id=cr.id)
    plan_change_request(store, journey="mirror", change_request_id=cr.id, summary="Plan")
    mark_change_request_implemented(
        store, journey="mirror", change_request_id=cr.id, evidence="Implemented"
    )
    validate_change_request(store, journey="mirror", change_request_id=cr.id, evidence="Valid")
    complete_change_request(store, journey="mirror", change_request_id=cr.id, notes="Done")

    review = review_refinement_story(
        store, journey="mirror", refinement_story_id=story.id, summary="Review only"
    )
    coherence = coherence_refinement_story(
        store, journey="mirror", refinement_story_id=story.id, summary="Coherent"
    )
    close = close_refinement_story(
        store, journey="mirror", refinement_story_id=story.id, summary="Closed"
    )

    assert review.event == "refinement_story_reviewed"
    assert coherence.event == "refinement_story_coherent"
    assert close.new_status == "closed"
    rendered = render_refinement_flow_event_surface(close)
    assert (
        "RS Flow: ✓ Pull → ✓ Select CR → ✓ CR Cycle → ✓ Review → ✓ Coherence → ◉ Close" in rendered
    )
    assert "CR Cycle:" not in rendered
    assert "◻ RS001 CLOSED" in rendered
    assert "RS001: Builder lifecycle refinement" not in rendered
    assert "Closed" in rendered
    assert "Refinement Story" not in rendered
    assert "current RS phase" not in rendered
    assert "closure record" not in rendered
    cursor = store.get_refinement_cursor("mirror")
    assert cursor is not None
    assert cursor.active_refinement_story_id is None
    assert store.get_change_request(cr.id).outcome_notes == "Done"


def test_refinement_story_close_rejects_unfinished_change_requests(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)
    review_refinement_story(store, journey="mirror", refinement_story_id=story.id, summary="Review")
    coherence_refinement_story(
        store, journey="mirror", refinement_story_id=story.id, summary="Coherent"
    )

    import pytest

    with pytest.raises(ValueError, match="unfinished Change Requests"):
        close_refinement_story(
            store, journey="mirror", refinement_story_id=story.id, summary="Close"
        )
    cursor = store.get_refinement_cursor("mirror")
    assert cursor is not None
    assert cursor.active_refinement_story_id == story.id
    assert store.get_change_request(cr.id).status == "captured"


def test_refinement_story_review_requires_active_story(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")

    import pytest

    with pytest.raises(ValueError, match="active Refinement Story is required"):
        review_refinement_story(
            store, journey="mirror", refinement_story_id=story.id, summary="Review"
        )


def test_refinement_story_overview_omits_ribbons_even_with_active_cr(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    cr = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    pull_refinement_story(store, journey="mirror", refinement_story_id=story.id)
    select_change_request(store, journey="mirror", change_request_id=cr.id)
    confirm_change_request(store, journey="mirror", change_request_id=cr.id)
    plan_change_request(store, journey="mirror", change_request_id=cr.id, summary="Plan")
    mark_change_request_implemented(
        store, journey="mirror", change_request_id=cr.id, evidence="Implemented"
    )

    overview = get_refinement_story_overview(
        store,
        journey="mirror",
        refinement_story_id=story.id,
    )
    rendered = render_refinement_story_overview_surface(journey="mirror", overview=overview)

    assert "RS Flow:" not in rendered
    assert "CR Cycle:" not in rendered


def test_refinement_story_overview_renders_simplified_action_ordered_cr_surface(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    done = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body="Preserve human-authored plan details.",
        refinement_story_id=story.id,
    )
    captured = capture_change_request(
        store,
        journey="mirror",
        title="Roadmap after Done",
        body="Show roadmap position after Delivery Done.",
        refinement_story_id=story.id,
    )
    planned = capture_change_request(
        store,
        journey="mirror",
        title="Use display codes",
        body="Show CR display codes instead of ids.",
        refinement_story_id=story.id,
    )
    store.update_change_request_status(done.id, "done", completed_at="2026-06-26T00:00:00Z")
    store.update_change_request_status(planned.id, "planned")

    overview = get_refinement_story_overview(
        store,
        journey="mirror",
        refinement_story_id=story.id,
    )
    rendered = render_refinement_story_overview_surface(journey="mirror", overview=overview)

    assert overview.change_requests == (
        store.get_change_request(done.id),
        captured,
        store.get_change_request(planned.id),
    )
    assert "<<<ARIAD:REFINEMENT_STORY_OVERVIEW>>>" in rendered
    assert "Refinement Work" in rendered
    assert "RS Flow:" not in rendered
    assert "CR Cycle:" not in rendered
    assert "journey" not in rendered
    assert "refinement story" not in rendered
    assert "status" not in rendered
    assert "available next moves" not in rendered
    assert "boundary" not in rendered
    assert "Builder lifecycle refinement" in rendered
    assert "change requests (#3)" in rendered
    assert "🟦 CR003: Use display codes [planned]" in rendered
    assert "🟨 CR002: Roadmap after Done [captured]" in rendered
    assert "🟩 CR001: Plan safety [done]" in rendered
    assert rendered.index("CR003") < rendered.index("CR002") < rendered.index("CR001")


def test_change_request_captured_surface_shows_full_body_and_compact_refs(store):
    story = create_refinement_story(store, journey="mirror", title="Builder lifecycle refinement")
    body = (
        "Preserve human-authored plan details. This long body should be rendered in full, "
        "without truncation, because the captured card is where the requested change becomes visible."
    )
    change_request = capture_change_request(
        store,
        journey="mirror",
        title="Plan safety",
        body=body,
        refinement_story_id=story.id,
        source="dogfood",
    )

    rendered = render_change_request_captured_surface(
        journey="mirror",
        change_request=change_request,
        refinement_story=story,
    )

    assert "<<<ARIAD:CHANGE_REQUEST_CAPTURED>>>" in rendered
    assert "Refinement Work" in rendered
    assert "RS Flow:" not in rendered
    assert "CR Cycle:" not in rendered
    assert "CR001: Plan safety" in rendered
    assert "Requested change" in rendered
    assert "Preserve human-authored plan details." in rendered
    assert "without truncation" in rendered
    assert "Refinement Story" in rendered
    assert "RS001: Builder lifecycle refinement" in rendered
    assert "journey" not in rendered
    assert "status" not in rendered
    assert "source" not in rendered
    assert "boundary" not in rendered
    assert "dogfood" not in rendered
    assert story.id not in rendered
    assert change_request.id not in rendered
