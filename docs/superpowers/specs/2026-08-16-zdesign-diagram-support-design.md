# zdesign 图表(diagram)场景支持 — 设计文档

- 日期:2026-08-16
- 状态:已确认(方案与三个关键决策均经用户拍板)
- 范围:zskills 仓库 `skills/zdesign/`

## 背景与动机

zdesign 目前只覆盖 UI 产出(web 页面 / 应用界面 / 组件 / 风格探索 / app 屏)。用户需要它同时支持**品牌 token 驱动的图表设计**——架构图、流程图、时序图、ER 图、SVG 等,覆盖四个场景:

1. 文档 / README 配图(需可导出 PNG/SVG)
2. 品牌设计稿内嵌图表(与页面一起预览)
3. 独立单图交付(slide、社交图卡,固定尺寸)
4. 图表风格探索(并排对比样张)

环境里已装第三方 skill **diagram-design 2.4.0**:27 种图表类型、硬布局规则(正交圆角连线、复杂度预算、4px 网格、自检脚本),但绑定其自带的 editorial 设计系统(Instrument Serif + Geist,coral accent),换肤机制为语义角色(paper/ink/muted/accent/link)。

**互补关系**:diagram-design 有布局语法但只有一套皮肤;zdesign 有品牌 token 管道(getdesign,73+ 品牌)但没有图表布局知识。

## 已确认的决策

| # | 决策 | 选择 |
|---|------|------|
| D1 | 与 diagram-design 的关系 | **桥接复用**:已装则 Read 其布局语法,未装则 zdesign 自带精简规则兜底 |
| D2 | 品牌主色在图表中的用法 | **焦点克制用色**:品牌 primary → 图表 accent,仅 1-2 个焦点节点/主箭头可用;其余节点一律 ink/muted 中性色。品牌感由整体调性(paper/ink/字体)传达 |
| D3 | 图表字体策略 | **品牌优先 + 缺失退化**:标题←品牌 display(无 serif 用 sans);节点名←品牌 sans;技术子标签←品牌 mono,品牌无 mono 则保留 Geist Mono(功能性字体,交付时说明) |
| D4 | 总体方案 | **方案 1:场景分支 + 语义角色桥**(否决了"完整内联"与"超薄路由") |

## 设计

### 1. 工作流变化(最小侵入,8 步框架不动)

| 步骤 | 变化 |
|---|---|
| 1 确认任务 | 任务类型清单新增「图表(架构图/流程图/时序图/ER/状态机…)」;产出根逻辑照旧(强制询问,默认 `.zdesign/`) |
| 2-3 选风格/取 token | 完全复用现有流程(awesome-claude-design 菜单 / getdesign / 本地 DESIGN.md / 参考蒸馏) |
| 4 token 转换 | 图表场景走新分支:token → **图表语义角色**(而非 CSS 变量),映射产物落盘 `<产出根>/diagram-style.md` |
| 5 产出 | 自包含 HTML(inline SVG,零运行时依赖),布局语法来源见第 3 节 |
| 6 预览 | 照旧 `npx zdesign-dashboard@latest --dir <产出根> --open` |
| 7-8 验收/交付 | 验收清单增加图表专项;交付物含 diagram-style.md 路径与所选品牌名 |

### 2. token → 图表语义角色映射

`diagram-style.md`(YAML)是图表产出的唯一视觉真相,地位等同 DESIGN.md:

| 图表语义角色 | 来源 token | 退化策略 |
|---|---|---|
| `paper`(画布底) | `colors.background` | — |
| `ink`(主文字/描边) | `colors.text-primary` | — |
| `muted`(次要文字/默认箭头) | `colors.text-secondary` | — |
| `accent`(焦点色,≤2 元素) | `colors.primary` | — |
| `link`(HTTP/外部调用) | `colors.info` / 蓝系 | 缺失时保留 diagram-design 默认 link 蓝 `#2e5aa8` |

字体三元组(D3):

- 标题 ← `typography.display` / headings;品牌无 serif 则用品牌 sans
- 节点名 ← `typography.body` sans
- 技术子标签(端口/URL/类型)← 品牌 mono / code;品牌无 mono → Geist Mono 并在交付说明

accent 约束(D2)硬规则:普通节点一律 ink/muted;**accent 元素总数 ≤2**(可为焦点节点、主箭头或其组合,如"2 个焦点节点"或"1 个焦点节点 + 1 条主箭头");违反即验收不通过。

### 3. 与 diagram-design 的协作

- **探测**:扫已装 skill 目录寻找 `diagram-design`(路径模式 `~/.zcode/cli/plugins/cache/**/diagram-design/**/SKILL.md` 或会话内 skill 列表)。
- **已装(主路径)**:Read diagram-design 的 SKILL.md §4-§9(反模式/设计系统/SVG 原语/布局间距/taste gate)+ 按图型 Read 对应 `references/type-<name>.md`,按其布局语法产出。**不修改其 `references/style-guide.md`**(不污染第三方插件缓存)——品牌换肤通过 zdesign 在产出时以 `diagram-style.md` 覆盖语义角色实现。
- **图型选择**:复用 diagram-design 的 27 类型选择表(架构→architecture、流程→flowchart、时序→sequence…)。
- **尺寸预设按场景映射**:文档配图 → `doc-inline` / `doc-wide`;设计稿内嵌 → `fit`;独立单图 → `slide-16x9` / `social-og`;风格探索 → 并排 2-3 张。
- **导出 PNG/SVG**:diagram-design 在场时按其 `references/export.md` 流程执行。
- **未装(兜底)**:使用 zdesign 自带 `references/diagram-basics.md`——覆盖常用 8 类型(架构/流程图/时序图/ER/状态机/泳道/树/层栈)的精简规则:正交圆角连线(r=8)、箭头标签遮罩 + 6-10px 间隙、同边多连线附着点扇形展开(≥12px)、复杂度预算(≤9 节点、≤12 箭头,超出拆 overview + detail)、4px 网格、SVG a11y(title/desc)。产出时提示"建议安装 diagram-design 获得完整图表语法与自检脚本"。

### 4. 调度边界(description 措辞)

zdesign 的 description 追加图表触发语义,要点:

- 触发:branded diagram / architecture / flowchart / sequence / ER **in the chosen design system's style**(品牌 token 驱动的图表)
- 让路:图表但无品牌/设计系统诉求 → diagram-design 独立承接(zdesign 不抢)

### 5. 文件变更清单

```
skills/zdesign/
├── SKILL.md                                  # 改:description 追加图表触发;第 1/4/5 步图表分支;新增「图表场景」章节(映射表 + 协作约定 + 验收)
├── references/diagram-basics.md              # 新:兜底图表规则(8 类型精简布局语法)
├── references/diagram-style-mapping.md       # 新:token→语义角色映射权威细节(映射表、退化策略、accent 约束、字体三元组、diagram-style.md 格式定义)
├── assets/templates/diagram-starter.html     # 新:图表骨架范式(语义角色 CSS 变量 + 节点/连线 SVG 原语示例)
└── references/quality-checklist.md           # 改:追加图表验收项
```

### 6. 验收增量(图表专项)

- [ ] 所有图表颜色/字体来自 `diagram-style.md` 语义角色,无硬编码
- [ ] accent 元素总数 ≤2(节点/主箭头合计),普通节点为 ink/muted
- [ ] 连线正交圆角(r=8),无对角斜线
- [ ] 箭头标签有遮罩 + 6-10px 间隙,不压线、不与节点重叠
- [ ] 同边多连线附着点 ≥12px 扇形展开,无重叠/共享连线
- [ ] 复杂度预算内(≤9 节点、≤12 箭头),超出拆图
- [ ] 坐标/字号/间距 4px 网格
- [ ] SVG 有 `role="img"` + prefixed `title`/`desc`
- [ ] 场景对位:文档配图可导出 PNG/SVG;内嵌图随 dashboard 预览;单图符合所选尺寸预设
- [ ] 预览打开、亲眼确认过

### 7. 错误处理

| 情况 | 处理 |
|---|---|
| diagram-design 探测失败 | 走兜底 `diagram-basics.md`,交付时提示建议安装 |
| 品牌 token 无 mono 字体 | 技术子标签退化 Geist Mono,交付说明中披露 |
| 品牌 token 无 info/蓝系 | link 角色保留 diagram-design 默认 `#2e5aa8`,交付说明中披露 |
| getdesign 无网络 / CLI 不可用 | 现有 WebFetch 兜底照旧(`https://getdesign.md/<slug>/design-md`) |
| 图表超复杂度预算 | 拆 overview + detail 两张,不硬塞 |

## 非目标

- 不在 zdesign 内完整复刻 27 种图表类型的深度规则(以桥接 diagram-design 为主路径)
- 不修改 diagram-design 插件的任何文件
- 不做实时协作编辑、多用户等图表编辑器功能
- 不支持 draw.io / Mermaid 源导入重绘(那是 diagram-design 的能力,品牌图表场景暂不涉及;未来有需求再议)

## 测试 / 验证策略

- 用 2 个品牌(如 linear.app、stripe)各产 1 张架构图,人工核验:语义角色映射正确、accent 克制、布局规则达标
- 卸载 diagram-design 场景(或模拟探测失败)验证兜底路径可用
- 验证四场景各一条:README 配图导出 PNG、设计稿内嵌预览、16:9 单图、双风格并排
- 端到端走一遍 dashboard 预览 + 保存自动刷新
