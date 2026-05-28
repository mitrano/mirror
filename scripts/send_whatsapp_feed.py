#!/usr/bin/env python3
"""Send the generated YouTube philosophy feed to WhatsApp via Meta Cloud API.

Required environment variables:
  WHATSAPP_ACCESS_TOKEN   Permanent or temporary Meta Graph API token
  WHATSAPP_PHONE_NUMBER_ID  WhatsApp Business Phone Number ID
  WHATSAPP_TO              Recipient phone number with country code, digits only

Example:
  WHATSAPP_ACCESS_TOKEN="..." \
  WHATSAPP_PHONE_NUMBER_ID="123456789" \
  WHATSAPP_TO="5511999999999" \
  uv run python scripts/send_whatsapp_feed.py \
    --input exports/youtube_filosofia_24h_whatsapp.txt
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

GRAPH_API_VERSION = "v20.0"
MAX_WHATSAPP_TEXT_CHARS = 4096


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Variável de ambiente obrigatória ausente: {name}")
    return value


def split_message(text: str, max_chars: int = MAX_WHATSAPP_TEXT_CHARS) -> list[str]:
    """Split text into WhatsApp-sized chunks, preferring paragraph boundaries."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        candidate = paragraph if not current else f"{current}\n\n{paragraph}"
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
            current = ""
        while len(paragraph) > max_chars:
            chunks.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
        current = paragraph
    if current:
        chunks.append(current)
    return chunks


def send_text_message(
    *,
    access_token: str,
    phone_number_id: str,
    recipient: str,
    text: str,
    graph_api_version: str,
) -> dict[str, object]:
    url = f"https://graph.facebook.com/{graph_api_version}/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {"preview_url": True, "body": text},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Erro HTTP {error.code} ao enviar WhatsApp:\n{body}") from error


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("exports/youtube_filosofia_24h_whatsapp.txt"),
        help="Arquivo TXT formatado para WhatsApp",
    )
    parser.add_argument("--graph-api-version", default=GRAPH_API_VERSION)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra quantas mensagens seriam enviadas, sem chamar a API",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Arquivo não encontrado: {args.input}")

    text = args.input.read_text(encoding="utf-8")
    chunks = split_message(text)
    if not chunks:
        raise SystemExit("Arquivo de entrada está vazio.")

    if args.dry_run:
        print(f"Arquivo: {args.input}")
        print(f"Partes a enviar: {len(chunks)}")
        for index, chunk in enumerate(chunks, start=1):
            print(f"Parte {index}: {len(chunk)} caracteres")
        return

    access_token = require_env("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = require_env("WHATSAPP_PHONE_NUMBER_ID")
    recipient = require_env("WHATSAPP_TO")

    for index, chunk in enumerate(chunks, start=1):
        prefix = f"Parte {index}/{len(chunks)}\n\n" if len(chunks) > 1 else ""
        response = send_text_message(
            access_token=access_token,
            phone_number_id=phone_number_id,
            recipient=recipient,
            text=f"{prefix}{chunk}",
            graph_api_version=args.graph_api_version,
        )
        message_id = response.get("messages", [{}])[0].get("id", "sem-id")
        print(f"Enviado parte {index}/{len(chunks)}: {message_id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrompido.", file=sys.stderr)
        raise SystemExit(130)
