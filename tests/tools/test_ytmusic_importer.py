from pathlib import Path

from memory.tools.ytmusic_importer import (
    SongRequest,
    choose_matches,
    load_song_requests,
    parse_song_line,
    render_plan,
)


class FakeYouTubeMusicClient:
    def __init__(self) -> None:
        self.created_playlists: list[str] = []
        self.added: list[tuple[str, tuple[str, ...]]] = []
        self.playlists: dict[str, dict[str, str]] = {}
        self.playlist_tracks: dict[str, set[str]] = {}
        self.search_index: dict[str, list[dict[str, object]]] = {}

    def search_songs(self, query: str, limit: int) -> list[dict[str, object]]:
        return self.search_index.get(query, [])[:limit]

    def find_playlist(self, title: str) -> dict[str, str] | None:
        return self.playlists.get(title.casefold())

    def create_playlist(self, title: str, description: str) -> str:
        playlist_id = f"playlist-{len(self.created_playlists) + 1}"
        self.created_playlists.append(title)
        self.playlists[title.casefold()] = {"title": title, "playlistId": playlist_id}
        self.playlist_tracks[playlist_id] = set()
        return playlist_id

    def get_playlist_video_ids(self, playlist_id: str) -> set[str]:
        return self.playlist_tracks.get(playlist_id, set())

    def add_playlist_items(self, playlist_id: str, video_ids: list[str]) -> None:
        self.added.append((playlist_id, tuple(video_ids)))


def test_parse_song_line_accepts_artist_dash_title() -> None:
    request = parse_song_line("Radiohead - Weird Fishes")

    assert request == SongRequest(
        raw="Radiohead - Weird Fishes",
        query="Radiohead Weird Fishes",
        artist="Radiohead",
        title="Weird Fishes",
    )


def test_parse_song_line_ignores_blank_and_comment_lines() -> None:
    assert parse_song_line("   ") is None
    assert parse_song_line("# comment") is None


def test_load_song_requests_reads_utf8_file(tmp_path: Path) -> None:
    songs = tmp_path / "songs.txt"
    songs.write_text("Milton Nascimento - Cais\n\nAphex Twin - Xtal\n", encoding="utf-8")

    requests = load_song_requests(songs)

    assert [request.raw for request in requests] == ["Milton Nascimento - Cais", "Aphex Twin - Xtal"]


def test_choose_matches_creates_missing_playlist_and_reports_duplicate() -> None:
    client = FakeYouTubeMusicClient()
    client.search_index = {
        "Radiohead Weird Fishes": [
            {
                "title": "Weird Fishes/ Arpeggi",
                "videoId": "radiohead-1",
                "artists": [{"name": "Radiohead"}],
            }
        ],
        "Milton Nascimento Cais": [
            {
                "title": "Cais",
                "videoId": "milton-1",
                "artists": [{"name": "Milton Nascimento"}],
            }
        ],
    }

    plan = choose_matches(
        client,
        [
            SongRequest("Radiohead - Weird Fishes", "Radiohead Weird Fishes"),
            SongRequest("Milton Nascimento - Cais", "Milton Nascimento Cais"),
        ],
        playlist_title="Mirror Test",
    )

    assert plan.playlist_id == "playlist-1"
    assert plan.playlist_created is True
    assert [match.video_id for match in plan.matches] == ["radiohead-1", "milton-1"]
    assert plan.video_ids_to_add == ("radiohead-1", "milton-1")


def test_choose_matches_tracks_ambiguous_and_not_found_without_losing_top_match() -> None:
    client = FakeYouTubeMusicClient()
    client.playlists["mirror test"] = {"title": "Mirror Test", "playlistId": "existing"}
    client.playlist_tracks["existing"] = {"xtal-1"}
    client.search_index = {
        "Aphex Twin Xtal": [
            {"title": "Xtal", "videoId": "xtal-1", "artists": [{"name": "Aphex Twin"}]},
            {"title": "Xtal Remastered", "videoId": "xtal-2", "artists": [{"name": "Aphex Twin"}]},
        ],
    }

    plan = choose_matches(
        client,
        [
            SongRequest("Aphex Twin - Xtal", "Aphex Twin Xtal"),
            SongRequest("Unknown - Missing", "Unknown Missing"),
        ],
        playlist_title="Mirror Test",
    )

    assert plan.playlist_created is False
    assert plan.playlist_id == "existing"
    assert len(plan.matches) == 1
    assert len(plan.ambiguous) == 1
    assert [request.raw for request in plan.not_found] == ["Unknown - Missing"]
    assert plan.duplicate_video_ids == ("xtal-1",)
    assert plan.video_ids_to_add == ()


def test_render_plan_makes_dry_run_state_and_counts_visible() -> None:
    client = FakeYouTubeMusicClient()
    client.playlists["mirror test"] = {"title": "Mirror Test", "playlistId": "existing"}
    client.search_index = {
        "Radiohead Weird Fishes": [
            {"title": "Weird Fishes/ Arpeggi", "videoId": "radiohead-1", "artists": [{"name": "Radiohead"}]}
        ]
    }
    plan = choose_matches(
        client,
        [SongRequest("Radiohead - Weird Fishes", "Radiohead Weird Fishes")],
        playlist_title="Mirror Test",
    )

    rendered = render_plan(plan, applied=False)

    assert "YouTube Music Importer PoC — DRY RUN" in rendered
    assert "Matched: 1" in rendered
    assert "To add: 1" in rendered
