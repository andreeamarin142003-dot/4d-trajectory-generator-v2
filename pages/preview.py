# ─────────────────────────────────────────────────────────────────────────────
# pages/preview.py  —  Route Preview page
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from components.navbar import render as navbar
from components.maps import route_map
from trajectory import get_coords, compute_trajectory
from config import ACTYPE, CRUISE_FL


def _to_dms(dd: float, is_lat: bool) -> str:
    """Convert decimal degrees to AIP DMS format (e.g. N4434.30 E02605.10)."""
    hem = ("N" if dd >= 0 else "S") if is_lat else ("E" if dd >= 0 else "W")
    dd  = abs(dd)
    d   = int(dd)
    m   = (dd - d) * 60
    # Latitude: 2-digit degrees  |  Longitude: 3-digit degrees
    return f"{hem}{d:02d}{m:05.2f}" if is_lat else f"{hem}{d:03d}{m:05.2f}"


def show():
    navbar("preview")

    if "waypoints" not in st.session_state:
        st.info("Please generate a route first.")
        return

    wps     = st.session_state["waypoints"]
    airways = st.session_state.get("airways", [])
    adep    = st.session_state["adep"]
    ades    = st.session_state["ades"]

    left, right = st.columns([1, 1.4], gap="large")

    with left:
        st.markdown("## Route Preview")
        st.markdown(f"**{adep} → {ades}**")
        st.markdown(
            f'<span style="color:#22c55e;font-weight:600">{ACTYPE}</span>'
            f'&nbsp;|&nbsp;FL{CRUISE_FL}',
            unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Waypoints:**")

        for i, wp in enumerate(wps):
            c = get_coords(wp)
            if c:
                coord = f"{_to_dms(c[0], True)}  {_to_dms(c[1], False)}"
            else:
                coord = "—"

            airway    = airways[i] if i < len(airways) else ""
            airway_html = (
                f'<br><span class="wp-airway">✈ {airway}</span>'
                if airway and airway != "DCT" else "")

            st.markdown(f"""
            <div class="wp-card">
              <span class="wp-name">{wp}</span>
              <span class="wp-coord">{coord}</span>
              {airway_html}
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate 4D Trajectory →", use_container_width=True):
            with st.spinner("Computing trajectory…"):
                df = compute_trajectory(
                    wps, st.session_state.get("dep_time", "20:00"))
            st.session_state["trajectory"] = df
            st.session_state["page"]       = "trajectory"
            st.rerun()

    with right:
        route_map(wps, key="rmap_preview")
