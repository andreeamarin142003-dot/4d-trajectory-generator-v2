# ─────────────────────────────────────────────────────────────────────────────
# pages/trajectory_page.py  —  4D Trajectory viewer
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from components.navbar import render as navbar
from components.maps import trajectory_map
from config import ACTYPE, CRUISE_FL

PHASE_COLOR = {"climb": "#f59e0b", "cruise": "#22c55e", "descent": "#ef4444"}


def show():
    navbar("trajectory")

    if "trajectory" not in st.session_state:
        st.info("Please generate a trajectory first.")
        return

    df   = st.session_state["trajectory"]
    wps  = st.session_state["waypoints"]
    adep = st.session_state["adep"]
    ades = st.session_state["ades"]

    left, right = st.columns([1, 1.5], gap="large")

    with left:
        st.markdown("## 4D Trajectory")
        st.markdown(f"**{adep} → {ades}** &nbsp;|&nbsp; {ACTYPE} FL{CRUISE_FL}")

        # ── Summary metrics ───────────────────────────────────────────────
        dur_min = round(len(df) * 30 / 60)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Samples",     f"{len(df)} pts", "30 s/pt")
        m2.metric("Flight Time", f"{dur_min} min")
        m3.metric("Max Alt",     f"FL{df['fl'].max()}")
        m4.metric("Avg TAS",     f"{round(df['speed_tas'].mean())} kt")

        # ── Phase breakdown ───────────────────────────────────────────────
        pc = df["phase"].value_counts()
        ph1, ph2, ph3 = st.columns(3)
        for ph, col in zip(["climb", "cruise", "descent"], [ph1, ph2, ph3]):
            pct = pc.get(ph, 0) / len(df) * 100
            col.markdown(f"""
            <div style="text-align:center;background:rgba(255,255,255,0.04);
                 border-radius:10px;padding:10px;
                 border:1px solid rgba(255,255,255,0.06);">
              <div style="width:9px;height:9px;border-radius:50%;
                   background:{PHASE_COLOR[ph]};margin:0 auto 4px;"></div>
              <div style="font-size:11px;color:rgba(255,255,255,0.45)">
                {ph.capitalize()}</div>
              <div style="font-size:16px;font-weight:500">{pct:.0f}%</div>
            </div>""", unsafe_allow_html=True)

        # ── Data table ────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(
            df[["time", "lat", "lon", "altitude", "fl", "speed_tas", "mach", "phase"]]
            .rename(columns={
                "time": "Time", "lat": "Lat", "lon": "Lon",
                "altitude": "Alt (ft)", "fl": "FL",
                "speed_tas": "TAS (kt)", "mach": "Mach", "phase": "Phase"}),
            use_container_width=True, height=240)

        csv = df.to_csv(index=False).encode()
        st.download_button("⬇ Download CSV", csv, "trajectory.csv", "text/csv")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("View Vertical Profile →", use_container_width=True):
            st.session_state["page"] = "vertical"
            st.rerun()

    with right:
        trajectory_map(df, wps, key="tmap_traj")
