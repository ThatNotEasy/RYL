#!/usr/bin/env python3
# coordinator.py — Calibrate, mark & LIVE X/Y on map.png

import argparse, json, os, re, sys
from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ===== Default map =====
DEFAULT_MAP = "map.png"

# ===== Fallback (if you skip calibration) =====
# X increases to the right. Y increases toward the TOP (going down decreases Y).
WORLD_BOUNDS = dict(x_min=700, x_max=3500, y_min=900, y_max=3400)
ROI_PADDING  = dict(top=0.07, bottom=0.06, left=0.02, right=0.02)

@dataclass
class Calib:
    A: list
    img_w: int
    img_h: int
    anchors: list

# ---------- Parsing ----------
def parse_xy(s: str) -> Tuple[int, int]:
    nums = re.findall(r"-?\d+", s)
    if len(nums) != 2:
        raise argparse.ArgumentTypeError('Use exactly two ints, e.g. "1115, 2547"')
    return int(nums[0]), int(nums[1])

def parse_xy_list(s: str) -> List[Tuple[int, int]]:
    return [parse_xy(p.strip()) for p in s.split(";") if p.strip()]

def find_map(custom: str | None) -> str:
    path = custom or DEFAULT_MAP
    if os.path.exists(path):
        return path
    raise FileNotFoundError(f"Map image not found: {path}. Place map as '{DEFAULT_MAP}' or pass -m PATH.")

# ---------- Geometry ----------
def compute_roi(im_w: int, im_h: int, pad: dict) -> Tuple[int,int,int,int]:
    L = int(im_w * pad["left"]); R = int(im_w * (1 - pad["right"]))
    T = int(im_h * pad["top"]);  B = int(im_h * (1 - pad["bottom"]))
    return (L, T, R - L, B - T)  # left, top, width, height

def fit_affine(world_pts: List[Tuple[float,float]], pix_pts: List[Tuple[float,float]]) -> np.ndarray:
    if len(world_pts) != len(pix_pts) or len(world_pts) < 3:
        raise ValueError("Need >=3 matching points to solve affine transform.")
    M, b = [], []
    for (x,y),(u,v) in zip(world_pts, pix_pts):
        M += [[x,y,1,0,0,0],[0,0,0,x,y,1]]
        b += [u, v]
    sol, *_ = np.linalg.lstsq(np.asarray(M,float), np.asarray(b,float), rcond=None)
    return np.array([[sol[0], sol[1], sol[2]], [sol[3], sol[4], sol[5]]], dtype=float)

def apply_affine(A: np.ndarray, x: float, y: float) -> Tuple[int,int]:
    u, v = A @ np.array([x, y, 1.0], dtype=float)
    return int(round(u)), int(round(v))

def invert_affine(A_2x3: np.ndarray) -> np.ndarray:
    """Return 3x3 inverse for pixel->world: [x y 1]^T = Ainv * [u v 1]^T"""
    M = np.array([[A_2x3[0,0], A_2x3[0,1], A_2x3[0,2]],
                  [A_2x3[1,0], A_2x3[1,1], A_2x3[1,2]],
                  [0,          0,          1         ]], dtype=float)
    return np.linalg.inv(M)

def pixel_to_world_fallback(px: int, py: int, roi: Tuple[int,int,int,int], bounds: dict) -> Tuple[int,int]:
    L,T,W,H = roi
    # normalize inside ROI
    xr = (px - L) / max(W, 1)
    yr = 1.0 - ((py - T) / max(H, 1))  # invert because pixels grow downward
    x = bounds["x_min"] + xr * (bounds["x_max"] - bounds["x_min"])
    y = bounds["y_min"] + yr * (bounds["y_max"] - bounds["y_min"])
    return int(round(x)), int(round(y))

# ---------- Calibration IO ----------
def collect_clicks(img_path: str, n: int) -> List[Tuple[int,int]]:
    import tkinter as tk
    from PIL import ImageTk
    im = Image.open(img_path).convert("RGBA"); W,H = im.size
    root = tk.Tk(); root.title(f"Click {n} points (in order)")
    tk_im = ImageTk.PhotoImage(im)
    c = tk.Canvas(root, width=W, height=H); c.pack()
    c.create_image(0, 0, anchor=tk.NW, image=tk_im)
    clicks = []; r = max(4, min(W,H)//150)
    def on_click(e):
        clicks.append((e.x, e.y))
        c.create_oval(e.x-r, e.y-r, e.x+r, e.y+r, outline="#00ffff", width=2)
        if len(clicks) >= n: root.destroy()
    c.bind("<Button-1>", on_click)
    tk.Label(root, text=f"Click {n} blue squares in the same order as your coords. Press ESC to cancel.").pack()
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()
    if len(clicks) != n: raise RuntimeError(f"Expected {n} clicks, got {len(clicks)}")
    return clicks

def save_calib(path: str, A: np.ndarray, W: int, H: int, w_a, p_a):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"type":"affine","A":A.tolist(),"img_w":W,"img_h":H,
                   "anchors":[{"world":list(w),"pixel":list(p)} for w,p in zip(w_a,p_a)]}, f, indent=2)

def load_calib(path: str) -> Calib:
    with open(path, "r", encoding="utf-8") as f: d = json.load(f)
    if d.get("type")!="affine": raise ValueError("Unsupported calibration type.")
    return Calib(A=d["A"], img_w=d["img_w"], img_h=d["img_h"], anchors=d.get("anchors", []))

# ---------- Drawing ----------
def draw_marker(im: Image.Image, xy: Tuple[int,int], label: str) -> None:
    W,H = im.size; draw = ImageDraw.Draw(im, "RGBA")
    cross_len = max(10, int(min(W, H) * 0.018)); thickness = max(2, int(min(W, H) * 0.003))
    x,y = xy
    draw.line((x - cross_len, y, x + cross_len, y), fill=(255, 50, 50, 255), width=thickness)
    draw.line((x, y - cross_len, x, y + cross_len), fill=(255, 50, 50, 255), width=thickness)
    r = cross_len // 2
    draw.ellipse((x - r, y - r, x + r, y + r), outline=(255,255,255,240), width=thickness)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", size=max(14, int(min(W,H)*0.03)))
    except Exception:
        font = ImageFont.load_default()
    tw, th = draw.textbbox((0,0), label, font=font)[2:]; pad = 6
    bx, by = x + cross_len + 8, y - th // 2 - pad
    draw.rectangle((bx, by, bx + tw + 2*pad, by + th + 2*pad), fill=(0,0,0,180),
                   outline=(255,255,255,200), width=1)
    draw.text((bx + pad, by + pad), label, font=font, fill=(255,255,255,255))

# ---------- LIVE mode ----------
def live_readout(map_path: str, calib_path: str | None):
    import tkinter as tk
    from PIL import ImageTk

    im = Image.open(map_path).convert("RGBA")
    W,H = im.size
    tk_im = ImageTk.PhotoImage(im)

    A = None
    Ainv = None
    if calib_path:
        calib = load_calib(calib_path)
        A = np.array(calib.A, dtype=float)
        Ainv = invert_affine(A)
    else:
        roi = compute_roi(W, H, ROI_PADDING)

    root = tk.Tk()
    root.title("RYL2 Map — LIVE X,Y (Esc to quit)")

    canvas = tk.Canvas(root, width=W, height=H)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_im)

    # crosshair items (updated on motion)
    cross_h = canvas.create_line(0,0,0,0, fill="#ff5050", width=2)
    cross_v = canvas.create_line(0,0,0,0, fill="#ff5050", width=2)
    ring    = canvas.create_oval(0,0,0,0, outline="#ffffff", width=2)

    status = tk.StringVar(value="Move mouse over the map…")
    label  = tk.Label(root, textvariable=status, font=("Consolas", 12))
    label.pack()

    def on_motion(e):
        px, py = e.x, e.y
        # Compute world X,Y
        if Ainv is not None:
            x, y, _ = Ainv @ np.array([px, py, 1.0], dtype=float)
            wx, wy = int(round(x)), int(round(y))
            inside = 0 <= px < W and 0 <= py < H
        else:
            L,T,WW,HH = roi
            inside = (L <= px <= L+WW) and (T <= py <= T+HH)
            wx, wy = pixel_to_world_fallback(px, py, roi, WORLD_BOUNDS)

        # update crosshair
        c = 12
        canvas.coords(cross_h, px-c, py, px+c, py)
        canvas.coords(cross_v, px, py-c, px, py+c)
        canvas.coords(ring, px-6, py-6, px+6, py+6)

        status.set(f"Pixel: ({px:4d}, {py:4d})   World: ({wx:4d}, {wy:4d})   "
                   + ("IN" if inside else "OUT"))

    def close(_=None):
        root.destroy()

    canvas.bind("<Motion>", on_motion)
    root.bind("<Escape>", close)
    root.mainloop()

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="RYL2 map tools: calibrate, mark, or live X/Y readout.")
    ap.add_argument("-c","--coordinate", type=parse_xy, help='Coordinate as "X, Y"')
    ap.add_argument("-m","--map", help="Path to map image (default: map.png)")
    ap.add_argument("-o","--output", help="Output image path (default: RYL2_map_marked_X_Y.png)")
    ap.add_argument("--calib", help="Path to a saved calibration JSON.")
    ap.add_argument("--calibrate", metavar='"x1,y1; x2,y2; ..."',
                    help="Enter world anchors; a window opens to click matching pixels in order.")
    ap.add_argument("-O","--calib-out", default="coordinator.calib.json",
                    help="Where to save calibration JSON (default: coordinator.calib.json)")
    ap.add_argument("--live", action="store_true",
                    help="Open map.png and show live X,Y while moving the mouse. Uses --calib if provided.")
    args = ap.parse_args()

    # LIVE mode
    if args.live:
        map_path = find_map(args.map)
        live_readout(map_path, args.calib)
        return

    # Calibration mode
    if args.calibrate:
        world_anchors = parse_xy_list(args.calibrate)
        map_path = find_map(args.map)
        im = Image.open(map_path).convert("RGBA")
        pix_anchors = collect_clicks(map_path, len(world_anchors))
        A = fit_affine(world_anchors, pix_anchors)
        save_calib(args.calib_out, A, *im.size, world_anchors, pix_anchors)
        print(f"[Calibrate] Saved -> {args.calib_out}")
        if not args.coordinate:
            return

    # Mark a coordinate
    if not args.coordinate:
        ap.error("No coordinate provided. Use -c \"X, Y\" (or run --live / --calibrate).")

    x, y = args.coordinate
    map_path = find_map(args.map)
    im = Image.open(map_path).convert("RGBA")

    if args.calib:
        calib = load_calib(args.calib)
        A = np.array(calib.A, dtype=float)
        px, py = apply_affine(A, x, y)
    else:
        # simple (less accurate) fallback
        W,H = im.size
        L,T,WW,HH = compute_roi(W,H,ROI_PADDING)
        xr = (x - WORLD_BOUNDS["x_min"]) / (WORLD_BOUNDS["x_max"] - WORLD_BOUNDS["x_min"])
        yr = (y - WORLD_BOUNDS["y_min"]) / (WORLD_BOUNDS["y_max"] - WORLD_BOUNDS["y_min"])
        px = L + xr * WW
        py = T + (1.0 - yr) * HH

    draw_marker(im, (int(round(px)), int(round(py))), f"({x}, {y})")
    out_path = args.output or f"RYL2_map_marked_{x}_{y}.png"
    im.save(out_path)
    print(f"Saved -> {out_path}")

if __name__ == "__main__":
    main()
