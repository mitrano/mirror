---
name: "mm-transcribe"
description: Transcribes local audio or video files through the clean Mirror Transcriber project. Use when Ricardo asks to transcribe a local audio/video file.
user-invocable: true
---

# Mirror Transcription

Use this skill when Ricardo asks to transcribe a local audio or video file.

## Backing Repository

- Journey: `transcricao-audio-video`
- Repository: `/home/ricardoalvares/repos/mirror-transcriber`
- Entry point: `uv run mirror-transcriber`

This skill uses the separate Mirror-focused transcription project. The original Windows `TranscritorWPP` repository remains separate and should not be edited for Mirror runtime use.

## Usage

For a local file path:

```bash
cd /home/ricardoalvares/repos/mirror-transcriber
uv run mirror-transcriber --provider gemini --no-diarize "/path/to/audio-or-video"
```

Useful variants:

```bash
uv run mirror-transcriber --provider groq "/path/to/audio-or-video"
uv run mirror-transcriber --provider local --no-diarize "/path/to/audio-or-video"
uv run mirror-transcriber --provider gemini --diarize "/path/to/audio-or-video"
uv run mirror-transcriber --print "/path/to/audio-or-video"
```

Provider options:

- `gemini` — preferred cloud route when API key exists.
- `groq` — hosted Whisper route.
- `local` — local Whisper route; use when cloud is unavailable or privacy/offline is preferred.

Format support:

- Mirror Transcriber does not use a fixed extension allowlist.
- For non-MP3 files, it asks FFmpeg to extract the first audio stream and convert it to MP3.
- Practical guarantee: if FFmpeg can open the audio/video file and extract audio, the tool attempts transcription.

Diarization:

- Use `--diarize` when Ricardo needs speaker identification.
- Groq is skipped when diarization is requested because it does not provide real diarization.
- Use `--no-diarize` for simpler/faster transcription.

## Operating Protocol

1. Confirm or infer the file path Ricardo wants transcribed.
2. If the path is unclear or inaccessible, ask for the file/path.
3. Prefer `--provider gemini --no-diarize` unless Ricardo requests offline/private/local processing or speaker identification.
4. Run the command from `/home/ricardoalvares/repos/mirror-transcriber`.
5. The generated `.txt` is written beside the original file unless `--output-dir` is used.
6. Read the generated text file and return the transcription or a concise summary, according to Ricardo's request.

## Safety / Compatibility

- Do not edit the Windows `TranscritorWPP` repository as part of normal Mirror transcription use.
- Do not commit audio, video, generated transcripts, logs, `.env`, API keys, or temporary files.
- If dependencies are missing, report the missing requirement instead of improvising.
