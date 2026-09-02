#!/usr/bin/env python3
# zdraw_layout.py — zdraw 布局计算 + SVG 渲染
#
# 用法:
#   python3 scripts/zdraw_layout.py spec.json -o coords.json [--svg out.svg] [--style diagram-style.md]
#
# spec JSON:
#   {
#     "layout": "hierarchy" | "sequence" | "grid",   # 架构/流程/树 | 时序 | 泳道/层栈
#     "direction": "TB" | "LR",                      # hierarchy 用,默认 TB
#     "nodes": [{"id":"api","label":"API 网关","kind":"normal|focal|store|external"}...],
#     "edges": [{"from":"api","to":"db","label":"查询","style":"solid|dashed"}...],
#     # sequence 专用: nodes 按顺序即生命线序;edges 顺序即消息序
#     # grid 专用: node.lane = 泳道/层索引(0 起)
#     "lanes": ["前端","后端"]                        # grid 用(可选)
#   }
#
# 输出 coords.json:
#   {"canvas":{"w":..,"h":..},"nodes":{"api":{"x":..,"y":..,"w":..,"h":..}}, "svg_inner": "..."}
#
# 硬规则内联(见 skills/zdraw/references/layout-rules.md):4px 网格、间距阶梯、
# 正交圆角连线(r=8)、标签遮罩留隙 8px、箭头先画节点后画、复杂度预算 ≤9 节点 ≤12 边。
import json, re, sys, argparse

# ---------- 4px 网格常数 ----------
G = 4
NODE_W, NODE_H = 160, 48          # 标准盒
GAP_X, GAP_Y = 80, 64             # 同层水平距 / 跨层垂直距
MARGIN = 40
R = 8                             # 连线圆角
LABEL_GAP = 8                     # 标签遮罩与连线间隙
MAX_NODES, MAX_EDGES = 9, 12

FONTS = {"sans": "Inter, system-ui, sans-serif", "mono": "Geist Mono, monospace"}
INK, MUTED, PAPER, RULE, ACCENT = "#0b0c0e", "#8a8f98", "#ffffff", "rgba(11,12,14,0.10)", "#5e6ad2"

def g4(v):  # 吸附 4px 网格
    return int(round(v / G)) * G

def grid(x, y, w=NODE_W, h=NODE_H):
    return g4(x), g4(y), g4(w), g4(h)

# ---------- 布局算法 ----------
def layout_hierarchy(spec):
    """层序:无入边的在前,子节点随父层 +1(LR 则旋转 90°)。"""
    nodes, edges = spec["nodes"], spec.get("edges", [])
    ids = [n["id"] for n in nodes]
    level = {i: 0 for i in ids}
    indeg = {i: 0 for i in ids}
    children = {i: [] for i in ids}
    for e in edges:
        indeg[e["to"]] += 1
        children[e["from"]].append(e["to"])
    queue = [i for i in ids if indeg[i] == 0]
    seen = set()
    while queue:
        cur = queue.pop(0)
        if cur in seen: continue
        seen.add(cur)
        for ch in children[cur]:
            level[ch] = max(level[ch], level[cur] + 1)
            indeg[ch] -= 1
            if indeg[ch] == 0: queue.append(ch)
    # 分层内水平排布
    layers = {}
    for i in ids: layers.setdefault(level[i], []).append(i)
    coords, pos = {}, {}
    if spec.get("direction", "TB") == "LR":
        for lv, members in sorted(layers.items()):
            for k, nid in enumerate(members):
                x, y, w, h = grid(MARGIN + lv * (NODE_W + GAP_X),
                                  MARGIN + k * (NODE_H + G * 6))
                coords[nid] = {"x": x, "y": y, "w": w, "h": h}
    else:
        for lv, members in sorted(layers.items()):
            for k, nid in enumerate(members):
                x, y, w, h = grid(MARGIN + k * (NODE_W + GAP_X),
                                  MARGIN + lv * (NODE_H + GAP_Y))
                coords[nid] = {"x": x, "y": y, "w": w, "h": h}
    return coords

def layout_sequence(spec):
    """生命线垂直等距,消息按边序自上而下排。"""
    nodes, edges = spec["nodes"], spec.get("edges", [])
    step = NODE_H + G * 8
    top = MARGIN + 40
    coords = {}
    order = [n["id"] for n in nodes]
    for k, nid in enumerate(order):
        x, y, w, h = grid(MARGIN + k * (NODE_W + GAP_X), MARGIN, NODE_W, NODE_H)
        coords[nid] = {"x": x, "y": y, "w": w, "h": h, "lifeline_to": g4(top + len(edges) * step + 40)}
    return coords

def layout_grid(spec):
    """泳道/层栈:node.lane 决定行(lanes 提供标签),列按出现序。"""
    coords, col = {}, {}
    for n in spec["nodes"]:
        lane = int(n.get("lane", 0))
        c = col.get(lane, 0)
        col[lane] = c + 1
        x, y, w, h = grid(MARGIN + c * (NODE_W + GAP_X),
                          MARGIN + lane * (NODE_H + G * 10))
        coords[n["id"]] = {"x": x, "y": y, "w": w, "h": h}
    return coords

LAYOUTS = {"hierarchy": layout_hierarchy, "sequence": layout_sequence, "grid": layout_grid}

# ---------- SVG 渲染(正交圆角 + 标签遮罩 + 箭头三件套;箭头先画节点后画) ----------
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def orthogonal_path(a, b):
    """肘线路径 + 拐角 r=8 圆弧;返回 path d 与标签锚点(中点)。"""
    x1, y1 = a[0], a[1]; x2, y2 = b[0], b[1]
    if abs(y1 - y2) < 1:  # 同轴水平直线
        return f"M {x1},{y1} L {x2},{y2}", (g4((x1 + x2) / 2), y1)
    if abs(x1 - x2) < 1:  # 同轴垂直直线
        return f"M {x1},{y1} L {x2},{y2}", (x1, g4((y1 + y2) / 2))
    mid = g4((y1 + y2) / 2)  # 肘形:垂直出 → 水平 → 垂直到达
    return (f"M {x1},{y1} L {x1},{mid - R} Q {x1},{mid} {x1 + R},{mid} "
            f"L {x2 - R},{mid} Q {x2},{mid} {x2},{mid + R} L {x2},{y2}",
            (g4((x1 + x2) / 2), mid))

def anchor(c, side, k=1, total=1):
    """盒边附着点:同边多条按 k/(total+1) 扇形展开。"""
    x, y, w, h = c["x"], c["y"], c["w"], c["h"]
    return {"bottom": (x + w * k // (total + 1), y + h),
            "top":    (x + w * k // (total + 1), y),
            "right":  (x + w, y + h * k // (total + 1)),
            "left":   (x, y + h * k // (total + 1))}[side]

def render_svg(spec, coords, style):
    c = {k: dict(style) for k in style} if style else {"ink": INK, "muted": MUTED, "paper": PAPER, "rule": RULE, "accent": ACCENT}
    nodes, edges = spec["nodes"], spec.get("edges", [])
    max_x = max(v["x"] + v["w"] for v in coords.values())
    max_y = max(v.get("lifeline_to", v["y"] + v["h"]) for v in coords.values())
    W, H = g4(max_x + MARGIN), g4(max_y + MARGIN + 20)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="zd-title zd-desc">',
           f'  <title id="zd-title">{esc(spec.get("title", "diagram"))}</title>',
           f'  <desc id="zd-desc">{esc(spec.get("desc", "示意流程图"))}</desc>',
           '  <defs>',
           f'    <marker id="zd-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{c["muted"]}"/></marker>',
           f'    <marker id="zd-arrow-accent" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{c["accent"]}"/></marker>',
           '  </defs>',
           f'  <rect width="{W}" height="{H}" fill="{c["paper"]}"/>']
    # —— 箭头层(先画) ——
    by_id = {n["id"]: n for n in nodes}
    outcount, outtotal = {}, {}
    for e in edges: outtotal[e["from"]] = outtotal.get(e["from"], 0) + 1
    for e in edges:
        k = outcount.get(e["from"], 0) + 1; outcount[e["from"]] = k
        a = coords[e["from"]]; b = coords[e["to"]]
        p1 = anchor(a, "bottom", k, outtotal[e["from"]]) if a["y"] < b["y"] else anchor(a, "right", k, outtotal[e["from"]])
        p2 = anchor(b, "top", 1, 1) if a["y"] < b["y"] else anchor(b, "left", 1, 1)
        d, mid = orthogonal_path(p1, p2)
        dashed = ' stroke-dasharray="4,3"' if e.get("style") == "dashed" else ""
        accent = e.get("kind") == "focal"
        color = c["accent"] if accent else c["muted"]
        marker = "zd-arrow-accent" if accent else "zd-arrow"
        out.append(f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{dashed} marker-end="url(#{marker})"/>')
        if e.get("label"):
            lx, ly = mid; lw = max(28, len(e["label"]) * 8 + 12)
            out.append(f'  <rect x="{g4(lx - lw/2)}" y="{g4(ly - 8)}" width="{g4(lw)}" height="16" fill="{c["paper"]}" opacity="0.95"/>')
            out.append(f'  <text x="{lx}" y="{ly + 4}" text-anchor="middle" font-family="{FONTS["sans"]}" font-size="10" fill="{c["muted"]}">{esc(e["label"])}</text>')
    # —— 节点层(后画,压线上) ——
    for n in nodes:
        v = coords[n["id"]]; kind = n.get("kind", "normal")
        fill, stroke = c["paper"], c["ink"]
        if kind == "focal":   fill, stroke = c["accent"], c["accent"]
        if kind == "store":   fill = "rgba(11,12,14,0.05)"
        if kind == "external": fill, stroke = "rgba(11,12,14,0.03)", "rgba(11,12,14,0.30)"
        out.append(f'  <rect x="{v["x"]}" y="{v["y"]}" width="{v["w"]}" height="{v["h"]}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        out.append(f'  <text x="{v["x"] + v["w"]//2}" y="{v["y"] + v["h"]//2 + 4}" text-anchor="middle" font-family="{FONTS["sans"]}" font-size="12" font-weight="600" fill="{c["ink"]}">{esc(n["label"])}</text>')
    out.append("</svg>")
    return "\n".join(out)

# ---------- 样式注入(diagram-style.md 语义角色) ----------
def load_style(path):
    if not path: return None
    roles = {}
    for m in re.finditer(r'^\s{2}(paper|ink|muted|soft|rule|accent|accent-tint|link):\s*"?([^"\n]+)"?', open(path).read(), re.M):
        roles[m.group(1)] = m.group(2).strip()
    if not roles: return None
    return {"paper": roles.get("paper", PAPER), "ink": roles.get("ink", INK),
            "muted": roles.get("muted", MUTED), "rule": roles.get("rule", RULE),
            "accent": roles.get("accent", ACCENT)}

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("-o", "--out", default="coords.json")
    ap.add_argument("--svg"); ap.add_argument("--style")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    n, e = len(spec["nodes"]), len(spec.get("edges", []))
    if n > MAX_NODES or e > MAX_EDGES:
        sys.exit(f"预算超限:节点 {n}/{MAX_NODES},边 {e}/{MAX_EDGES} — 拆 overview + detail 两张再跑")
    coords = LAYOUTS[spec.get("layout", "hierarchy")](spec)
    style = load_style(a.style)
    out = {"canvas": {"w": max(v["x"] + v["w"] for v in coords.values()) + MARGIN,
                      "h": max(v.get("lifeline_to", v["y"] + v["h"]) for v in coords.values()) + MARGIN},
           "nodes": coords}
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"coords → {a.out}(节点 {n},边 {e},画布 {out['canvas']['w']}×{out['canvas']['h']})")
    if a.svg:
        open(a.svg, "w").write(render_svg(spec, coords, style))
        print(f"svg    → {a.svg}")

if __name__ == "__main__":
    main()
