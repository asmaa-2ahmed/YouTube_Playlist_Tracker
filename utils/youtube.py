"""Core YouTube playlist logic: fetching, duration math, time helpers."""

from typing import Optional
import yt_dlp


# ── Time helpers ──────────────────────────────────────────────────────────────

def hms_str(seconds: int) -> str:
    """Return a readable duration string e.g. '2h 04m 07s' or '14m 03s'."""
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m:02d}m {s:02d}s" if h else f"{m}m {s:02d}s"


def parse_mmss(time_str: str) -> int:
    """Parse 'mm:ss' → total seconds.  Raises ValueError on bad input."""
    parts = time_str.strip().split(":")
    if len(parts) != 2:
        raise ValueError("Expected mm:ss format")
    return int(parts[0]) * 60 + int(parts[1])


def is_valid_playlist_url(url: str) -> bool:
    """Quick check that the URL looks like a YouTube playlist."""
    return "youtube.com/playlist" in url or "youtu.be" in url


# ── Playlist fetching ─────────────────────────────────────────────────────────

def fetch_durations(playlist_url: str) -> dict:
    """
    Fetch video durations for a playlist via yt-dlp.

    Uses extract_flat='in_playlist' for speed (no per-video requests).
    ignoreerrors=True skips private / deleted videos instead of crashing.

    Returns dict with keys: title, durations (list[int]), skipped (int)
    Or dict with key: error (str)
    """
    opts = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,           # don't crash on private/deleted videos
        "extract_flat": "in_playlist",  # fast: reads playlist page only
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)

        if not info:
            return {"error": "No data returned. Check the URL."}

        entries = info.get("entries") or []
        durations, skipped = [], 0

        for entry in entries:
            if not entry:                # None = yt-dlp skipped (private/deleted)
                skipped += 1
                continue
            dur = entry.get("duration") or 0
            durations.append(int(dur))

        return {
            "title": info.get("title") or "Untitled Playlist",
            "durations": durations,
            "skipped": skipped,
        }

    except Exception as exc:
        return {"error": str(exc)}


# ── Progress calculation ──────────────────────────────────────────────────────

def calc_progress(
    durations: list,
    current_index: int,
    current_time_sec: int = 0,
    include_current: bool = False,
) -> Optional[dict]:
    """
    Compute progress stats given durations list and current position.

    Args:
        durations:        List of video durations in seconds.
        current_index:    1-based index of the video being watched.
        current_time_sec: Seconds elapsed inside the current video.
        include_current:  Count the full current video as completed.

    Returns None if current_index is out of range.
    """
    n = len(durations)
    if not (1 <= current_index <= n):
        return None

    video_dur = durations[current_index - 1]
    elapsed   = min(current_time_sec, video_dur)
    completed = sum(durations[:current_index - 1]) + (video_dur if include_current else elapsed)
    total     = sum(durations)
    remaining = total - completed

    return {
        "completed": completed,
        "remaining": remaining,
        "pct": (completed / total * 100) if total else 0.0,
        "video_duration": video_dur,
    }
