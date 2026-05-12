# ─────────────────────────────────────────────────────────────────────────────
# pages/route.py  —  Route Generator page
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import plotly.graph_objects as go
from components.navbar import render as navbar
from components.maps import route_map
from config import AIRPORTS, ROUTES, DEPARTURES, VALID_DEST, ACTYPE, CRUISE_FL


def show():
    navbar("route")

    left, right = st.columns([1, 1.4], gap="large")

    with left:
        st.markdown("## Route Generator")

        # ── Departure selector ────────────────────────────────────────────
        dep_opts = {f"{k} – {AIRPORTS[k]['name']}": k for k in DEPARTURES}
        dep_label = st.selectbox("Departure Airport (ADEP)",
                                 list(dep_opts.keys()), key="sel_dep")
        adep = dep_opts[dep_label]

        # ── Destination selector (filtered by departure) ──────────────────
        valid = VALID_DEST[adep]
        dest_opts = {f"{k} – {AIRPORTS[k]['name']}": k for k in valid}
        des_label = st.selectbox("Destination Airport (ADES)",
                                 list(dest_opts.keys()), key="sel_des")
        ades = dest_opts[des_label]

        # ── Fixed aircraft info ───────────────────────────────────────────
        st.markdown(f"""
        <div class="ac-info">
          ✈&nbsp; Aircraft: <b style="color:#a78bfa">{ACTYPE}</b>
          &nbsp;|&nbsp;
          Cruise Level: <b style="color:#a78bfa">FL{CRUISE_FL}</b>
        </div>""", unsafe_allow_html=True)

        dep_time = st.text_input("Departure Time (UTC)", "20:00",
                                 key="dep_time_input")

        # ── Generate ──────────────────────────────────────────────────────
        if st.button("Generate Route →", use_container_width=True):
            key = f"{adep}-{ades}"
            if key in ROUTES:
                wps, airways = ROUTES[key]
                st.session_state["waypoints"] = wps
                st.session_state["airways"]   = airways
                st.session_state["adep"]      = adep
                st.session_state["ades"]      = ades
                st.session_state["dep_time"]  = dep_time
                st.session_state["page"]      = "preview"
                st.rerun()

    # ── Map ───────────────────────────────────────────────────────────────────
    with right:
        # Show current route if already generated, otherwise blank map
        if "adep" in st.session_state and "ades" in st.session_state:
            key = f"{st.session_state['adep']}-{st.session_state['ades']}"
            if key in ROUTES:
                route_map(ROUTES[key][0], key="rmap_route")
                return

        # Blank placeholder map
        a = AIRPORTS["LROP"]; b = AIRPORTS["EHAM"]
        fig = go.Figure(go.Scattermapbox(
            mode="markers",
            lat=[a["lat"], b["lat"]], lon=[a["lon"], b["lon"]],
            marker=dict(size=8, color="#7c3aed")))
        fig.update_layout(
            mapbox=dict(style="carto-darkmatter",
                        center=dict(lat=48, lon=13), zoom=3),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)", height=480)
        st.plotly_chart(fig, use_container_width=True, key="rmap_blank")
