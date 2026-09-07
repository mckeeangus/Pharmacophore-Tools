"""Render a linear GIF/MP4 of the pharmacophore-construction method.

Slide-deck companion to ``pharmacophore_method.html`` (same palette, same 9
stages). Stylised schematic cartoons, not real coordinates. The payoff is the
nicotinic three-point model (cation + aromatic + acceptor).

Run with pixi (matplotlib + pillow live in the ``ph4`` feature)::

    pixi run -e ph4 python docs/method_animation/render_animation.py

Writes ``pharmacophore_method.gif`` (always) and ``pharmacophore_method.mp4``
(only if an ffmpeg writer is available) next to this script.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, FancyArrow, RegularPolygon

# ---------------------------------------------------------------- palette ----
FAM = {
    "cation":   "#FF0000",
    "aromatic": "#FFD900",
    "acceptor": "#00CC00",
    "donor":    "#FF66B2",
    "hydro":    "#00E5E5",
    "anion":    "#FF7300",
    "excl":     "#8C8C8C",
}
# dark "molecular viewer" theme (matches the artifact's dark tokens)
BG = "#0f1521"
PANEL = "#151d2b"
INK = "#e7ecf6"
SUB = "#9aa7bd"
FAINT = "#6b7890"
GRID = "#1b2436"
BOND = "#aabaddAA"
ACCENT = "#5b93ff"

STAGES = [
    ("DrugCLIP hit set",
     "Take the top-N compounds by DrugCLIP score."),
    ("Conformer generation & energy filtering",
     "Fan each hit into an ETKDG ensemble; discard strained high-energy conformers."),
    ("Initialisation - seedless (default)",
     "Top-ranked compound's lowest-energy conformer sets the reference frame."),
    ("Iterative feature-clique alignment",
     "Match same-type features on internal distances (a clique), then Kabsch."),
    ("EM refinement",
     "Re-align every compound to the consensus, re-pick best conformer; the cloud tightens."),
    ("Directional matching",
     "Match donor/acceptor orientation - resolve a ring-flipped acceptor."),
    ("Abstraction to features",
     "Drop atoms and bonds; keep the typed pharmacophore feature points."),
    ("Clustering - Gaussian KDE",
     "Molecule-weighted occupancy field; peaks kept, low-support scatter filtered."),
    ("Nicotinic three-point model",
     "Cationic centre + aromatic ring + H-bond acceptor (~5.0 A). Excluded volume not drawn."),
]
N = len(STAGES)

# conserved 3-point core (local units ~ Angstrom); cation-acceptor ~ 5.0
CORE = {"cation": (-2.3, 1.05), "aromatic": (0.15, 1.75), "acceptor": (2.3, -0.95)}


def build_compounds(seed: int = 20240906):
    rng = np.random.default_rng(seed)
    comps = []
    for i in range(6):
        feats = []
        for k in ("cation", "aromatic", "acceptor"):
            feats.append(dict(fam=k, core=True,
                              x=CORE[k][0] + rng.uniform(-0.21, 0.21),
                              y=CORE[k][1] + rng.uniform(-0.21, 0.21)))
        for _ in range(int(rng.integers(1, 4))):
            fam = rng.choice(["hydro", "donor", "hydro", "acceptor"])
            feats.append(dict(fam=fam, core=False,
                              x=rng.uniform(-3.6, 3.6), y=rng.uniform(-2.8, 2.8)))
        res = rng.uniform(-0.85, 0.85, size=(len(feats), 2))
        comps.append(dict(
            id=i, rank=i + 1, score=round(0.94 - i * 0.06, 2),
            feats=feats, res=res,
            u=dict(ang=rng.uniform(-0.57, 0.57), dx=rng.uniform(-1.5, 1.5),
                   dy=rng.uniform(-1.1, 1.1)),
            flip=(i == 2),
        ))
    return comps


COMPS = build_compounds()

ease = lambda t: (2 * t * t) if t < 0.5 else (1 - (-2 * t + 2) ** 2 / 2)
clamp = lambda t, a=0.0, b=1.0: max(a, min(b, t))
lerp = lambda a, b, t: a + (b - a) * t
seg = lambda t, a, b: clamp((t - a) / (b - a))


def pose(f, ang, dx, dy):
    c, s = np.cos(ang), np.sin(ang)
    return f["x"] * c - f["y"] * s + dx, f["x"] * s + f["y"] * c + dy


# ------------------------------------------------------------- primitives ----
def dot(ax, x, y, fam, r, alpha=1.0, dim=False):
    col = FAM[fam]
    ax.add_patch(Circle((x, y), r, color=col, alpha=alpha * (0.5 if dim else 1.0),
                        zorder=6, ec="white", lw=0.8))


def ring(ax, x, y, rad, alpha=1.0):
    ax.add_patch(RegularPolygon((x, y), 6, radius=rad, orientation=np.pi / 6,
                                fill=False, ec=FAM["aromatic"], lw=2.0,
                                alpha=alpha, zorder=5))


def draw_compound(ax, c, ox, oy, u, ang=0, dx=0, dy=0, rscale=0.0, alpha=1.0,
                  show_ring=True, show_bonds=True, dot_r=None, directions=False,
                  flipv=0.0, only_core=False):
    dot_r = dot_r if dot_r is not None else u * 0.34
    P, pts = {}, []
    for idx, f in enumerate(c["feats"]):
        if only_core and not f["core"]:
            continue
        lx, ly = pose(f, ang, dx, dy)
        lx += c["res"][idx, 0] * rscale
        ly += c["res"][idx, 1] * rscale
        px, py = ox + lx * u, oy + ly * u
        pts.append((f, px, py))
        if f["core"]:
            P[f["fam"]] = (px, py)
    if show_bonds and "aromatic" in P:
        for f, px, py in pts:
            if f["core"] and f["fam"] != "aromatic":
                ax.plot([P["aromatic"][0], px], [P["aromatic"][1], py],
                        color=BOND, lw=1.4, alpha=alpha * 0.9, zorder=4)
    if show_ring and "aromatic" in P:
        ring(ax, *P["aromatic"], u * 0.72, alpha * 0.9)
    for f, px, py in pts:
        dot(ax, px, py, f["fam"], dot_r if f["core"] else dot_r * 0.8,
            alpha, dim=not f["core"])
    if directions:
        for f, px, py in pts:
            if f["fam"] == "acceptor" and "aromatic" in P:
                vx, vy = px - P["aromatic"][0], py - P["aromatic"][1]
                if c["flip"]:
                    sign = lerp(-1, 1, flipv)
                    vx, vy = sign * vx, sign * vy
                nrm = np.hypot(vx, vy) or 1
                ax.add_patch(FancyArrow(px, py, vx / nrm * u * 0.7, vy / nrm * u * 0.7,
                             width=0.4, head_width=3.5, color=FAM["acceptor"],
                             alpha=alpha, zorder=7, length_includes_head=True))
            if f["fam"] == "donor":
                ax.add_patch(FancyArrow(px, py, u * 0.25, u * 0.55, width=0.35,
                             head_width=3, color=FAM["donor"], alpha=alpha * 0.9,
                             zorder=7, length_includes_head=True))
    return P


def grid_anchors(ax_w, ax_h):
    xs = np.linspace(ax_w * 0.20, ax_w * 0.80, 3)
    ys = np.linspace(ax_h * 0.70, ax_h * 0.32, 2)
    return [(xs[i % 3], ys[i // 3]) for i in range(6)]


# ---------------------------------------------------------------- stages -----
def stage1(ax, t, W, H):
    A = grid_anchors(W, H); u = min(W, H) / 26
    ax.text(W * 0.5, H * 0.93, "DrugCLIP rank", color=FAINT, ha="center", fontsize=10,
            family="monospace")
    for i, c in enumerate(COMPS):
        app = ease(clamp(t * 1.5 - i * 0.12))
        if app <= 0:
            continue
        ox, oy = A[i]
        draw_compound(ax, c, ox, oy - (1 - app) * 12, u, alpha=app)
        ax.text(ox - u * 1.9, oy + u * 1.6, f"#{c['rank']}", color=SUB, fontsize=10,
                family="monospace", weight="bold", alpha=app)
        bw = u * 2.4
        ax.add_patch(plt.Rectangle((ox - bw / 2, oy - u * 1.8), bw, 3, color=GRID, alpha=app))
        ax.add_patch(plt.Rectangle((ox - bw / 2, oy - u * 1.8),
                     bw * (0.55 + 0.42 * (len(COMPS) - i) / len(COMPS)), 3,
                     color=ACCENT, alpha=app))


def stage2(ax, t, W, H):
    A = grid_anchors(W, H); u = min(W, H) / 26
    fan, cull = seg(t, 0, 0.42), seg(t, 0.5, 1)
    rng = np.random.default_rng(7)
    for i, c in enumerate(COMPS):
        ox, oy = A[i]
        for k in range(3):
            keep = k == 0
            off = (k - 1) * u * 1.15 * fan
            a = (0.5 + 0.5 * fan) if keep else (0.45 + 0.25 * fan) * (1 - cull)
            if a <= 0.03:
                continue
            draw_compound(ax, c, ox + off, oy, u * 0.9,
                          ang=rng.uniform(-0.25, 0.25), alpha=a)
            if not keep:
                ax.text(ox + off, oy - u * 1.7, "dE^", color="#FF6666",
                        alpha=a, fontsize=9, ha="center", family="monospace")
        if cull > 0.6:
            ax.text(ox, oy + u * 1.85, "min-E kept", color=FAINT, fontsize=8,
                    ha="center", family="monospace")
    ax.text(W * 0.5, H * 0.93, "fan out -> discard strained conformers", color=FAINT,
            ha="center", fontsize=10, family="monospace")


def stage3(ax, t, W, H):
    u = min(W, H) / 13; cx, cy = W * 0.5, H * 0.5
    A = grid_anchors(W, H); move = ease(t)
    for i, c in enumerate(COMPS):
        if i == 0:
            continue
        gx, gy = A[i]
        draw_compound(ax, c, gx, gy, min(W, H) / 26, alpha=(1 - move) * 0.5)
    gx, gy = A[0]
    draw_compound(ax, COMPS[0], lerp(gx, cx, move), lerp(gy, cy, move),
                  lerp(min(W, H) / 26, u, move))
    if move > 0.5:
        a = (move - 0.5) * 2
        ax.add_patch(plt.Rectangle((cx - u * 3.4, cy - u * 3.0), u * 6.8, u * 6.0,
                     fill=False, ec=ACCENT, ls="--", lw=1.3, alpha=a))
        ax.text(cx, cy + u * 3.4, "reference frame  -  rank #1 lowest-energy conformer",
                color=ACCENT, ha="center", fontsize=10, family="monospace", alpha=a)


def stage4(ax, t, W, H):
    u = min(W, H) / 13; cx, cy = W * 0.5, H * 0.5
    baseP = draw_compound(ax, COMPS[0], cx, cy, u, alpha=0.95)
    per = 1 / (len(COMPS) - 1)
    for i in range(1, len(COMPS)):
        prog = seg(t, (i - 1) * per, (i - 1) * per + per * 0.96)
        if prog <= 0:
            continue
        c = COMPS[i]; snap = ease(prog)
        ang = lerp(c["u"]["ang"], 0, snap); dx = lerp(c["u"]["dx"], 0, snap)
        dy = lerp(c["u"]["dy"], 0, snap); rs = lerp(1.0, 0.42, snap)
        P = draw_compound(ax, c, cx, cy, u, ang=ang, dx=dx, dy=dy, rscale=rs,
                          alpha=0.35 + 0.6 * snap)
        if prog < 0.85:
            vis = clamp(1 - abs(prog - 0.4) / 0.4)
            for k in ("cation", "aromatic", "acceptor"):
                if k in P and k in baseP:
                    ax.plot([P[k][0], baseP[k][0]], [P[k][1], baseP[k][1]],
                            color=FAM[k], ls=(0, (2, 3)), lw=1.3, alpha=vis * 0.8, zorder=3)
    if {"cation", "acceptor"} <= baseP.keys():
        a, b = baseP["cation"], baseP["acceptor"]
        ax.plot([a[0], b[0]], [a[1], b[1]], color=SUB, ls=(0, (2, 3)), lw=1.4, alpha=0.9)
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 14, "match on internal distances",
                color=FAINT, ha="center", fontsize=9, family="monospace")
    done = min(int(clamp(t) * (len(COMPS) - 1)) + 1, len(COMPS))
    ax.text(W * 0.5, H * 0.94, f"clique + Kabsch  -  consensus updating  ({done}/{len(COMPS)})",
            color=FAINT, ha="center", fontsize=10, family="monospace")


def stage5(ax, t, W, H):
    u = min(W, H) / 13; cx, cy = W * 0.5, H * 0.5
    rs = lerp(0.42, 0.06, ease(clamp(t)))
    for i, c in enumerate(COMPS):
        draw_compound(ax, c, cx, cy, u, rscale=rs, alpha=0.95 if i == 0 else 0.7)
    it = min(int(t * 2) + 1, 2)
    ax.text(W * 0.5, H * 0.94, f"EM refinement  -  re-align to consensus  -  pass {it}/2",
            color=FAINT, ha="center", fontsize=10, family="monospace")


def stage6(ax, t, W, H):
    u = min(W, H) / 13; cx, cy = W * 0.5, H * 0.5
    flip = ease(seg(t, 0.35, 0.9))
    for c in COMPS:
        draw_compound(ax, c, cx, cy, u, rscale=0.06,
                      alpha=0.95 if c["flip"] else 0.55, directions=True,
                      flipv=flip if c["flip"] else 1.0)
    if t < 0.5:
        ax.text(W * 0.5, H * 0.94, "ring-flipped acceptor - orientation mismatch",
                color="#FF6666", ha="center", fontsize=10, family="monospace")
    else:
        ax.text(W * 0.5, H * 0.94, "orientation matched - acceptor vector corrected",
                color=FAM["acceptor"], ha="center", fontsize=10, family="monospace")


def stage7(ax, t, W, H):
    u = min(W, H) / 13; cx, cy = W * 0.5, H * 0.5
    dis = ease(t)
    for c in COMPS:
        draw_compound(ax, c, cx, cy, u, rscale=0.06,
                      show_ring=dis < 0.6, show_bonds=dis < 0.6, dot_r=u * 0.30)
    ax.text(W * 0.5, H * 0.94,
            "dropping atoms & bonds..." if dis < 0.6 else "typed feature point cloud",
            color=FAINT, ha="center", fontsize=10, family="monospace")


def stage8(ax, t, W, H):
    u = min(W, H) / 13; cx, cy = W * 0.5, H * 0.5
    field, filt = ease(seg(t, 0, 0.55)), seg(t, 0.6, 1)
    for c in COMPS:
        for idx, f in enumerate(c["feats"]):
            lx = f["x"] + c["res"][idx, 0] * 0.06
            ly = f["y"] + c["res"][idx, 1] * 0.06
            px, py = cx + lx * u, cy + ly * u
            noise = not f["core"]
            a = ((1 - filt) * 0.22 if noise else 0.3) * field
            if a > 0.01:
                ax.add_patch(Circle((px, py), u * (1.2 if noise else 2.0) * (0.4 + 0.6 * field),
                             color=FAM[f["fam"]], alpha=a, zorder=2, lw=0))
            da = ((1 - filt) * 0.8 + 0.05) if noise else 1.0
            dot(ax, px, py, f["fam"], u * (0.16 if noise else 0.24), da, dim=noise)
    if field > 0.7:
        for k in ("cation", "aromatic", "acceptor"):
            ax.add_patch(Circle((cx + CORE[k][0] * u, cy + CORE[k][1] * u), u * 0.9,
                         fill=False, ec=FAM[k], ls="--", lw=2, alpha=field, zorder=5))
    ax.text(W * 0.5, H * 0.94,
            "occupancy field forming..." if filt < 0.3 else "peaks kept - low-support scatter filtered",
            color=FAINT, ha="center", fontsize=10, family="monospace")


def stage9(ax, t, W, H):
    u = min(W, H) / 13; cx, cy = W * 0.5, H * 0.5
    app = ease(t)
    pts = {k: (cx + CORE[k][0] * u, cy + CORE[k][1] * u) for k in CORE}
    ev = clamp(1 - seg(t, 0.4, 0.75))
    for ex, ey in [(cx - u * 3.6, cy + u * 2.6), (cx + u * 3.4, cy - u * 2.2),
                   (cx - u * 3.2, cy - u * 2.6)]:
        ax.add_patch(Circle((ex, ey), u * 0.7, fill=False, ec=FAM["excl"], ls="--",
                     lw=1.4, alpha=ev * 0.4, zorder=2))
    ax.plot([pts["aromatic"][0], pts["cation"][0]], [pts["aromatic"][1], pts["cation"][1]],
            color=BOND, lw=1.5, alpha=app * 0.5)
    ax.plot([pts["aromatic"][0], pts["acceptor"][0]], [pts["aromatic"][1], pts["acceptor"][1]],
            color=BOND, lw=1.5, alpha=app * 0.5)
    ring(ax, *pts["aromatic"], u * 0.72, app * 0.55)
    for k, nm, sup in [("cation", "Cation", "0.9"), ("aromatic", "Aromatic", "1.0"),
                       ("acceptor", "Acceptor +", "0.6")]:
        px, py = pts[k]; R = u * 1.25 * app
        ax.add_patch(Circle((px, py), R, fill=False, ec=FAM[k], lw=1.6, alpha=app, zorder=6))
        ax.add_patch(Circle((px, py), R, color=FAM[k], alpha=0.14 * app, zorder=2, lw=0))
        dot(ax, px, py, k, u * 0.2, app)
        ax.text(px, py + R + 12, nm, color=FAM[k], ha="center", fontsize=11,
                weight="bold", family="monospace", alpha=app)
        ax.text(px, py - R - 10, f"support {sup}", color=FAINT, ha="center",
                fontsize=8, family="monospace", alpha=app)
    if app > 0.5:
        a, b = pts["cation"], pts["acceptor"]; aa = (app - 0.5) * 2
        ax.plot([a[0], b[0]], [a[1], b[1]], color=SUB, ls="--", lw=1.4, alpha=aa)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ax.text(mx, my, "5.0 A", color=INK, ha="center", va="center", fontsize=11,
                weight="bold", family="monospace",
                bbox=dict(boxstyle="round,pad=0.25", fc=BG, ec="none"), alpha=aa)
    if ev < 0.2:
        ax.text(W * 0.5, H * 0.94, "excluded-volume markers: in model, not drawn",
                color=FAINT, ha="center", fontsize=9, family="monospace")


RENDER = [stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8, stage9]
FRAMES_PER = [16, 20, 14, 30, 18, 22, 16, 22, 22]
HOLD = 10  # extra held frames at the end of each stage

# expand (stage, t) schedule
SCHED = []
for s, nf in enumerate(FRAMES_PER):
    for k in range(nf):
        SCHED.append((s, k / (nf - 1)))
    SCHED += [(s, 1.0)] * HOLD

W, H = 100.0, 56.0  # logical canvas


def setup_axes(ax):
    ax.clear()
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), W, H, color=BG, zorder=0))
    for x in np.arange(3, W, 7):
        ax.plot([x, x], [0, H], color=GRID, lw=0.6, zorder=1)
    for y in np.arange(3, H, 7):
        ax.plot([0, W], [y, y], color=GRID, lw=0.6, zorder=1)


def main():
    here = Path(__file__).resolve().parent
    fig = plt.figure(figsize=(9.6, 6.0), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0.12, 1, 0.82])       # canvas
    cap = fig.add_axes([0, 0, 1, 0.12]); cap.axis("off")
    cap.set_facecolor(PANEL)

    def frame(fi):
        s, t = SCHED[fi]
        setup_axes(ax)
        RENDER[s](ax, t, W, H)
        cap.clear(); cap.axis("off")
        cap.add_patch(plt.Rectangle((0, 0), 1, 1, color=PANEL, zorder=0,
                      transform=cap.transAxes))
        cap.text(0.018, 0.5, f"{s + 1:02d}", color=ACCENT, fontsize=15, weight="bold",
                 family="monospace", va="center", ha="left", transform=cap.transAxes)
        cap.text(0.06, 0.66, STAGES[s][0], color=INK, fontsize=12.5, weight="bold",
                 va="center", ha="left", transform=cap.transAxes)
        cap.text(0.06, 0.28, STAGES[s][1], color=SUB, fontsize=9.5, va="center",
                 ha="left", transform=cap.transAxes)
        # progress ticks
        for i in range(N):
            col = ACCENT if i <= s else FAINT
            cap.add_patch(plt.Rectangle((0.70 + i * 0.028, 0.44), 0.02, 0.12,
                          color=col, alpha=1 if i <= s else 0.4, transform=cap.transAxes))
        return []

    anim = FuncAnimation(fig, frame, frames=len(SCHED), interval=55, blit=False)

    gif_path = here / "pharmacophore_method.gif"
    anim.save(gif_path, writer=PillowWriter(fps=18))
    print(f"[ok] wrote {gif_path}  ({gif_path.stat().st_size/1e6:.1f} MB)")

    mp4_path = here / "pharmacophore_method.mp4"
    try:
        from matplotlib.animation import FFMpegWriter
        # Fall back to imageio-ffmpeg's bundled static binary when no system
        # ffmpeg is on PATH (avoids the full conda ffmpeg + its AV-locked binary).
        if not FFMpegWriter.isAvailable():
            try:
                import imageio_ffmpeg
                matplotlib.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
            except Exception:
                pass
        if FFMpegWriter.isAvailable():
            anim.save(mp4_path, writer=FFMpegWriter(fps=18, bitrate=2400))
            print(f"[ok] wrote {mp4_path}  ({mp4_path.stat().st_size/1e6:.1f} MB)")
        else:
            print("[skip] ffmpeg not available - MP4 not written")
    except Exception as exc:  # pragma: no cover
        print(f"[skip] MP4 failed: {exc}")

    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
