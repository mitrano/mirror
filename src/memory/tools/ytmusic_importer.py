"""Proof-of-viability YouTube Music playlist importer.

This module intentionally keeps the YouTube Music dependency behind a small
adapter. The pure planning code is testable without network access; the live
adapter is only created when the CLI is run against a real account.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


@dataclass(frozen=True)
class SongRequest:
    raw: str
    query: str
    artist: str | None = None
    title: str | None = None


@dataclass(frozen=True)
class SongMatch:
    request: SongRequest
    title: str
    artists: tuple[str, ...]
    video_id: str
    confidence: str

    @property
    def label(self) -> str:
        artists = ", ".join(self.artists) if self.artists else "unknown artist"
        return f"{self.title} — {artists} ({self.video_id})"


@dataclass(frozen=True)
class ImportPlan:
    playlist_title: str
    playlist_id: str | None
    playlist_created: bool
    matches: tuple[SongMatch, ...]
    ambiguous: tuple[tuple[SongRequest, tuple[SongMatch, ...]], ...]
    not_found: tuple[SongRequest, ...]
    duplicate_video_ids: tuple[str, ...]

    @property
    def video_ids_to_add(self) -> tuple[str, ...]:
        duplicate_ids = set(self.duplicate_video_ids)
        return tuple(match.video_id for match in self.matches if match.video_id not in duplicate_ids)


class YouTubeMusicClient(Protocol):
    def search_songs(self, query: str, limit: int) -> Sequence[dict[str, Any]]: ...

    def find_playlist(self, title: str) -> dict[str, Any] | None: ...

    def create_playlist(self, title: str, description: str) -> str: ...

    def get_playlist_video_ids(self, playlist_id: str) -> set[str]: ...

    def add_playlist_items(self, playlist_id: str, video_ids: Sequence[str]) -> None: ...


def parse_song_line(line: str) -> SongRequest | None:
    """Parse one user-provided song line.

    Supported input is deliberately permissive for the PoC:
    - ``Artist - Title``
    - common Unicode dash variants between artist and title
    - ``Title`` / arbitrary search query
    Blank lines and ``#`` comments are ignored.
    """
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    for separator in (" - ", f" {chr(8211)} ", f" {chr(8212)} "):
        if separator in stripped:
            artist, title = stripped.split(separator, 1)
            artist = artist.strip()
            title = title.strip()
            if artist and title:
                return SongRequest(raw=stripped, query=f"{artist} {title}", artist=artist, title=title)

    return SongRequest(raw=stripped, query=stripped)


def load_song_requests(path: Path) -> tuple[SongRequest, ...]:
    requests = [parsed for line in path.read_text(encoding="utf-8").splitlines() if (parsed := parse_song_line(line))]
    if not requests:
        raise ValueError(f"No songs found in {path}")
    return tuple(requests)


def _extract_artists(result: dict[str, Any]) -> tuple[str, ...]:
    artists = result.get("artists") or []
    names: list[str] = []
    for artist in artists:
        if isinstance(artist, dict) and artist.get("name"):
            names.append(str(artist["name"]))
        elif isinstance(artist, str):
            names.append(artist)
    return tuple(names)


def _to_match(request: SongRequest, result: dict[str, Any], confidence: str) -> SongMatch | None:
    video_id = result.get("videoId")
    title = result.get("title")
    if not video_id or not title:
        return None
    return SongMatch(
        request=request,
        title=str(title),
        artists=_extract_artists(result),
        video_id=str(video_id),
        confidence=confidence,
    )


def choose_matches(
    client: YouTubeMusicClient,
    requests: Sequence[SongRequest],
    *,
    playlist_title: str,
    search_limit: int = 3,
    create_missing_playlist: bool = True,
    playlist_description: str = "Created by Mirror Mind YouTube Music Importer PoC.",
) -> ImportPlan:
    playlist = client.find_playlist(playlist_title)
    playlist_id = None
    playlist_created = False
    if playlist is not None:
        raw_playlist_id = playlist.get("playlistId") or playlist.get("id")
        playlist_id = str(raw_playlist_id) if raw_playlist_id else None
    elif create_missing_playlist:
        playlist_id = client.create_playlist(playlist_title, playlist_description)
        playlist_created = True

    existing_video_ids = client.get_playlist_video_ids(playlist_id) if playlist_id else set()
    matches: list[SongMatch] = []
    ambiguous: list[tuple[SongRequest, tuple[SongMatch, ...]]] = []
    not_found: list[SongRequest] = []

    for request in requests:
        raw_results = list(client.search_songs(request.query, limit=search_limit))
        candidates = tuple(
            match
            for result in raw_results
            if (match := _to_match(request, result, confidence="top")) is not None
        )
        if not candidates:
            not_found.append(request)
            continue
        if len(candidates) > 1:
            ambiguous.append((request, candidates))
        matches.append(candidates[0])

    duplicate_ids = tuple(match.video_id for match in matches if match.video_id in existing_video_ids)
    return ImportPlan(
        playlist_title=playlist_title,
        playlist_id=playlist_id,
        playlist_created=playlist_created,
        matches=tuple(matches),
        ambiguous=tuple(ambiguous),
        not_found=tuple(not_found),
        duplicate_video_ids=duplicate_ids,
    )


class YTMusicApiClient:
    def __init__(self, auth_path: Path) -> None:
        try:
            from ytmusicapi import YTMusic  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover - exercised manually
            raise RuntimeError(
                "ytmusicapi is not installed. Install the optional dependency with: "
                "uv pip install ytmusicapi"
            ) from exc
        self._ytmusic = YTMusic(str(auth_path))

    def search_songs(self, query: str, limit: int) -> Sequence[dict[str, Any]]:
        return self._ytmusic.search(query, filter="songs", limit=limit)

    def find_playlist(self, title: str) -> dict[str, Any] | None:
        target = title.casefold().strip()
        playlists = self._ytmusic.get_library_playlists(limit=100)
        for playlist in playlists:
            if str(playlist.get("title", "")).casefold().strip() == target:
                return playlist
        return None

    def create_playlist(self, title: str, description: str) -> str:
        return str(self._ytmusic.create_playlist(title, description))

    def get_playlist_video_ids(self, playlist_id: str) -> set[str]:
        playlist = self._ytmusic.get_playlist(playlist_id, limit=None)
        tracks = playlist.get("tracks") or []
        return {str(track["videoId"]) for track in tracks if track.get("videoId")}

    def add_playlist_items(self, playlist_id: str, video_ids: Sequence[str]) -> None:
        if video_ids:
            self._ytmusic.add_playlist_items(playlist_id, list(video_ids), duplicates=False)


def render_plan(plan: ImportPlan, *, applied: bool) -> str:
    lines: list[str] = []
    state = "APPLIED" if applied else "DRY RUN"
    lines.append(f"YouTube Music Importer PoC — {state}")
    lines.append(f"Playlist: {plan.playlist_title}")
    lines.append(f"Playlist id: {plan.playlist_id or '(not created/found)'}")
    lines.append(f"Playlist created: {'yes' if plan.playlist_created else 'no'}")
    lines.append("")
    lines.append(f"Matched: {len(plan.matches)}")
    for index, match in enumerate(plan.matches, start=1):
        duplicate = " [duplicate]" if match.video_id in plan.duplicate_video_ids else ""
        lines.append(f"  {index}. {match.request.raw} -> {match.label}{duplicate}")
    lines.append("")
    lines.append(f"To add: {len(plan.video_ids_to_add)}")
    lines.append(f"Ambiguous: {len(plan.ambiguous)}")
    for request, candidates in plan.ambiguous:
        labels = "; ".join(candidate.label for candidate in candidates)
        lines.append(f"  - {request.raw}: {labels}")
    lines.append(f"Not found: {len(plan.not_found)}")
    for request in plan.not_found:
        lines.append(f"  - {request.raw}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import a text song list into a YouTube Music playlist.")
    parser.add_argument("--songs", required=True, type=Path, help="UTF-8 text file with one song per line")
    parser.add_argument("--playlist", required=True, help="Playlist title to find or create")
    parser.add_argument("--auth", required=True, type=Path, help="ytmusicapi browser headers auth file")
    parser.add_argument("--search-limit", type=int, default=3, help="candidate results per song")
    parser.add_argument("--apply", action="store_true", help="actually create/update the playlist")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    requests = load_song_requests(args.songs)
    client = YTMusicApiClient(args.auth)
    plan = choose_matches(
        client,
        requests,
        playlist_title=args.playlist,
        search_limit=args.search_limit,
        create_missing_playlist=args.apply,
    )
    if args.apply:
        if not plan.playlist_id:
            print("Cannot apply: playlist was not found or created", file=sys.stderr)
            return 2
        client.add_playlist_items(plan.playlist_id, plan.video_ids_to_add)
    print(render_plan(plan, applied=args.apply))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
