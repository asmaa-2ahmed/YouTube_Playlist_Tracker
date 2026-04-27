"""Reusable HTML component builders for the Streamlit UI."""


def playlist_banner(title: str) -> str:
    return f"""
    <div class="pl-banner">
        <div class="lbl">Playlist</div>
        <div class="title">{title}</div>
    </div>"""


def metric_grid(*cards: tuple) -> str:
    """Build a 2-col metric grid.  Each card is (label, value, accent=False)."""
    inner = ""
    for label, value, *rest in cards:
        accent = "accent" if rest and rest[0] else ""
        inner += f'<div class="card {accent}"><div class="lbl">{label}</div><div class="val">{value}</div></div>'
    return f'<div class="metric-grid">{inner}</div>'


def progress_bar(pct: float, current: int, total: int) -> str:
    return f"""
    <div class="prog-wrap">
        <div class="prog-track">
            <div class="prog-fill" style="width:{pct:.2f}%"></div>
        </div>
        <div class="prog-meta">
            <span>Video {current} of {total}</span>
            <span class="prog-pct">{pct:.1f}% complete</span>
        </div>
    </div>"""
