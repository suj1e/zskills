#!/usr/bin/env python3
# zdraw_layout.py — zdraw 布局计算 + SVG 渲染
#
# 用法:
#   python3 scripts/zdraw_layout.py spec.json -o coords.json [--svg out.svg] [--style diagram-style.md]
#
# spec JSON:
#   {
#     "title": "API 网关架构",                  # 可选,svg title
#     "desc": "一句话说明",                      # 可选,svg desc
#     "layout": "hierarchy" | "sequence" | "grid",
#     "direction": "TB" | "LR",                  # hierarchy 用,默认 TB
#     "nodes": [
#       {"id":"gw","label":"API 网关","kind":"normal|focal|store|external",
#        "lane":0}                               # lane 仅 grid 用
#     ],
#     "edges": [
#       {"from":"a","to":"b","label":"查询","style":"solid|dashed","kind":"normal|focal"}
#     ]                                          # sequence: edges 顺序 = 消息时间序
#   }
#
# 输出 coords.json: 画布尺寸 + 每节点坐标(+时序生命线信息),供手写 .excalidraw/.drawio 消费。
#
# 硬规则内联(见 skills/zdraw/references/layout-rules.md):4px 网格、正交圆角连线(r=8)、
# 标签遮罩留隙 8px、箭头先画节点后画、附着点扇形展开、复杂度预算 ≤9 节点 ≤12 边。
import json, sys, argparse

# ---------- 4px 网格常数 ----------
G = 4
NODE_H = 48
GAP_X, GAP_Y = 80, 64
MARGIN = 40
R = 8
MAX_NODES, MAX_EDGES = 9, 12
W_MIN, W_MAX = 80, 240

FONTS = {"sans": "Inter, system-ui, sans-serif", "mono": "Geist Mono, monospace"}
INK, MUTED, PAPER, ACCENT = "#0b0c0e", "#8a8f98", "#ffffff", "#5e6ad2"

def g4(v): return int(round(v / G)) * G

def text_w(label):
    """中文按 12px/字,其他按 7px/字估宽(12px 字号下)。"""
    w = sum(12 if ord(ch) > 0x2E7F else 7 for ch in label)
    return w

def node_w(label):
    return g4(max(W_MIN, min(W_MAX, text_w(label) + 40)))

# ---------- 布局算法 ----------
def layout_hierarchy(spec):
    """层序(最长路径定层),层内居中;TB 或 LR。"""
    nodes, edges = spec["nodes"], spec.get("edges", [])
    ids = [n["id"] for n in nodes]
    level = {i: 0 for i in ids}
    indeg = {i: 0 for i in ids}
    children = {i: [] for i in ids}
    for e in edges:
        if e["to"] not in level or e["from"] not in level:
            sys.exit(f"边引用未知节点: {e['from']}→{e['to']}")
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
    if len(seen) != len(ids):
        sys.exit("存在环:hierarchy 需要无环图(环状关系用 state 布局画白板)")
    layers = {}
    for n in nodes: layers.setdefault(level[n["id"]], []).append(n)
    lr = spec.get("direction", "TB") == "LR"
    coords = {}
    axis = 0
    # 先量各层总宽,取最宽层中心做公共轴
    widths = {}
    for lv, members in layers.items():
        widths[lv] = sum(node_w(m["label"]) + GAP_X for m in members) - GAP_X
    axis = g4(max(widths.values()) / 2) if lr is False else 0
    for lv, members in sorted(layers.items()):
        total = widths[lv]
        cur = g4(max(MARGIN, axis - total / 2)) if not lr else MARGIN
        for m in members:
            w = node_w(m["label"])
            if lr:
                x, y = MARGIN + lv * (NODE_W + GAP_X), cur
                coords[m["id"]] = {"x": g4(x), "y": g4(y), "w": w, "h": NODE_H}
                cur += NODE_H + G * 6
            else:
                coords[m["id"]] = {"x": cur, "y": g4(MARGIN + lv * (NODE_H + GAP_Y)),
                                   "w": w, "h": NODE_H}
                cur += w + GAP_X
    return coords

def layout_sequence(spec):
    """生命线头部等距;消息时间序决定纵向排布;返回生命线信息。"""
    order = [n["id"] for n in spec["nodes"]]
    n = len(order)
    head_gap = max(GAP_X, node_w(max((m["label"] for m in spec["nodes"]), key=len)))
    coords = {}
    for k, m in enumerate(spec["nodes"]):
        w = node_w(m["label"])
        x = g4(MARGIN + k * (w + head_gap - w + GAP_X))
        coords[m["id"]] = {"x": x, "y": MARGIN, "w": w, "h": NODE_H,
                           "cx": g4(x + w / 2), "role": "lifeline"}
    step = 56
    msgs_y0 = MARGIN + NODE_H + step // 2
    last_y = msgs_y0 + len(spec.get("edges", [])) * step
    for v in coords.values():
        v["lifeline_to"] = g4(last_y + 40)
    return coords

def layout_grid(spec):
    """泳道/层栈:node.lane 定行,列按出现序;lanes 提供车道标签。"""
    coords, col = {}, {}
    for m in spec["nodes"]:
        lane = int(m.get("lane", 0))
        c = col.get(lane, 0); col[lane] = c + 1
        w = node_w(m["label"])
        coords[m["id"]] = {"x": g4(MARGIN + c * (w + GAP_X)),
                           "y": g4(MARGIN + 32 + lane * (NODE_H + G * 10)),
                           "w": w, "h": NODE_H}
    return coords

LAYOUTS = {"hierarchy": layout_hierarchy, "sequence": layout_sequence, "grid": layout_grid}

# ---------- SVG 渲染 ----------
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def elbow(x1, y1, x2, y2):
    """跨轴肘线(圆角 r=8)或同轴直线;返回 (path d, 标签锚点)。"""
    if abs(y1 - y2) < 1:
        return f"M {x1},{y1} L {x2},{y2}", (g4((x1 + x2) / 2), y1)
    if abs(x1 - x2) < 1:
        return f"M {x1},{y1} L {x2},{y2}", (x1, g4((y1 + y2) / 2))
    mid = g4((y1 + y2) / 2)
    d = (f"M {x1},{y1} L {x1},{mid - R} Q {x1},{mid} {x1 + (R if x2 > x1 else -R)},{mid} "
         f"L {x2 - (R if x2 > x1 else -R)},{mid} Q {x2},{mid} {x2},{mid + (R if y2 > mid else -R)} L {x2},{y2}")
    return d, (g4((x1 + x2) / 2), mid)

def anchor(v, side, k=1, total=1):
    x, y, w, h = v["x"], v["y"], v["w"], v["h"]
    pts = {"bottom": (x + max(w * k // (total + 1), 12), y + h),
           "top":    (x + max(w * k // (total + 1), 12), y),
           "right":  (x + w, y + max(h * k // (total + 1), 8)),
           "left":   (x, y + max(h * k // (total + 1), 8))}
    return pts[side]

def edge_label(out, text, x, y, c):
    lw = g4(max(28, text_w(text) * 0.83 + 12))
    out.append(f'  <rect x="{g4(x - lw/2)}" y="{g4(y - 8 - LABEL_GAP/2)}" width="{lw}" height="16" fill="{c["paper"]}" opacity="0.95"/>')
    out.append(f'  <text x="{x}" y="{y + 4 - LABEL_GAP//2}" text-anchor="middle" font-family="{FONTS["sans"]}" font-size="10" fill="{c["muted"]}">{esc(text)}</text>')

LABEL_GAP = 8

def render_hierarchy_svg(spec, coords, c):
    out = []
    by_id = {n["id"]: n for n in spec["nodes"]}
    outtotal = {}
    for e in spec.get("edges", []): outtotal[e["from"]] = outtotal.get(e["from"], 0) + 1
    outcount = {}
    for e in spec.get("edges", []):
        outcount[e["from"]] = outcount.get(e["from"], 0) + 1
        k = outcount[e["from"]]
        a, b = coords[e["from"]], coords[e["to"]]
        if a["y"] + a["h"] < b["y"]:   p1, p2 = anchor(a, "bottom", k, outtotal[e["from"]]), anchor(b, "top", 1, 1)
        elif b["y"] + b["h"] < a["y"]: p1, p2 = anchor(a, "top", k, outtotal[e["from"]]), anchor(b, "bottom", 1, 1)
        elif a["x"] < b["x"]:          p1, p2 = anchor(a, "right", k, outtotal[e["from"]]), anchor(b, "left", 1, 1)
        else:                          p1, p2 = anchor(a, "left", k, outtotal[e["from"]]), anchor(b, "right", 1, 1)
        d, mid = elbow(*p1, *p2)
        focal = e.get("kind") == "focal"
        color = c["accent"] if focal else c["muted"]
        dashed = ' stroke-dasharray="4,3"' if e.get("style") == "dashed" else ""
        out.append(f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{dashed} marker-end="url(#{"zd-arrow-accent" if focal else "zd-arrow"})"/>')
        if e.get("label"): edge_label(out, e["label"], mid[0], mid[1], c)
    for m in spec["nodes"]:
        v = coords[m["id"]]; kind = m.get("kind", "normal")
        fill, stroke = c["paper"], c["ink"]
        if kind == "focal":    fill, stroke = c["accent"], c["accent"]
        elif kind == "store":  fill = "rgba(11,12,14,0.05)"
        elif kind == "external": fill, stroke = "rgba(11,12,14,0.03)", "rgba(11,12,14,0.30)"
        tcol = c["paper"] if kind == "focal" else c["ink"]
        out.append(f'  <rect x="{v["x"]}" y="{v["y"]}" width="{v["w"]}" height="{v["h"]}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        out.append(f'  <text x="{v["x"] + v["w"]//2}" y="{v["y"] + v["h"]//2 + 4}" text-anchor="middle" font-family="{FONTS["sans"]}" font-size="12" font-weight="600" fill="{tcol}">{esc(m["label"])}</text>')
    return out

def render_sequence_svg(spec, coords, c):
    out = []
    # 生命线
    for m in spec["nodes"]:
        v = coords[m["id"]]
        out.append(f'  <line x1="{v["cx"]}" y1="{v["y"] + v["h"]}" x2="{v["cx"]}" y2="{v["lifeline_to"]}" stroke="{c["rule"]}" stroke-width="1" stroke-dasharray="4,4"/>')
    msgs = spec.get("edges", [])
    step = 56
    y0 = MARGIN + NODE_H + step // 2
    for i, e in enumerate(msgs):
        y = g4(y0 + i * step)
        a, b = coords[e["from"]], coords[e["to"]]
        focal = e.get("kind") == "focal"
        color = c["accent"] if focal else c["muted"]
        dashed = ' stroke-dasharray="4,3"' if e.get("style") == "dashed" else ""
        if e["from"] == e["to"]:  # 自消息:右侧小回环
            x = a["cx"]
            out.append(f'  <path d="M {x},{y} L {x + 48},{y} L {x + 48},{y + 24} L {x + 4},{y + 24}" fill="none" stroke="{color}" stroke-width="1.5"{dashed} marker-end="url(#{"zd-arrow-accent" if focal else "zd-arrow"})"/>')
            if e.get("label"): edge_label(out, e["label"], x + 48 + text_w(e["label"]) * 0.83 // 2 + 8, y + 24 + 12, c)
            continue
        x1, x2 = (a["cx"], b["cx"]) if a["cx"] < b["cx"] else (b["cx"], a["cx"])
        out.append(f'  <path d="M {a["cx"]},{y} L {b["cx"]},{y}" fill="none" stroke="{color}" stroke-width="1.5"{dashed} marker-end="url(#{"zd-arrow-accent" if focal else "zd-arrow"})"/>')
        if e.get("label"): edge_label(out, e["label"], g4((a["cx"] + b["cx"]) / 2), y - 12, c)
    for m in spec["nodes"]:
        v = coords[m["id"]]
        out.append(f'  <rect x="{v["x"]}" y="{v["y"]}" width="{v["w"]}" height="{v["h"]}" rx="6" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1"/>')
        out.append(f'  <text x="{v["x"] + v["w"]//2}" y="{v["y"] + v["h"]//2 + 4}" text-anchor="middle" font-family="{FONTS["sans"]}" font-size="12" font-weight="600" fill="{c["ink"]}">{esc(m["label"])}</text>')
    return out

def render_grid_svg(spec, coords, c):
    out = []
    lanes = spec.get("lanes", [])
    for i, name in enumerate(lanes):
        y = MARGIN + 32 + i * (NODE_H + G * 10)
        out.append(f'  <text x="{MARGIN}" y="{y - 10}" font-family="{FONTS["mono"]}" font-size="10" fill="{c["muted"]}">{esc(name.upper())}</text>')
        max_x = max((v["x"] + v["w"] for v in coords.values()), default=MARGIN) + GAP_X
        out.append(f'  <line x1="{MARGIN}" y1="{y - 4}" x2="{g4(max_x)}" y2="{y - 4}" stroke="{c["rule"]}" stroke-width="1"/>')
    for m in spec["nodes"]:
        v = coords[m["id"]]
        out.append(f'  <rect x="{v["x"]}" y="{v["y"]}" width="{v["w"]}" height="{v["h"]}" rx="6" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1"/>')
        out.append(f'  <text x="{v["x"] + v["w"]//2}" y="{v["y"] + v["h"]//2 + 4}" text-anchor="middle" font-family="{FONTS["sans"]}" font-size="12" font-weight="600" fill="{c["ink"]}">{esc(m["label"])}</text>')
    return out

RENDERERS = {"hierarchy": render_hierarchy_svg, "sequence": render_sequence_svg, "grid": render_grid_svg}

# ---------- 样式注入 ----------
def load_style(path):
    if not path: return None
    import re
    roles = {}
    try: text = open(path).read()
    except Exception: return None
    for m in re.finditer(r'^\s{2}(paper|ink|muted|soft|rule|accent|accent-tint|link):\s*"?([^"\n]+)"?', text, re.M):
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
    layout = spec.get("layout", "hierarchy")
    if layout not in LAYOUTS: sys.exit(f"未知 layout: {layout}(可选 {list(LAYOUTS)})")
    coords = LAYOUTS[layout](spec)
    style = load_style(a.style)
    c = style or {"ink": INK, "muted": MUTED, "paper": PAPER, "rule": "rgba(11,12,14,0.10)", "accent": ACCENT}
    h_ext = max((v.get("lifeline_to", v["y"] + v["h"]) for v in coords.values()), default=MARGIN)
    out = {"layout": layout,
           "canvas": {"w": g4(max(v["x"] + v["w"] for v in coords.values()) + MARGIN),
                      "h": g4(h_ext + MARGIN)},
           "nodes": coords}
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"coords → {a.out}(节点 {n},边 {e},画布 {out['canvas']['w']}×{out['canvas']['h']})")
    if a.svg:
        body = RENDERERS[layout](spec, coords, c)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {out["canvas"]["w"]} {out["canvas"]["h"]}" '
               f'role="img" aria-labelledby="zd-title zd-desc">\n'
               f'  <title id="zd-title">{esc(spec.get("title", "diagram"))}</title>\n'
               f'  <desc id="zd-desc">{esc(spec.get("desc", "示意图"))}</desc>\n'
               f'  <defs>\n'
               f'    <marker id="zd-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{c["muted"]}"/></marker>\n'
               f'    <marker id="zd-arrow-accent" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{c["accent"]}"/></marker>\n'
               f'  </defs>\n'
               f'  <rect width="{out["canvas"]["w"]}" height="{out["canvas"]["h"]}" fill="{c["paper"]}"/>\n'
               + "\n".join(body) + "\n</svg>\n")
        open(a.svg, "w").write(svg)
        print(f"svg    → {a.svg}")

if __name__ == "__main__":
    main()
