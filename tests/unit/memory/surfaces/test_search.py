from memory.surfaces.search import SearchSurface


def test_search_surface_exposes_stable_empty_contract() -> None:
    results = SearchSurface().search("identity", perspective="atlas")

    assert results.query == "identity"
    assert results.perspective == "atlas"
    assert results.results == ()
    assert results.empty_state == "Search is not wired into the web surface yet."


def test_search_surface_finds_recent_memories_lexically(
    memory_service, mock_memory_embedding
) -> None:
    match = memory_service.add_memory(
        title="Surface boundary",
        content="Web renders surfaces.",
        memory_type="decision",
    )
    memory_service.add_memory(title="Other idea", content="Later.", memory_type="idea")

    results = SearchSurface(memories=memory_service).search("surface web")

    assert results.query == "surface web"
    assert results.empty_state is None
    assert len(results.results) == 1
    assert results.results[0].id == match.id
    assert results.results[0].title == "Surface boundary"


def test_search_surface_reports_empty_query(memory_service) -> None:
    results = SearchSurface(memories=memory_service).search("   ")

    assert results.query == ""
    assert results.results == ()
    assert results.empty_state == "Type a search term to search recent retained memories."


def test_search_surface_lists_recent_memories_by_category(
    memory_service, mock_memory_embedding
) -> None:
    decision = memory_service.add_memory(
        title="Choose surface boundary",
        content="Web renders surfaces.",
        memory_type="decision",
    )
    memory_service.add_memory(title="Draft idea", content="Later.", memory_type="idea")

    results = SearchSurface(memories=memory_service).memory_category("decisions")

    assert results.query == "Decisions"
    assert results.perspective == "memories"
    assert results.empty_state is None
    assert len(results.results) == 1
    assert results.results[0].id == decision.id
    assert results.results[0].title == "Choose surface boundary"
    assert results.results[0].metadata["icon"] == "◉"
    assert results.results[0].metadata["memory_type"] == "decision"


def test_search_surface_prefers_persona_icon_when_memory_has_persona(
    memory_service, mock_memory_embedding
) -> None:
    memory_service.add_memory(
        title="Product tracer bullet",
        content="Input trivial, hidden complexity.",
        memory_type="idea",
        layer="ego",
        persona="product-designer",
    )

    results = SearchSurface(memories=memory_service).search("tracer")

    assert results.results[0].metadata["icon"] == "✣"
    assert results.results[0].metadata["layer"] == "ego"
    assert results.results[0].metadata["persona"] == "product-designer"


def test_search_surface_reports_empty_memory_category(memory_service) -> None:
    results = SearchSurface(memories=memory_service).memory_category("patterns")

    assert results.query == "Patterns"
    assert results.results == ()
    assert results.empty_state == "No recent patterns memories are available yet."
