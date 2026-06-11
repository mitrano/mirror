from memory.builder.ariad_method import ARIAD_METHOD, get_ariad_method
from memory.builder.method_definition import validate_method_definition


def test_ariad_method_fixture_is_valid() -> None:
    validate_method_definition(ARIAD_METHOD)
    validate_method_definition(get_ariad_method())


def test_ariad_method_identity_and_resolution_layers() -> None:
    method = get_ariad_method()

    assert method.id == "ariad"
    assert method.label == "Ariad"
    assert method.resolution.layers == (
        "method_default",
        "project_config",
        "journey_config",
        "navigator_override",
    )
    assert method.resolution.conflict_policy == "explicit_override"
    assert method.resolution.audit is True


def test_ariad_taxonomy_contains_expected_levels_and_state_semantics() -> None:
    method = get_ariad_method()
    levels = {level.id: level for level in method.taxonomy.levels}

    assert set(levels) == {"cv", "delivery_story", "user_story", "technical_story", "task"}
    assert levels["cv"].contains == ("delivery_story",)
    assert levels["delivery_story"].contains == ("user_story", "technical_story")
    assert levels["user_story"].contains == ("task",)
    assert levels["technical_story"].contains == ("task",)
    assert levels["user_story"].state_semantics
    assert "observable behavior" in levels["user_story"].state_semantics["Validated"]
    assert levels["technical_story"].state_semantics
    assert "internal capability" in levels["technical_story"].state_semantics["Validated"]


def test_ariad_lifecycle_matches_exploration_spine() -> None:
    method = get_ariad_method()

    assert [(event.id, event.meaning) for event in method.lifecycle] == [
        ("pull", "escolhe o foco"),
        ("prepare", "lê o terreno"),
        ("plan", "firma o contrato"),
        ("implement", "muda o sistema"),
        ("validation", "prova comportamento"),
        ("review", "encara a dívida"),
        ("coherence", "integra os rastros"),
        ("done", "registra e fecha"),
    ]


def test_after_plan_checkpoint_blocks_implement_until_approval() -> None:
    method = get_ariad_method()
    checkpoints = {checkpoint.id: checkpoint for checkpoint in method.checkpoints}

    after_plan = checkpoints["after_plan"]
    assert after_plan.occurs_after == "plan"
    assert after_plan.blocks == ("implement",)
    assert after_plan.required_artifacts == ("plan",)
    assert after_plan.required_confirmations == ("navigator_approval",)


def test_ariad_policies_capture_history_push_and_release() -> None:
    method = get_ariad_method()
    policies = method.policies or {}

    assert policies["history"]["commit"]["mode"] == "propose_and_wait"
    assert policies["history"]["commit"]["granularity"] == "coherent_story"
    assert policies["push"]["mode"] == "ask_before_push"
    assert "release_publish" in policies["push"]["allowed_after"]
    assert policies["release"]["modes"] == ["planned_release", "emergent_release"]


def test_ariad_declares_adoption_templates_as_method_data() -> None:
    method = get_ariad_method()
    templates = {template.id: template for template in method.templates}

    assert set(templates) == {
        "ariad_adoption",
        "technical_debt_ledger",
        "delivery_story_index",
        "user_story_index",
        "technical_story_index",
        "plan",
        "test_guide",
        "review",
        "coherence",
    }
    assert templates["plan"].path == "docs/project/roadmap/templates/plan.md"
    assert "Implementation must not start" in templates["plan"].content
    assert templates["technical_debt_ledger"].path == (
        "docs/project/roadmap/technical-debt-ledger.md"
    )
    assert "Navigator Decision" in templates["technical_debt_ledger"].content


def test_ariad_surfaces_bind_to_lifecycle_and_entrypoint_events() -> None:
    method = get_ariad_method()
    surfaces = {surface.id: surface for surface in method.surfaces}

    assert surfaces["adoption_report"].event == "adoption"
    assert surfaces["builder_resume"].event == "on_builder_load"
    assert surfaces["plan_checkpoint"].event == "plan"
    assert surfaces["plan_checkpoint"].stops_for == "navigator_approval"
    assert surfaces["validation_checkpoint"].event == "validation"
    assert surfaces["review_checkpoint"].event == "review"


def test_ariad_open_questions_preserve_deferred_design_areas() -> None:
    method = get_ariad_method()
    open_questions = method.open_questions or {}

    assert open_questions["maintenance_and_operational_updates"]["status"] == "open"
    assert open_questions["final_surface_content"]["status"] == "open"
    assert open_questions["final_dsl_file_format"]["status"] == "open"
