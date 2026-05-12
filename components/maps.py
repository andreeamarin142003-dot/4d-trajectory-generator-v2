# ─────────────────────────────────────────────────────────────────────────────
# components/maps.py  —  Plotly/Mapbox map renderers
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from trajectory import get_coords

PHASE_COLOR = {"climb": "#f59e0b", "cruise": "#22c55e", "descent": "#ef4444"}
MAP_STYLE   = "carto-darkmatter"


def _base_layout(lats: list, lons: list, height: int = 480) -> dict:
    return dict(
        mapbox=dict(style=MAP_STYLE,
                    center=dict(lat=sum(lats)/len(lats), lon=sum(lons)/len(lons)),
                    zoom=4),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
    )


def route_map(waypoints: list[str], key: str = "rmap"):
    """Draw the planned route with waypoint labels."""
    pts   = [(wp, *get_coords(wp)) for wp in waypoints if get_coords(wp)]
    lats  = [p[1] for p in pts]
    lons  = [p[2] for p in pts]
    names = [p[0] for p in pts]

    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        mode="lines", lat=lats, lon=lons,
        line=dict(width=2.5, color="#7c3aed"), hoverinfo="skip"))
    fig.add_trace(go.Scattermapbox(
        mode="markers+text", lat=lats, lon=lons,
        text=names, textposition="top right",
        textfont=dict(size=10, color="#c4b5fd"),
        marker=dict(size=7, color="#7c3aed"),
        hovertext=names, hoverinfo="text"))

    fig.update_layout(**_base_layout(lats, lons), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, key=key)


def trajectory_map(df: pd.DataFrame, waypoints: list[str], key: str = "tmap"):
    """Draw the 4D trajectory coloured by phase + altitude colour bar."""
    fig = go.Figure()

    # Phase-coloured lines
    for phase, color in PHASE_COLOR.items():
        d = df[df["phase"] == phase]
        if not d.empty:
            fig.add_trace(go.Scattermapbox(
                mode="lines", lat=d["lat"], lon=d["lon"],
                line=dict(width=3.5, color=color),
                name=phase.capitalize()))

    # Altitude colour-scale markers (every 6th point to reduce clutter)
    sample = df[::6]
    fig.add_trace(go.Scattermapbox(
        mode="markers", lat=sample["lat"], lon=sample["lon"],
        marker=go.scattermapbox.Marker(
            size=5, color=sample["altitude"], colorscale="Viridis",
            showscale=True,
            colorbar=dict(
                title=dict(text="Alt (ft)", font=dict(color="#e2e8f0")),
                tickfont=dict(color="#e2e8f0"),
                bgcolor="rgba(13,15,30,0.8)",
                bordercolor="rgba(255,255,255,0.1)",
                thickness=12)),
        hovertext=[
            f"<b>{r.time}</b><br>"
            f"Alt: {r.altitude:,} ft (FL{r.fl})<br>"
            f"TAS: {r.speed_tas} kt  M{r.mach:.3f}<br>"
            f"{r.phase.capitalize()}"
            for r in sample.itertuples()],
        hoverinfo="text", showlegend=False))

    # Waypoint pins
    for wp in waypoints:
        c = get_coords(wp)
        if c:
            fig.add_trace(go.Scattermapbox(
                mode="markers+text", lat=[c[0]], lon=[c[1]],
                text=[wp], textposition="top right",
                textfont=dict(size=9, color="#93c5fd"),
                marker=dict(size=7, color="#1d4ed8"),
                hovertext=[wp], hoverinfo="text", showlegend=False))

    fig.update_layout(
        **_base_layout(df["lat"].tolist(), df["lon"].tolist()),
        legend=dict(font=dict(color="#e2e8f0"),
                    bgcolor="rgba(13,15,30,0.7)",
                    bordercolor="rgba(255,255,255,0.1)",
                    borderwidth=1, x=0.01, y=0.99))
    st.plotly_chart(fig, use_container_width=True, key=key)
