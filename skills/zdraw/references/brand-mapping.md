# zdraw · token → 语义角色映射(权威细节)

图表产出的视觉真相不是 CSS 变量,而是**语义角色**——颜色/字体按角色消费,布局按 `layout-rules.md` 执行。本文是映射的唯一权威定义。

## 颜色映射

| 语义角色 | 用途 | 来源 DESIGN.md token | 退化策略 |
|---|---|---|---|
| `paper` | 画布底 | `colors.background` | — |
| `paper-2` | 容器底(可选) | `colors.background-secondary` / surface-1 | 缺失用 `paper` |
| `ink` | 主文字 / 主描边 | `colors.text-primary` | — |
| `muted` | 次要文字 / 默认箭头 | `colors.text-secondary` / text-muted | — |
| `soft` | 弱化描边 / 细节 | `colors.text-tertiary` / border | 缺失用 `muted` |
| `rule` | 发丝线边框 | `colors.border` / hairline | 缺失用 `ink @ 0.10` |
| `accent` | **焦点色,≤2 元素** | `colors.primary` | — |
| `accent-tint` | 焦点节点填充 | `colors.primary` 加透明度(@ 0.05–0.12) | — |
| `link` | HTTP/API/外部调用 | `colors.info` / 蓝系 | 缺省用 `muted` 加蓝相或默认 `#2e5aa8`,交付时披露 |

透明度记法:`ink @ 0.05` = ink 色 5% 不透明度(画淡填充/淡描边)。

## accent 硬规则(焦点克制)

- **accent 元素总数 ≤2**:可为焦点节点、主箭头或其组合(2 节点,或 1 节点 + 1 箭头)。
- 其余所有节点一律 `ink` / `muted` / `soft` 中性处理。
- 品牌感由整体调性传达(paper/ink/字体),**不是到处刷品牌色**。品牌 UI 里 primary 可大面积用,图表里不行——图表语法的信噪比优先。
- 违反 = 验收不通过,回炉。

## 字体三元组(品牌优先 + 缺失退化)

| 槽位 | 用途 | 来源 | 退化 |
|---|---|---|---|
| 标题 | 页 H1 | `typography.display` / headings | 品牌无 serif/display → 品牌 sans 加权重 |
| 节点名 | 人类可读标签(12px 上下,600) | `typography.body` sans | — |
| 技术子标签 | 端口 / URL / 类型 / 箭头标注 | 品牌 mono / `typography.code` | 品牌 无 mono → Geist Mono(功能性字体,非品牌表达,交付时说明) |

- **mono 只给技术内容**(端口、命令、URL),节点名永远 sans——铁律。
- Google Fonts 引入:`<link href="https://fonts.googleapis.com/css2?family=<品牌字体>:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap">`(仅缺 mono 时补 Geist Mono)。

## `<产出根>/diagram-style.md` 格式定义

映射产物落盘为 YAML frontmatter 文件,地位等同 DESIGN.md——**图表产出的唯一视觉真相**:

```markdown
---
source-design: linear.app        # 来自哪个 DESIGN.md
generated: 2026-08-16
roles:
  paper: "#ffffff"
  paper-2: "#f7f8f8"
  ink: "#0b0c0e"
  muted: "#8a8f98"
  soft: "#b4b9c2"
  rule: "rgba(11,12,14,0.10)"
  accent: "#5e6ad2"
  accent-tint: "rgba(94,106,210,0.08)"
  link: "#2e5aa8"                # 退化值需注明
fonts:
  display: ["Linear Display", "sans-serif"]
  sans: ["Inter", "system-ui", "sans-serif"]
  mono: ["Geist Mono", "monospace"]   # 退化需注明
degradations:                    # 所有退化决策在此披露
  - "link 用默认蓝:DESIGN.md 无 info/blue token"
  - "mono 退化 Geist Mono:品牌无 mono 字体"
---

# diagram-style · linear.app

(可选:映射时的取舍说明)
```

已有 `diagram-style.md` 且本次 source-design 相同 → 直接复用,不重映射。

## 与源文件/渲染的配合

- 语义角色只管**视觉**;布局(连线/间距/预算)完全按 `layout-rules.md` 执行。
- **注入三个出口**:
  1. `.drawio` — mxCell `style` 串消费角色值(`fillColor=#paper;strokeColor=#ink;fontColor=#ink`),箭头默认 `strokeColor=#muted`
  2. `.excalidraw` — 元素 `strokeColor`/`backgroundColor`/`fontFamily` 直填角色值
  3. `.svg`(layout 脚本渲染)— `--style diagram-style.md` 注入为 CSS 变量,`fill="var(--ink)"` 消费——换品牌只改变量,布局不动
- `diagram-style.md` 落盘 `.zdev/design/diagram-style.md`,与 zdesign 的 brands/ 同源共享;同 source-design 复跑直接复用。
