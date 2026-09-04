---
name: zdraw
icon: "📐"
description: "Use when the user wants any diagram produced, edited, or converted — architecture, flowchart, sequence, ER, state machine, swimlane, tree, layer stack, whiteboard sketches. Outputs editable source files (.excalidraw / .drawio) plus rendered SVG, with optional brand-toned styling from zdesign's DESIGN.md sources. Triggers on '画个图', '架构图', '流程图', '时序图', 'ER图', '状态图', '草图', '示意图', '白板', 'draw a diagram', 'excalidraw', 'drawio'. For page/UI design use zdesign."
---

# zdraw

图表 skill:**定类型 → 结构先行 → 布局计算 → 双格式源文件 → 渲染交付**。

一切"图"归这里——架构、流程、时序、ER、状态机、泳道、树、层栈、白板草图。交付**永远双轨**:可编辑源文件(.excalidraw / .drawio)+ 渲染导出(.svg)。页面/UI 归 zdesign。

## 何时触发
- 用户说"画个架构图 / 流程图 / 时序图 / ER 图 / 草图 / 白板"
- zarchitect 出方案时为 change 配图(落 `openspec/changes/<slug>/diagrams/`)
- zdocs 写文档需要配图(落 `docs/diagrams/`)
- 需要 .excalidraw / .drawio 文件的生成、编辑、互转

## 格式路由(三级优先)

| 优先 | 格式 | 场景 |
|---|---|---|
| **1. Mermaid** | 图将**住在 markdown 里** | README / design.md / docs / change 文档内嵌——零坐标、diff 友好、GitHub 原生渲染,直接写 \`\`\`mermaid 代码块,连布局脚本都不用跑 |
| **2. .excalidraw** | 独立图文件 / 白板 / 草图 | 需要精细布局、品牌调性、或作为独立源文件被人继续编辑(独立文件的默认格式) |
| **3. .drawio** | 点名 / 图标库 / Confluence | 用户点名、交付目标硬要求、大型图标库工程图(云拓扑/标准 UML) |

**Mermaid 降级条件**(命中任一 → 升 .excalidraw):
- 布局自动生成不可控,节点多(>12)或关系复杂时图会乱 → excalidraw 走脚本布局
- 品牌化诉求(语义角色注入)→ excalidraw/drawio
- mermaid 不支持的类型(自由白板、复杂泳道变体)→ excalidraw/drawio

**双交付铁律**:独立源文件场景 = 源(.excalidraw/.drawio)+ 渲染 .svg,缺一不算交付;**Mermaid 场景源即交付**(md 内代码块本身),.svg 用户要了才另出。

## 工作流

### 0. 先问图住哪(路由判定)
图将内嵌 markdown(README/design.md/docs/change 文档)→ **Mermaid 代码块直达交付**(跳过 3-4 步,无需布局脚本);命中降级条件或独立图文件 → 继续下方完整管线。

### 1. 定类型与场景
类型八选一 + 白板:architecture / flowchart / sequence / erd / state / swimlane / tree / layer-stack。场景定尺寸预设(doc-inline 800×600 / doc-wide 1120×n / slide-16x9 1600×900 / social-og 1200×630 / fit)。**尺寸同时约束字号阶梯**——slide 的节点名 16px,不是 12px。

### 2. 结构先行(先内容后视觉)
把图写成**节点/边清单**(文本):节点 = id + 名称 + 类型(普通/焦点/存储/外部);边 = from/to + 标签 + 样式(实/虚)。节点 > 6 个时清单先给用户扫一眼确认,再进布局。
**复杂度预算:≤9 节点、≤12 边。超了拆 overview + detail 两张,不硬塞。**

### 3. 布局计算(脚本辅助,禁止裸估坐标)
把清单写成 spec JSON,跑仓库根的布局脚本:

```bash
python3 scripts/zdraw_layout.py spec.json -o coords.json --svg out.svg
```

- 支持 hierarchy(架构/流程/树,层内居中)/ sequence(时序,生命线+消息序+自消息)/ grid(泳道/层栈,含车道标签)三种算法
- 节点宽度随标签自适应(中文 12px/字符、英文 7px,80–240 钳制);自动落实 4px 网格、间距阶梯、画布尺寸
- SVG 渲染内置:正交圆角连线、标签遮罩留隙、箭头三件套、时序生命线、泳道分隔(规则见 `references/layout-rules.md`)
- 脚本算不了的(自由白板)才手摆,同样守 4px 网格

### 4. 生成源文件(坐标来自 coords,禁止手估)
按 `references/formats.md` 的骨架写,**默认只出 .excalidraw**:
- `.excalidraw`(主):elements 数组(rectangle/arrow/text),坐标直填
- `.drawio`(次,场景命中才出):mxGraphModel XML,mxCell 节点/边,style 串消费品牌色

### 5. 品牌化(可选)
用户要求图匹配品牌时:查 `design/brands/<slug>/DESIGN.md`(与 zdesign 同源共享;无则先蒸馏归档),按 `references/brand-mapping.md` 映射为语义角色落盘 `design/diagram-style.md`,再注入源文件(excalidraw strokeColors / drawio style 串)。**accent 焦点克制 ≤2 元素**;无品牌诉求则中性配色,不抢。

### 6. 验收
按 `references/quality-checklist.md` 逐项自检:预算内 / 正交圆角 / 标签不压线 / 4px 网格 / 双交付齐 / 浏览器亲眼确认 .svg。未全过回炉。

### 7. 交付
返回:文件清单表(源文件 + .svg,各自用途)+ 类型/场景/尺寸 + 品牌来源(有则报 diagram-style.md 路径)。落盘位置按调用方契约:change 挂图 `openspec/changes/<slug>/diagrams/`、文档配图 `docs/diagrams/`、独立图 `docs/diagrams/`。

## 边界
- 只产图与图源,不写文档正文(zdocs)、不做页面(zdesign)、不改业务代码
- 不主动导出 PNG——用户要了再导(无头浏览器/平台截图,不强制零依赖)
- 白板自由摆件同样守 4px 网格与复杂度预算

## 资产
- `references/layout-rules.md` — 布局语法权威:8 类型速查、连线/节点盒/网格/预算硬规则
- `references/brand-mapping.md` — DESIGN.md token → 语义角色映射权威(含 diagram-style.md 格式定义)
- `references/formats.md` — .excalidraw / .drawio 生成骨架与互转/export 命令
- `references/quality-checklist.md` — 图表验收速查
- `scripts/zdraw_layout.py`(仓库根)— 布局计算 + SVG 渲染
