# ─────────────────────────────────────────────────────────────────────────────
# trajectory.py  —  4D trajectory computation engine
# Uses a simplified BADA-inspired performance model for the A321N
# ─────────────────────────────────────────────────────────────────────────────

import math
import pandas as pd
from datetime import datetime, timedelta
from config import AIRPORTS, WAYPOINTS, PERF, CRUISE_ALT_FT


def get_coords(wp: str) -> tuple[float, float] | None:
    """Return (lat, lon) for an airport or waypoint identifier."""
    if wp in AIRPORTS:
        return AIRPORTS[wp]["lat"], AIRPORTS[wp]["lon"]
    if wp in WAYPOINTS:
        return WAYPOINTS[wp]
    return None


def haversine_nm(la1, lo1, la2, lo2) -> float:
    """Great-circle distance in nautical miles."""
    R = 3440.065
    la1, lo1, la2, lo2 = map(math.radians, [la1, lo1, la2, lo2])
    dlat = la2 - la1
    dlon = lo2 - lo1
    a = math.sin(dlat / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def mach_to_tas(mach: float, alt_ft: float) -> float:
    """Convert Mach number to True Air Speed (kt) using ISA temperature."""
    T = 288.15 - 0.0065 * min(alt_ft, 36_089) * 0.3048 if alt_ft <= 36_089 else 216.65
    return mach * 661.4786 * math.sqrt(T / 288.15)


def cas_to_tas(cas: float, alt_ft: float) -> float:
    """Approximate CAS → TAS conversion using ISA density ratio."""
    return cas / math.sqrt(math.exp(-alt_ft / 27_000))


def interp(table: dict, alt: float) -> float:
    """Linear interpolation over an altitude-keyed performance table."""
    keys = sorted(table)
    if alt <= keys[0]:
        return table[keys[0]]
    if alt >= keys[-1]:
        return table[keys[-1]]
    for i in range(len(keys) - 1):
        if keys[i] <= alt <= keys[i + 1]:
            f = (alt - keys[i]) / (keys[i + 1] - keys[i])
            return table[keys[i]] * (1 - f) + table[keys[i + 1]] * f


def _toc_distance(start_alt: float) -> float:
    """Estimate distance (nm) flown during climb from start_alt to cruise."""
    DT = 30
    alt, dist = float(start_alt), 0.0
    while alt < CRUISE_ALT_FT:
        cr = interp(PERF["climb_rate_fpm"], alt)
        spd = (cas_to_tas(PERF["climb_cas_lo_kt"], alt) if alt < 10_000
               else cas_to_tas(PERF["climb_cas_hi_kt"], alt) if alt < 28_000
               else mach_to_tas(PERF["cruise_mach"] * 0.97, alt))
        alt = min(alt + cr / 60 * DT, CRUISE_ALT_FT)
        dist += spd / 3600 * DT
    return dist


def _tod_distance() -> float:
    """Estimate distance (nm) needed to descend from cruise to ~2 000 ft."""
    DT = 30
    alt, dist = float(CRUISE_ALT_FT), 0.0
    while alt > 2_000:
        dr = interp(PERF["desc_rate_fpm"], alt)
        spd = (mach_to_tas(PERF["desc_mach"], alt) if alt >= 28_000
               else cas_to_tas(PERF["desc_cas_kt"], alt))
        alt = max(alt - dr / 60 * DT, 2_000)
        dist += spd / 3600 * DT
    return dist


def compute_trajectory(waypoints: list[str], dep_time_str: str = "20:00") -> pd.DataFrame:
    """
    Simulate a 4D trajectory along the given waypoint sequence.

    Returns a DataFrame with columns:
        time, lat, lon, altitude, fl, speed_tas, mach, phase, dist_nm
    Each row represents a 30-second snapshot.
    """
    # Build (name, lat, lon) list, skipping any unresolved waypoints
    coords = [(wp, *get_coords(wp)) for wp in waypoints if get_coords(wp)]
    if len(coords) < 2:
        return pd.DataFrame()

    # Segment distances and cumulative sums
    segs = [haversine_nm(coords[i][1], coords[i][2], coords[i+1][1], coords[i+1][2])
            for i in range(len(coords) - 1)]
    total_nm = sum(segs)

    # Top-of-climb and top-of-descent distances
    dep_elev = AIRPORTS.get(waypoints[0], {}).get("elev", 500) or 500
    toc_dist = _toc_distance(dep_elev)
    tod_dist = total_nm - _tod_distance()

    # Parse departure time
    hh, mm = map(int, dep_time_str.split(":"))
    t0 = datetime.now().replace(hour=hh, minute=mm, second=0, microsecond=0)

    DT      = 30          # seconds per simulation step
    MAX_STEPS = 12_000    # safety ceiling
    alt     = float(dep_elev)
    dist_flown = 0.0
    elapsed    = 0.0
    rows       = []

    for _ in range(MAX_STEPS):
        if dist_flown >= total_nm:
            break

        # ── Determine flight phase ─────────────────────────────────────────
        if alt < CRUISE_ALT_FT - 50 and dist_flown < toc_dist * 1.05:
            phase = "climb"
        elif dist_flown >= tod_dist:
            phase = "descent"
        else:
            phase = "cruise"

        # ── Speed and altitude update ──────────────────────────────────────
        if phase == "climb":
            spd = (cas_to_tas(PERF["climb_cas_lo_kt"], alt) if alt < 10_000
                   else cas_to_tas(PERF["climb_cas_hi_kt"], alt) if alt < 28_000
                   else mach_to_tas(PERF["cruise_mach"] * 0.97, alt))
            alt = min(alt + interp(PERF["climb_rate_fpm"], alt) / 60 * DT, CRUISE_ALT_FT)

        elif phase == "cruise":
            spd = mach_to_tas(PERF["cruise_mach"], alt)

        else:  # descent
            spd = (mach_to_tas(PERF["desc_mach"], alt) if alt >= 28_000
                   else cas_to_tas(PERF["desc_cas_kt"], alt))
            arr_elev = AIRPORTS.get(waypoints[-1], {}).get("elev", 500) or 500
            alt = max(alt - interp(PERF["desc_rate_fpm"], alt) / 60 * DT, arr_elev)

        spd = max(spd, 150)   # floor to avoid stall in edge cases

        # ── Position along route ───────────────────────────────────────────
        dist_flown = min(dist_flown + spd / 3600 * DT, total_nm)
        rem = dist_flown
        clat, clon = coords[0][1], coords[0][2]
        for i, seg in enumerate(segs):
            if rem <= seg:
                f = rem / seg if seg > 0 else 0
                clat = coords[i][1] + (coords[i+1][1] - coords[i][1]) * f
                clon = coords[i][2] + (coords[i+1][2] - coords[i][2]) * f
                break
            rem -= seg
        else:
            clat, clon = coords[-1][1], coords[-1][2]

        mach = spd / mach_to_tas(1.0, alt)
        t_now = t0 + timedelta(seconds=elapsed)

        rows.append({
            "time":      t_now.strftime("%H:%M:%S"),
            "lat":       round(clat, 4),
            "lon":       round(clon, 4),
            "altitude":  round(alt),
            "fl":        round(alt / 100),
            "speed_tas": round(spd),
            "mach":      round(mach, 3),
            "phase":     phase,
            "dist_nm":   round(dist_flown, 1),
        })
        elapsed += DT

    return pd.DataFrame(rows)
