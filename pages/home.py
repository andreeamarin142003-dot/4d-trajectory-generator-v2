# ─────────────────────────────────────────────────────────────────────────────
# pages/home.py  —  Landing / hero page
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from components.navbar import render as navbar


def show():
    navbar("home")

    # Three columns: empty | content | empty  →  centres everything
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("""
        <div style="text-align:center; padding: 4rem 0 2rem;">
          <h1 style="font-size:2.6rem;font-weight:300;color:#fff;
                     letter-spacing:-0.02em;">
            4D Trajectory Generator
          </h1>
          <p style="color:rgba(255,255,255,0.6);font-size:15px;
                    line-height:1.85;margin:1.4rem 0 2.8rem;">
            The 4D Trajectory Generator is an interactive tool that computes
            realistic aircraft trajectories using official AIP navigation data.
            By selecting a departure airport (ADEP) and destination airport (ADES),
            the system automatically builds a valid route using published waypoints
            and airways. It then generates a full 4D flight profile — latitude,
            longitude, altitude, and speed over time — based on a simplified
            aircraft performance model with variable climb, cruise, and descent
            speeds. The trajectory climbs ASAP to the chosen cruise level and
            descends ALAP, following standard ATM principles and assuming no wind.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Centre the button using a sub-column layout
        b_left, b_mid, b_right = st.columns([1, 1, 1])
        with b_mid:
            if st.button("Get Started →", use_container_width=True):
                st.session_state["page"] = "route"
                st.rerun()
