---
name: "mm-transcribe"
description: Transcribes local audio or video files through Ricardo's TranscritorWPP repository. Use when Ricardo asks to transcribe an audio/video file and no better direct transcription route is available.
user-invocable: true
---

# Mirror Transcription

Use this skill when Ricardo asks to transcribe a local audio or video file.

## Backing Repository

- Journey: `transcricao-audio-video`
- Repository: `/home/ricardoalvares/repos/TranscritorWPP`
- Entry point: `/home/ricardoalvares/repos/TranscritorWPP/transcribe.py`

This skill is an operational bridge. The Windows `.bat` flow in TranscritorWPP is the preserved Windows contract and must not be changed just to serve Mirror.

## Usage

For a local file path:

```bash
cd /home/ricardoalvares/repos/TranscritorWPP
python transcribe.py --provider gemini --no-diarize "/path/to/audio-or-video"
```

Provider options:

- `gemini` — default preferred cloud route when API key exists.
- `groq` — Whisper hosted route.
- `local` — local Whisper route; use when cloud is unavailable or privacy/offline is preferred.

Diarization:

- Use `--diarize` when Ricardo needs speaker identification and the provider supports it.
- Use `--no-diarize` for simpler/faster transcription.

Dry run before processing uncertain files:

```bash
cd /home/ricardoalvares/repos/TranscritorWPP
python transcribe.py --dry-run "/path/to/audio-or-video"
```

## Operating Protocol

1. Confirm or infer the file path Ricardo wants transcribed.
2. If the path is unclear or inaccessible, ask for the file/path.
3. Prefer `--provider gemini --no-diarize` unless Ricardo requests offline/private/local processing or speaker identification.
4. Run the command from the TranscritorWPP repository.
5. The generated `.txt` is written beside the processed MP3 by TranscritorWPP.
6. Read the generated text file and return the transcription or a concise summary, according to Ricardo's request.

## Safety / Compatibility

- Do not edit the Windows `.bat` files as part of normal transcription use.
- Do not commit audio, video, generated transcripts, logs, `.env`, API keys, or temporary files.
- If dependencies are missing, report the missing requirement instead of improvising.
