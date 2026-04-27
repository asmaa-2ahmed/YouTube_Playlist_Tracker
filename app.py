"""YouTube Playlist Tracker — Streamlit entry point."""

from pathlib import Path
import streamlit as st
from utils import (
    fetch_durations, calc_progress, hms_str,
    parse_mmss, is_valid_playlist_url,
    playlist_banner, metric_grid, progress_bar,
)

# ── Page setup ────────────────────────────────────────────────────────────────

st.set_page_config(page_title="YT Playlist Tracker", page_icon="📺", layout="centered")

css = Path("utils/styles.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown('<div class="hero-title">Track Your Progress 💪📈 </div>', unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────

st.markdown('<div class="section-label">Playlist URL</div>', unsafe_allow_html=True)
url = st.text_input("url", placeholder="https://youtube.com/playlist?list=...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Where are you? (optional)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    idx_input = st.number_input("Current video index (1-based)", min_value=0, step=1, value=0,
                                help="Leave at 0 to show total duration only.")
with col2:
    time_input = st.text_input("Time in current video (mm:ss)", placeholder="e.g. 12:34",
                               help="Leave blank if at the start.")

include_current = st.checkbox("Count full current video as completed")

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("Calculate →")

# ── On submit ─────────────────────────────────────────────────────────────────

if not run:
    st.stop()

# Validate URL
if not url.strip():
    st.error("Please enter a playlist URL.")
    st.stop()

if not is_valid_playlist_url(url.strip()):
    st.error("URL doesn't look like a YouTube playlist. Expected a link containing 'youtube.com/playlist'.")
    st.stop()

# Parse optional timestamp
current_time_sec = 0
if time_input.strip():
    try:
        current_time_sec = parse_mmss(time_input)
    except ValueError:
        st.warning("Invalid time format — expected mm:ss. Time will be treated as 0.")

# Fetch playlist
with st.spinner("Fetching playlist info…"):
    data = fetch_durations(url.strip())

if "error" in data:
    st.error(f"Could not fetch playlist: {data['error']}")
    st.stop()

durations   = data["durations"]
total_sec   = sum(durations)
total_count = len(durations)
skipped     = data["skipped"]

if skipped:
    st.warning(f"{skipped} video(s) were skipped (private or deleted).")

# ── Display results ───────────────────────────────────────────────────────────

st.markdown(playlist_banner(data["title"]), unsafe_allow_html=True)
st.markdown(
    metric_grid(("Total videos", total_count), ("Total duration", hms_str(total_sec), True)),
    unsafe_allow_html=True,
)

# Progress section (only if user provided a valid index)
current_index = int(idx_input) if idx_input > 0 else None

if current_index is not None:
    prog = calc_progress(durations, current_index, current_time_sec, include_current)

    if prog is None:
        st.error(f"Video index {current_index} is out of range (playlist has {total_count} videos).")
        st.stop()

    st.markdown(
        metric_grid(
            ("Completed", hms_str(prog["completed"])),
            ("Remaining", hms_str(prog["remaining"])),
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        progress_bar(prog["pct"], current_index, total_count),
        unsafe_allow_html=True,
    )
