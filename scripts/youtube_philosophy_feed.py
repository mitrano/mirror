#!/usr/bin/env python3
"""Generate a YouTube-like HTML feed of philosophy videos from subscriptions.

Requires OAuth because YouTube subscriptions are private account data.

Run with:
  uv run --with google-api-python-client --with google-auth-oauthlib \
    python scripts/youtube_philosophy_feed.py \
      --client-secrets .local/youtube_client_secret.json \
      --output exports/youtube_filosofia_24h.html
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
BOILERPLATE_PATTERNS = [
    # Evita falso positivo de "ética" em descrições padrão médicas/jurídicas/publicitárias.
    r"c[oó]digo de [eé]tica(?: m[eé]dica)?",
    r"[eé]tica m[eé]dica",
    r"publicidade (?:do )?c[oó]digo de [eé]tica",
    r"resolu[cç][aã]o cfm\s*\d+[/.-]\d+",
    r"conselho federal de medicina",
    r"car[aá]ter de presta[cç][aã]o de informa[cç][oõ]es",
]

DEFAULT_KEYWORDS = [
    "filosofia",
    "philosophy",
    "filósofo",
    "filosófico",
    "philosophical",
    "ética",
    "ethics",
    "metafísica",
    "metaphysics",
    "epistemologia",
    "epistemology",
    "estoicismo",
    "stoicism",
    "sócrates",
    "socrates",
    "platão",
    "plato",
    "aristóteles",
    "aristotle",
    "nietzsche",
    "kant",
    "hegel",
    "spinoza",
    "descartes",
    "foucault",
    "deleuze",
    "camus",
    "sartre",
    "heidegger",
]


@dataclass(frozen=True)
class Video:
    video_id: str
    title: str
    channel_title: str
    published_at: datetime
    url: str
    thumbnail: str
    description: str
    duration_seconds: int = 0


def parse_rfc3339(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def parse_iso8601_duration(value: str) -> int:
    match = re.fullmatch(
        r"P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?",
        value,
    )
    if not match:
        return 0
    parts = {key: int(val or 0) for key, val in match.groupdict().items()}
    return (
        parts["days"] * 86400
        + parts["hours"] * 3600
        + parts["minutes"] * 60
        + parts["seconds"]
    )


def format_duration(seconds: int) -> str:
    if seconds <= 0:
        return "duração indisponível"
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def get_youtube_service(
    client_secrets: Path,
    token_path: Path,
    auth_port: int,
    auth_timeout_seconds: int,
    open_browser: bool,
) -> Any:
    creds: Credentials | None = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_info(json.loads(token_path.read_text()), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), SCOPES)
            creds = flow.run_local_server(
                port=auth_port,
                open_browser=open_browser,
                timeout_seconds=auth_timeout_seconds,
                authorization_prompt_message=(
                    "Abra esta URL no navegador, autorize o acesso e aguarde o retorno para o terminal:\n{url}\n"
                ),
            )
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def list_subscribed_channels(youtube: Any) -> list[dict[str, str]]:
    channels: list[dict[str, str]] = []
    page_token: str | None = None
    while True:
        response = (
            youtube.subscriptions()
            .list(part="snippet", mine=True, maxResults=50, pageToken=page_token)
            .execute()
        )
        for item in response.get("items", []):
            snippet = item["snippet"]
            resource = snippet["resourceId"]
            channels.append({"id": resource["channelId"], "title": snippet.get("title", "")})
        page_token = response.get("nextPageToken")
        if not page_token:
            return channels


def get_upload_playlists(youtube: Any, channel_ids: list[str]) -> dict[str, str]:
    playlists: dict[str, str] = {}
    for start in range(0, len(channel_ids), 50):
        batch = channel_ids[start : start + 50]
        response = (
            youtube.channels()
            .list(part="contentDetails", id=",".join(batch), maxResults=50)
            .execute()
        )
        for item in response.get("items", []):
            uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]
            playlists[item["id"]] = uploads
    return playlists


def text_matches(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    for pattern in BOILERPLATE_PATTERNS:
        lowered = re.sub(pattern, " ", lowered, flags=re.IGNORECASE)
    return any(keyword.lower() in lowered for keyword in keywords)


def list_recent_philosophy_videos(
    youtube: Any,
    playlists: dict[str, str],
    published_after: datetime,
    keywords: list[str],
    pages_per_channel: int,
) -> list[Video]:
    videos: list[Video] = []
    for playlist_id in playlists.values():
        page_token: str | None = None
        pages = 0
        stop_channel = False
        while not stop_channel and pages < pages_per_channel:
            pages += 1
            try:
                response = (
                    youtube.playlistItems()
                    .list(
                        part="snippet,contentDetails",
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken=page_token,
                    )
                    .execute()
                )
            except HttpError as error:
                if getattr(error, "status_code", None) == 404 or "playlistNotFound" in str(error):
                    print(f"Aviso: playlist de uploads indisponível; pulando {playlist_id}")
                    break
                raise
            for item in response.get("items", []):
                snippet = item.get("snippet", {})
                published_at_raw = snippet.get("publishedAt")
                if not published_at_raw:
                    continue
                published_at = parse_rfc3339(published_at_raw)
                if published_at < published_after:
                    stop_channel = True
                    break

                video_id = item.get("contentDetails", {}).get("videoId")
                if not video_id:
                    continue

                title = snippet.get("title", "")
                channel_title = snippet.get("channelTitle", "")
                description = snippet.get("description", "")
                searchable = f"{title}\n{channel_title}\n{description}"
                if not text_matches(searchable, keywords):
                    continue

                thumbnails = snippet.get("thumbnails", {})
                thumbnail = (
                    thumbnails.get("medium")
                    or thumbnails.get("high")
                    or thumbnails.get("default")
                    or {}
                ).get("url", "")
                videos.append(
                    Video(
                        video_id=video_id,
                        title=title,
                        channel_title=channel_title,
                        published_at=published_at,
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        thumbnail=thumbnail,
                        description=description,
                    )
                )
            page_token = response.get("nextPageToken")
            if not page_token:
                break
    return sorted(videos, key=lambda video: video.published_at)


def add_video_durations(youtube: Any, videos: list[Video]) -> list[Video]:
    durations: dict[str, int] = {}
    for start in range(0, len(videos), 50):
        batch = videos[start : start + 50]
        response = (
            youtube.videos()
            .list(part="contentDetails", id=",".join(video.video_id for video in batch), maxResults=50)
            .execute()
        )
        for item in response.get("items", []):
            durations[item["id"]] = parse_iso8601_duration(
                item.get("contentDetails", {}).get("duration", "")
            )
    return [replace(video, duration_seconds=durations.get(video.video_id, 0)) for video in videos]


def render_html(videos: list[Video], generated_at: datetime, published_after: datetime) -> str:
    rows = []
    for video in videos:
        description = " ".join(video.description.split())[:220]
        published = video.published_at.astimezone().strftime("%d/%m/%Y %H:%M")
        duration = format_duration(video.duration_seconds)
        rows.append(
            f"""
            <article class="video-card">
              <a class="thumb" href="{html.escape(video.url)}" target="_blank" rel="noopener">
                <img src="{html.escape(video.thumbnail)}" alt="" loading="lazy">
              </a>
              <div class="meta">
                <a class="title" href="{html.escape(video.url)}" target="_blank" rel="noopener">{html.escape(video.title)}</a>
                <div class="channel">{html.escape(video.channel_title)}</div>
                <div class="date">Publicado em {html.escape(published)} · duração: {html.escape(duration)}</div>
                <p>{html.escape(description)}</p>
              </div>
            </article>
            """
        )

    body = "\n".join(rows) if rows else "<p class='empty'>Nenhum vídeo de filosofia encontrado nas últimas 24 horas.</p>"
    video_links = "\n".join(html.escape(video.url) for video in videos)
    unique_channels = sorted({video.channel_title for video in videos}, key=str.casefold)
    channel_items = "\n".join(
        f"<li>{html.escape(channel)}</li>" for channel in unique_channels
    ) or "<li>Nenhum canal encontrado.</li>"
    generated = generated_at.astimezone().strftime("%d/%m/%Y %H:%M")
    since = published_after.astimezone().strftime("%d/%m/%Y %H:%M")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Feed YouTube — Filosofia 24h</title>
  <style>
    :root {{ color-scheme: dark; --bg:#0f0f0f; --panel:#181818; --text:#f1f1f1; --muted:#aaa; --line:#303030; --red:#ff0033; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:Roboto, Arial, sans-serif; }}
    header {{ position:sticky; top:0; z-index:2; display:flex; align-items:center; gap:16px; padding:14px 24px; background:#0f0f0fe8; border-bottom:1px solid var(--line); backdrop-filter: blur(8px); }}
    .logo {{ width:34px; height:24px; background:var(--red); border-radius:7px; display:grid; place-items:center; color:white; font-weight:900; }}
    h1 {{ font-size:20px; margin:0; }}
    .sub {{ color:var(--muted); font-size:13px; margin-top:3px; }}
    main {{ width:min(1120px, 100%); margin:0 auto; padding:24px; }}
    .video-card {{ display:grid; grid-template-columns: 280px 1fr; gap:16px; padding:14px 0; border-bottom:1px solid var(--line); }}
    .thumb {{ display:block; aspect-ratio:16/9; background:#222; border-radius:12px; overflow:hidden; }}
    .thumb img {{ width:100%; height:100%; object-fit:cover; display:block; }}
    .title {{ color:var(--text); text-decoration:none; font-size:18px; font-weight:700; line-height:1.25; }}
    .title:hover {{ color:white; text-decoration:underline; }}
    .channel, .date, p {{ color:var(--muted); font-size:14px; }}
    .channel {{ margin-top:8px; }}
    .date {{ margin-top:3px; }}
    p {{ line-height:1.4; margin:10px 0 0; }}
    .copy-section {{ margin-top:34px; padding:22px; background:var(--panel); border:1px solid var(--line); border-radius:14px; }}
    .copy-section h2 {{ font-size:18px; margin:0 0 12px; }}
    .copy-section .hint {{ color:var(--muted); font-size:13px; margin:0 0 12px; }}
    .link-box {{ width:100%; min-height:180px; resize:vertical; padding:14px; border-radius:10px; border:1px solid var(--line); background:#0b0b0b; color:var(--text); font:14px/1.45 monospace; }}
    .channel-list {{ margin:0; padding-left:22px; color:var(--text); line-height:1.7; }}
    .empty {{ padding:40px; text-align:center; background:var(--panel); border-radius:14px; }}
    @media (max-width: 720px) {{ main {{ padding:12px; }} .video-card {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header>
    <div class="logo">▶</div>
    <div>
      <h1>Filosofia nas suas inscrições</h1>
      <div class="sub">Últimas 24h desde {html.escape(since)} · gerado em {html.escape(generated)} · ordenado por duração, do menor para o maior</div>
    </div>
  </header>
  <main>
    {body}

    <section class="copy-section">
      <h2>Links dos vídeos para copiar</h2>
      <p class="hint">Um link por linha, na mesma ordem do feed: do vídeo mais curto para o mais longo.</p>
      <textarea class="link-box" readonly>{video_links}</textarea>
    </section>

    <section class="copy-section">
      <h2>Canais presentes neste feed</h2>
      <p class="hint">Lista única dos canais, sem repetição.</p>
      <ul class="channel-list">
        {channel_items}
      </ul>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-secrets", type=Path, required=True)
    parser.add_argument("--token", type=Path, default=Path(".local/youtube_token.json"))
    parser.add_argument("--output", type=Path, default=Path("exports/youtube_filosofia_24h.html"))
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--pages-per-channel", type=int, default=2)
    parser.add_argument("--min-duration-seconds", type=int, default=30)
    parser.add_argument("--keywords", nargs="*", default=DEFAULT_KEYWORDS)
    parser.add_argument("--auth-port", type=int, default=8080)
    parser.add_argument("--auth-timeout-seconds", type=int, default=300)
    parser.add_argument("--no-browser", action="store_true", help="Mostra a URL de OAuth sem abrir o navegador automaticamente")
    args = parser.parse_args()

    if not args.client_secrets.exists():
        raise SystemExit(f"Arquivo OAuth não encontrado: {args.client_secrets}")

    now = datetime.now(UTC)
    published_after = now - timedelta(hours=args.hours)
    youtube = get_youtube_service(
        args.client_secrets,
        args.token,
        auth_port=args.auth_port,
        auth_timeout_seconds=args.auth_timeout_seconds,
        open_browser=not args.no_browser,
    )

    channels = list_subscribed_channels(youtube)
    playlists = get_upload_playlists(youtube, [channel["id"] for channel in channels])
    videos = list_recent_philosophy_videos(
        youtube=youtube,
        playlists=playlists,
        published_after=published_after,
        keywords=args.keywords,
        pages_per_channel=args.pages_per_channel,
    )
    videos = add_video_durations(youtube, videos)
    videos = [video for video in videos if video.duration_seconds > args.min_duration_seconds]
    videos = sorted(videos, key=lambda video: (video.duration_seconds or 10**9, video.published_at))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(videos, now, published_after), encoding="utf-8")
    print(f"Canais inscritos: {len(channels)}")
    print(f"Vídeos de filosofia encontrados: {len(videos)}")
    print(f"HTML gerado: {args.output}")


if __name__ == "__main__":
    main()
