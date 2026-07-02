import pytest

from memory.builder.lifecycle_ribbon import (
    render_change_request_lifecycle_ribbon,
    render_lifecycle_ribbon,
    render_refinement_lifecycle_ribbon,
)


def test_render_lifecycle_ribbon_marks_current_and_future_stages():
    rendered = render_lifecycle_ribbon("pull")

    assert rendered == (
        "Delivery Flow: ◉ Pull → ○ Prepare → ○ Expand → ○ Plan → ○ Implement → "
        "○ Validate → ○ Debt Review → ○ Done"
    )


def test_render_lifecycle_ribbon_marks_previous_stages_done():
    rendered = render_lifecycle_ribbon("prepare")

    assert rendered == (
        "Delivery Flow: ✓ Pull → ◉ Prepare → ○ Expand → ○ Plan → ○ Implement → "
        "○ Validate → ○ Debt Review → ○ Done"
    )


def test_render_refinement_lifecycle_ribbon_uses_rs_flow_copy_and_arrows():
    rendered = render_refinement_lifecycle_ribbon("pull")

    assert (
        rendered == "RS Flow: ◉ Pull → ○ Select CR → ○ CR Cycle → ○ Review → ○ Coherence → ○ Close"
    )


def test_render_refinement_lifecycle_ribbon_marks_review_phase():
    rendered = render_refinement_lifecycle_ribbon("review")

    assert (
        rendered == "RS Flow: ✓ Pull → ✓ Select CR → ✓ CR Cycle → ◉ Review → ○ Coherence → ○ Close"
    )


def test_render_change_request_lifecycle_ribbon_uses_cr_cycle_copy_and_arrows():
    rendered = render_change_request_lifecycle_ribbon("implement")

    assert rendered == "CR Cycle: ✓ Confirm → ✓ Plan → ◉ Implement → ○ Validate → ○ Done Note"


def test_render_lifecycle_ribbon_rejects_unknown_stage():
    with pytest.raises(ValueError, match="unknown Ariad lifecycle stage"):
        render_lifecycle_ribbon("commit")
