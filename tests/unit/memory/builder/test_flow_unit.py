from memory import MemoryClient
from memory.builder.delivery_cursor import set_delivery_cursor
from memory.builder.flow_unit import (
    FLOW_UNIT_DELIVERY_STORY,
    FLOW_UNIT_STORY_BY_STORY,
    inspect_navigator_flow_unit,
    render_navigator_flow_unit_report,
    set_navigator_flow_unit,
)
from memory.config import default_db_path_for_home


def _store(tmp_path):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    client = MemoryClient(env="test", db_path=db_path)
    return client, client.store


def test_navigator_flow_unit_defaults_to_story_by_story(tmp_path):
    _client, store = _store(tmp_path)
    set_delivery_cursor(
        store,
        journey="sandbox-pet-store",
        method="ariad",
        active_item="CV20.DS5",
        active_item_title="Delivery Story Level Lifecycle",
        active_item_level="delivery_story",
    )

    report = inspect_navigator_flow_unit(store, journey="sandbox-pet-store", method="ariad")

    assert report.flow_unit == FLOW_UNIT_STORY_BY_STORY
    assert report.source == "default"


def test_set_navigator_flow_unit_persists_delivery_story_choice(tmp_path):
    _client, store = _store(tmp_path)
    set_delivery_cursor(
        store,
        journey="sandbox-pet-store",
        method="ariad",
        active_item="CV20.DS5",
        active_item_title="Delivery Story Level Lifecycle",
        active_item_level="delivery_story",
    )

    report = set_navigator_flow_unit(
        store,
        journey="sandbox-pet-store",
        method="ariad",
        flow_unit=FLOW_UNIT_DELIVERY_STORY,
    )
    inspected = inspect_navigator_flow_unit(store, journey="sandbox-pet-store", method="ariad")

    assert report.flow_unit == FLOW_UNIT_DELIVERY_STORY
    assert inspected.flow_unit == FLOW_UNIT_DELIVERY_STORY
    assert inspected.source == "cursor"
    assert inspected.cursor.last_delivery_event == "navigator_flow_unit_selected"


def test_render_navigator_flow_unit_report_declares_choices_and_boundary(tmp_path):
    _client, store = _store(tmp_path)
    set_delivery_cursor(store, journey="sandbox-pet-store", method="ariad")
    report = inspect_navigator_flow_unit(store, journey="sandbox-pet-store", method="ariad")

    rendered = render_navigator_flow_unit_report(report)

    assert "<<<ARIAD:NAVIGATOR_FLOW_UNIT>>>" in rendered
    assert "effective flow unit\nstory_by_story" in rendered
    assert "delivery_story: parent Delivery Story becomes" in rendered
    assert "No Plan, implementation, validation, push, or release work was executed" in rendered
