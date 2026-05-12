# ─────────────────────────────────────────────────────────────────────────────
# pages/vertical.py  —  Vertical Profile & Flight Summary
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import plotly.graph_objects as go
from components.navbar import render as navbar
from config import ACTYPE, CRUISE_FL

PHASE_COLOR  = {"climb": "#f59e0b", "cruise": "#22c55e", "descent": "#ef4444"}
RESET_KEYS   = ["waypoints", "airways", "adep", "ades", "trajectory", "dep_time"]


def show():
    navbar("vertical")

    if "trajectory" not in st.session_state:
        st.info("Please generate a trajectory first.")
        return

    df   = st.session_state["trajectory"]
    adep = st.session_state["adep"]
    ades = st.session_state["ades"]

    dur_min  = round(len(df) * 30 / 60)
    total_nm = df["dist_nm"].max()

    # ── Vertical Profile chart ────────────────────────────────────────────────
    st.markdown(f"### Vertical Profile — {adep} → {ades}  ({ACTYPE}, FL{CRUISE_FL})")

    fig = go.Figure()
    for phase, color in PHASE_COLOR.items():
        d = df[df["phase"] == phase]
        if not d.empty:
            fig.add_trace(go.Scatter(
                x=d["time"], y=d["altitude"],
                mode="lines", line=dict(width=3, color=color),
                name=phase.capitalize(),
                hovertemplate="<b>%{x}</b><br>Alt: %{y:,} ft<extra></extra>"))

    fig.update_layout(
        xaxis=dict(
            title=dict(text="Time (UTC)", font=dict(color="#6b7cb8")),
            tickfont=dict(color="#6b7cb8"),
            gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(
            title=dict(text="Altitude (ft)", font=dict(color="#6b7cb8")),
            tickfont=dict(color="#6b7cb8"),
            gridcolor="rgba(255,255,255,0.08)",
            tickformat=","),
        legend=dict(font=dict(color="#e2e8f0"), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="#0a0c1a", plot_bgcolor="#0a0c1a",
        height=360, margin=dict(l=60, r=20, t=20, b=60))
    st.plotly_chart(fig, use_container_width=True, key="vp_chart")

    # ── Flight Summary ────────────────────────────────────────────────────────
    st.markdown("### Flight Summary")

    cruise_df = df[df["phase"] == "cruise"]
    climb_df  = df[df["phase"] == "climb"]
    desc_df   = df[df["phase"] == "descent"]

    toc_row = cruise_df.iloc[0]  if not cruise_df.empty else None
    tod_row = desc_df.iloc[0]    if not desc_df.empty  else None

    # Row 1: high-level
    r1 = st.columns(5)
    r1[0].metric("Departure",       df["time"].iloc[0])
    r1[1].metric("Arrival (est.)",  df["time"].iloc[-1])
    r1[2].metric("Flight Time",     f"{dur_min} min")
    r1[3].metric("Distance",        f"{total_nm:.0f} nm")
    r1[4].metric("Cruise Level",    f"FL{CRUISE_FL}")

    # Row 2: phase details
    if toc_row is not None and tod_row is not None:
        st.markdown("---")
        r2 = st.columns(4)
        r2[0].metric("TOC — Top of Climb",   toc_row.time)
        r2[1].metric("TOD — Top of Descent", tod_row.time)
        r2[2].metric("Cruise TAS",
                     f"{round(cruise_df['speed_tas'].mean())} kt")
        r2[3].metric("Cruise Mach",
                     f"M{cruise_df['mach'].mean():.3f}")

        r3 = st.columns(4)
        r3[0].metric("TOC Flight Level",    f"FL{toc_row.fl}")
        r3[1].metric("TOD Flight Level",    f"FL{tod_row.fl}")
        r3[2].metric("Climb Duration",
                     f"{round(len(climb_df) * 30 / 60)} min")
        r3[3].metric("Descent Duration",
                     f"{round(len(desc_df) * 30 / 60)} min")

    # ── Phase Statistics table ────────────────────────────────────────────────
    st.markdown("### Phase Statistics")
    stats = (
        df.groupby("phase")
        .agg(**{
            "Duration (min)": ("phase",     lambda x: round(len(x) * 30 / 60, 1)),
            "Avg Alt (ft)":   ("altitude",  lambda x: round(x.mean())),
            "Max Alt (ft)":   ("altitude",  "max"),
            "Avg TAS (kt)":   ("speed_tas", lambda x: round(x.mean())),
            "Avg Mach":       ("mach",      lambda x: round(x.mean(), 3)),
            "Distance (nm)":  ("dist_nm",   lambda x: round(x.max() - x.min(), 1)),
        })
        .reset_index()
        .rename(columns={"phase": "Phase"})
    )
    st.dataframe(stats, use_container_width=True)

    # ── Restart button ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        if st.button("🔄 Start New Flight", use_container_width=True):
            for k in RESET_KEYS:
                st.session_state.pop(k, None)
            st.session_state["page"] = "home"
            st.rerun()
