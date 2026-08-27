---
name: zdesign
icon: "🎨"
description: "Use when the user wants concrete UI/visual design produced — landing pages, web app screens, app screens, components, or visual style exploration. Picks a design system, generates HTML/CSS that strictly follows it, runs a live preview, self-verifies, and delivers polished artifacts (never half-baked). Independent of OpenDesign. For design taste/guidance alone, frontend-design may suffice; use zdesign when actual design artifacts are needed. Also covers branded diagrams (architecture, flowchart, sequence, ER, state machine, SVG schematics) rendered in the chosen design system's style — use zdesign when diagrams must match the brand; plain unbranded diagrams route to diagram-design instead."
---

# zdesign

独立的视觉 / 界面设计 skill。**选设计系统 → 产出 HTML/CSS → 过质量门禁交付**;实时预览按需由 zdash 拉起面板(#design 直达)。不依赖 OpenDesign。

## 核心理念

- **设计系统驱动**:所有视觉决策(配色 / 字体 / 圆角 / 间距)来自选定的 `DESIGN.md`,不自由发挥。
- **完善交付,不是半成品**:产出必须过【约束】【细节】【验收】三道关,未全过则回炉。
- **轻量自洽**:产出是纯 HTML/CSS(零运行时依赖);预览由面板(zdash)按需提供。
- **统一输出根**:所有产出默认写入 `.zdev/design/`,skill 不询问输出路径。

## 工作流

### 1. 预览(可选)
用户想边写边看时,用 zdash 拉起面板(#design 直达),保存即热刷新。本 skill 自身不启动任何服务。

产出根统一为 `.zdev/design/`。

### 2. 确认任务
确认:做什么(web 页面 / 应用界面 / 组件 / 风格探索 / app 屏 / **图表**(架构图 / 流程图 / 时序图 / ER / 状态机等))?给谁用?有无参考?目标设备与断点?

### 3. 选风格(动态发现,可插拔源)
**查找顺序**:`.zdev/design/brands/<slug>/DESIGN.md`(本地已归档,直接用)→ getdesign 官方库 → 现场蒸馏(产出回填 brands/)。

风格菜单默认来自 [awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) 的 README —— 68 个品牌,9 大分类(AI / 开发工具 / 后端 / SaaS / 设计工具 / 金融 / 电商 / 媒体 / 汽车)。

- 用 WebFetch 抓 `https://raw.githubusercontent.com/VoltAgent/awesome-claude-design/main/README.md`
- 解析出品牌清单(`slug` + 一句话描述 + 分类)。slug 就是 getdesign.md 的品牌路径,如 `linear.app`、`stripe`、`notion`、`vercel`、`apple`。
- **按分类**展示给用户选;**视觉探索**场景并排 2-3 个对比。
- 用户也可直接指定("用 Linear 风格")。

### 4. 取 DESIGN.md(官方 CLI,拿完整 token)
选定品牌后,拉取并归档到品牌源目录(`brands/` 已有同 slug 的 DESIGN.md 则跳过拉取):

```bash
mkdir -p .zdev/design/brands/<brand-slug> && cd .zdev/design/brands/<brand-slug>
npx -y getdesign@latest add <brand-slug>
cd -  # 回项目根继续后续步骤
```
产出的 `DESIGN.md` 是 YAML frontmatter,含完整 token:`colors` / `typography`(type scale)/ `rounded` / `spacing` / `components` / `layout` / `shadows` / `motion` / do's & don'ts。读它,这是本次产出的唯一视觉真相来源。

> 若无网络 / CLI 不可用,可改用 WebFetch 抓 `https://getdesign.md/<brand-slug>/design-md` 兜底。

### 5. token → CSS 变量(或图表语义角色)
UI 产出:把 DESIGN.md 的 YAML token 映射成 `:root` CSS 变量(如 `--color-primary`、`--surface-1`、`--font-display`、`--radius-md`、`--space-lg`)。**产出全程引用变量,绝不硬编码 hex / px 常数**。

图表产出:不走 CSS 变量直连,改走 **token → 图表语义角色** 映射,落盘 `.zdev/design/diagram-style.md`——见下方【图表(diagram)场景】。

### 6. 按约束产出 + 打磨细节
遵守下方【约束】硬规则与【细节】清单,产出 HTML/CSS 写入 `.zdev/design/`。预览开着就边写边看(保存即热刷新);没开也不阻塞写作。

### 7. 验收(闭环)
按【验收】清单逐项自检 + 预览确认。**未全过 → 回第 6 步修,过了才交付。**

### 8. 交付
返回:产出文件路径 + 所选风格名 + 验收清单结果;已开预览的附面板 URL(#design)。

## 风格源(多源,可插拔)
zdesign **不绑定单一库**。选风格时按优先级尝试多个源,任一命中即可:

**A. DESIGN.md 库(token 现成,直接消费)**
- `getdesign` 官方库(首选):`npx -y getdesign@latest add <brand>`(73+ 品牌,如 linear.app / stripe / notion / vercel / apple…)。菜单可从 [awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) 的 README 抓取(68 条分类索引)。
- 本地 `DESIGN.md`:用户项目里已有的直接 Read;zdesign 自产的统一归档 `.zdev/design/brands/<slug>/DESIGN.md`,是查找的第一优先级。
- 任意 YAML / DESIGN.md 文件:符合 token 格式即可。

**B. 参考驱动(库内没有时,现场蒸馏成 token)**
当 A 类都查不到该风格(如 **shadcn**、或官方设计系统 Material 3 / Apple HIG / IBM Carbon / Polaris / Fluent…),从参考来源蒸馏出一份 DESIGN.md(YAML frontmatter):
- 官方规范页 / 品牌官网 URL → WebFetch 抓 → 提炼 token
- 截图 → 视觉分析提炼 token
- 已知范式(如 shadcn 的 zinc 色阶 + ring-offset)→ 直接落 token
蒸馏产物落盘 `.zdev/design/brands/<slug>/DESIGN.md` 归档——从此它就是 A 类本地源,同品牌复跑零成本。

## 图表(diagram)场景

**判据**:图表 + 品牌诉求(要匹配所选设计系统)→ zdesign 承接;纯图表无品牌诉求 → 让 diagram-design 独立处理,不抢。

### 视觉:token → 语义角色
图表的视觉真相不是 CSS 变量,是**语义角色**(`paper`/`ink`/`muted`/`accent`/`link` + 字体三元组)。按 `references/diagram-style-mapping.md` 把选定 DESIGN.md 映射落盘为 `.zdev/design/diagram-style.md`(地位等同 DESIGN.md,同品牌复跑直接复用)。要点:

- **accent 焦点克制**:品牌 primary 只给 ≤2 个元素(焦点节点/主箭头合计),其余节点一律中性(ink/muted/soft)。品牌感靠整体调性传达,不在图表里刷品牌色。
- **字体品牌优先 + 缺失退化**:标题←品牌 display(无 serif 用 sans);节点名←品牌 sans;技术子标签←品牌 mono,无 mono 退化 Geist Mono 并披露。
- 角色注入 CSS 变量后 inline SVG 直接 `fill="var(--ink)"` 消费。

### 布局:语法源四级降级(拉最新优先)
类型数/版本**不硬编码**,以实际拉到的为准(上游持续演进)。依次尝试,任一级成功即用:

1. **拉上游 main 最新**:WebFetch `https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/skills/diagram-design/SKILL.md` —— 取类型选择表与布局规则(§4-§9),按所选图型再拉同目录 `references/type-<name>.md`。
2. **WebFetch 直连超时** → 改用 web reader 类 MCP 工具抓同一 URL(raw.githubusercontent 在部分网络下本机不通)。
3. **网络全失败** → 本地插件缓存 `~/.zcode/cli/plugins/cache/diagram-design/**/skills/diagram-design/`(版本可能滞后,交付时说明)。
4. **都没有** → 自带 `references/diagram-basics.md` 精简规则(8 常用类型 + 硬规则),并提示建议安装 diagram-design。

无论哪级:**不修改 diagram-design 任何文件**;换肤靠产出时以 diagram-style.md 覆盖语义角色。

### 场景 × 尺寸
文档/README 配图 → `doc-inline`/`doc-wide`(可按需导出 PNG/SVG,手动不问不导);设计稿内嵌 → `fit`(随 dashboard 预览);独立单图 → `slide-16x9`/`social-og`;风格探索 → 并排 2-3 张。尺寸同时约束字号阶梯(slide 的节点名是 16px 不是 12px)。

### 交付
图表产出交付时另报:diagram-style.md 路径 + 所选品牌 + **所用语法源的 diagram-design 版本与级别**(最新 main / 本地缓存 x.y.z / 兜底)。验收走 `references/quality-checklist.md` 图表专项。

## 【约束】硬规则(产出时强制)
1. **token 强制**:颜色 / 字号 / 圆角 / 间距 100% 来自选定 DESIGN.md → CSS 变量。禁止硬编码。
2. **防 AI 感红线**:禁默认 indigo / violet 充当主色、禁 emoji 当图标、禁等权重三栏网格、禁"渐变涂色标题"、字号严格按 type scale 不漂移。
3. **响应式**:至少 mobile / desktop 两断点,触控目标 ≥ 44px,内容不横向溢出。
4. **a11y 基础**:语义化标签、文字对比度达 AA、`:focus` 可见、图片有 alt。

## 【细节】打磨清单
- **状态完整**:默认 / hover / active / focus / disabled;空 / 加载 / 错误 / 成功。
- **真实文案**:不留 Lorem ipsum、"Button"、"Title",用贴合场景的占位文案。
- **视觉层级**:主次分明,留白节奏遵循 spacing 阶梯。
- **对齐与栅格**:全局一致。
- **微交互**:过渡用 token 的 motion,克制不浮夸。

## 【验收】交付前自检
- [ ] 所有颜色 / 字号 / 圆角 / 间距都引用 CSS 变量(无硬编码)
- [ ] 视觉调性与所选 DESIGN.md 一致
- [ ] 覆盖需求的所有功能与状态
- [ ] mobile / desktop 响应式都不破
- [ ] a11y 基础过关(对比度 / 语义 / focus)
- [ ] 面板里亲眼看过成品(web 必做:开过预览直接看,没开此时用 zdash 拉起看)——确认调性/响应式符合预期

**未全过 → 回炉,绝不交付半成品。**

## app 场景
DESIGN.md 的 token 同样适用,但落点不同:web 落 HTML/CSS 且可进面板实时预览;app 产出 SwiftUI / Compose / Flutter 代码,把 token 映射到各平台颜色 / 字体 API,指引用户在模拟器或真机验证。

## 输出格式
交付时给出:产出文件路径(`.zdev/design/` 下)+ 所选风格名 + 验收清单结果(逐项 ✓);开了预览附面板 URL。

## 资产
- `references/diagram-style-mapping.md` — 图表 token → 语义角色映射权威细节(含 diagram-style.md 格式定义、上游 URL 常量)
- `references/diagram-basics.md` — 图表兜底布局规则(语法源四级降级全失败时用)
- `references/quality-checklist.md` — 约束 / 细节 / 验收的详细速查(含图表专项)
