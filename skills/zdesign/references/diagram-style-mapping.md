# zdesign 图表 · token → 语义角色映射(权威细节)

图表产出的视觉真相不是 CSS 变量,而是**语义角色**——颜色/字体按角色消费,布局语法按 diagram-design(拉最新)执行。本文是映射的唯一权威定义。

## 上游常量

- diagram-design 仓库:`https://github.com/cathrynlavery/diagram-design`
- 拉最新入口(SKILL.md):`https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/skills/diagram-design/SKILL.md`
- 图型细则同目录拼接:`.../main/skills/diagram-design/references/type-<name>.md`
- **版本号/类型数不硬编码**——以拉到的 frontmatter `metadata.version` 与类型表为准(上游持续演进)。

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
| `link` | HTTP/API/外部调用 | `colors.info` / 蓝系 | 缺失保留 diagram-design 默认 `#2e5aa8`,交付时披露 |

透明度记法:`ink @ 0.05` = ink 色 5% 不透明度(画淡填充/淡描边),来自 diagram-design 的节点处理惯例。

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

- **mono 只给技术内容**(端口、命令、URL),节点名永远 sans——这是 diagram-design 的铁律,照用。
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

## 与布局语法源的配合

- 语义角色只管**视觉**;布局(连线/间距/预算)完全按拉到的 diagram-design 最新规则执行,或兜底 `diagram-basics.md`。
- 产出时把 `diagram-style.md` 的角色注入为 CSS 变量(见 `assets/templates/diagram-starter.html`),inline SVG 内直接 `fill="var(--ink)"` 消费——换品牌只改变量,布局不动。
- 不修改 diagram-design 的任何文件(上游 / 本地插件缓存都不碰)。
