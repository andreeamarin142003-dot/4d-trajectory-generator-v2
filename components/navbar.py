# ─────────────────────────────────────────────────────────────────────────────
# components/navbar.py  —  Top navigation bar
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st

STEPS = [
    ("Home",            "home"),
    ("Route Generator", "route"),
    ("Route Preview",   "preview"),
    ("Trajectory",      "trajectory"),
    ("Vertical Profile","vertical"),
]

RESET_KEYS = ["waypoints", "airways", "adep", "ades", "trajectory", "dep_time"]


def _reset_and_go(page: str):
    """Clear flight state and navigate to page."""
    for k in RESET_KEYS:
        st.session_state.pop(k, None)
    st.session_state["page"] = page
    st.rerun()


def render(active: str):
    """Render the sticky top navigation bar."""
    logo_col, steps_col, btn_col = st.columns([2, 5, 2])

    # ── Logo ─────────────────────────────────────────────────────────────────
    with logo_col:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:10px 0 4px;">
          <div style="width:26px;height:26px;
               background:linear-gradient(135deg,#7c3aed,#4f46e5);
               border-radius:6px;font-size:13px;display:flex;
               align-items:center;justify-content:center;">✦</div>
          <span style="font-size:14px;font-weight:600;color:#fff;">
            4D Trajectory Generator<span style="color:#7c3aed">.</span>
          </span>
        </div>""", unsafe_allow_html=True)

    # ── Step links ────────────────────────────────────────────────────────────
    with steps_col:
        nav_cols = st.columns(len(STEPS))
        for (label, page), col in zip(STEPS, nav_cols):
            with col:
                is_active = (page == active)
                # Active step gets a subtle purple highlight; others are ghost
                btn_style = (
                    "border:1px solid rgba(124,58,237,0.5);"
                    "background:rgba(124,58,237,0.18);color:#fff;"
                    if is_active else
                    "border:1px solid transparent;"
                    "background:transparent;color:rgba(255,255,255,0.5);"
                )
                # Inject per-button style via markdown trick
                st.markdown(f"""
                <style>
                div[data-testid="column"] button[kind="secondary"]{{}}
                #nav-{page} button{{
                    {btn_style}
                    border-radius:7px;font-size:12px;padding:5px 8px;
                    width:100%;transition:all .15s;
                }}
                </style>""", unsafe_allow_html=True)
                if st.button(label, key=f"nav_{page}_{active}",
                             use_container_width=True):
                    # Navigating backwards is allowed without resetting state
                    st.session_state["page"] = page
                    st.rerun()

    # ── Get Started button ────────────────────────────────────────────────────
    with btn_col:
        st.markdown("<div style='padding:6px 0;'>", unsafe_allow_html=True)
        if st.button("✈ Get Started", key=f"gs_{active}",
                     type="primary", use_container_width=True):
            _reset_and_go("home")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<hr style="margin:4px 0 16px;border-color:rgba(255,255,255,0.07);">',
                unsafe_allow_html=True)
