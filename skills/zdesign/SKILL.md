---
name: zdesign
icon: "🎨"
description: "Use when the user wants concrete UI/visual design produced — landing pages, web app screens, app screens, components, or visual style exploration. Picks a design system, generates HTML/CSS that strictly follows it, runs a live preview, self-verifies, and delivers polished artifacts (never half-baked). Independent of OpenDesign. For design taste/guidance alone, frontend-design may suffice; use zdesign when actual design artifacts are needed. Also covers branded diagrams (architecture, flowchart, sequence, ER, state machine, SVG schematics) rendered in the chosen design system's style — use zdesign when diagrams must match the brand; plain unbranded diagrams route to diagram-design instead."
---

# zdesign

独立的视觉 / 界面设计 skill。**先拉起 zdashboard 实时预览 → 再选设计系统 → 产出 HTML/CSS → 过质量门禁交付**。不依赖 OpenDesign。

## 核心理念

- **设计系统驱动**:所有视觉决策(配色 / 字体 / 圆角 / 间距)来自选定的 `DESIGN.md`,不自由发挥。
- **完善交付,不是半成品**:产出必须过【约束】【细节】【验收】三道关,未全过则回炉。
- **轻量自洽**:产出是纯 HTML/CSS(零运行时依赖);实时预览由独立包 `zdashboard` 提供。

## 工作流

### 1. 检查/拉起实时预览
先检查 zdashboard 是否已在运行(访问 `http://localhost:4190/__config`):
- 能访问 → 已有实例在运行,询问用户:「检测到 zdashboard 已在运行,直接使用现有实例还是重新拉最新版?」
  - 用户选「直接使用」→ 沿用当前实例
  - 用户选「重新拉最新版」→ 继续下面的启动流程
- 不能访问 → 直接拉起最新版

确认产出根后执行:
```bash
npx zdashboard@latest --mode design --dir <产出根> --open
```
预览由独立 npm 包 `zdashboard` 提供(无需自带,npx 自动拉起)。浏览器自动打开,每次保存自动刷新。把 URL 给用户。端口默认 4173,被占用自动顺延(`--port` 可指定),多项目并行不冲突。

产出根确认规则:
- **独立设计** -> 产出根 = `cwd`(整个文件夹就是为设计而生)
- **已有项目**(默认)-> 产出根 = `cwd/.zdesign/`(隔离,不污染项目)
- **自定义** -> 用户填的任意路径(cwd 不是项目根时用这个填项目根)

产出根确定后本次会话沿用,不写持久配置;产出根已存在 / 非空时只写入新文件,不清空。

### 2. 确认任务
再确认:做什么(web 页面 / 应用界面 / 组件 / 风格探索 / app 屏 / **图表**(架构图 / 流程图 / 时序图 / ER / 状态机等))?给谁用?有无参考?目标设备与断点?

### 3. 选风格(动态发现,可插拔源)
风格菜单默认来自 [awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) 的 README —— 68 个品牌,9 大分类(AI / 开发工具 / 后端 / SaaS / 设计工具 / 金融 / 电商 / 媒体 / 汽车)。

- 用 WebFetch 抓 `https://raw.githubusercontent.com/VoltAgent/awesome-claude-design/main/README.md`
- 解析出品牌清单(`slug` + 一句话描述 + 分类)。slug 就是 getdesign.md 的品牌路径,如 `linear.app`、`stripe`、`notion`、`vercel`、`apple`。
- **按分类**展示给用户选;**视觉探索**场景并排 2-3 个对比。
- 用户也可直接指定("用 Linear 风格")。

### 4. 取 DESIGN.md(官方 CLI,拿完整 token)
选定品牌后,在一个临时目录运行:
```bash
npx -y getdesign@latest add <brand-slug>
```
产出的 `DESIGN.md` 是 YAML frontmatter,含完整 token:`colors` / `typography`(type scale)/ `rounded` / `spacing` / `components` / `layout` / `shadows` / `motion` / do's & don'ts。读它,这是本次产出的唯一视觉真相来源。

> 若无网络 / CLI 不可用,可改用 WebFetch 抓 `https://getdesign.md/<brand-slug>/design-md` 兜底。

### 5. token → CSS 变量(或图表语义角色)
UI 产出:把 DESIGN.md 的 YAML token 映射成 `:root` CSS 变量(如 `--color-primary`、`--surface-1`、`--font-display`、`--radius-md`、`--space-lg`)。**产出全程引用变量,绝不硬编码 hex / px 常数**。参考 `assets/templates/starter.html` 的映射范式。

图表产出:不走 CSS 变量直连,改走 **token → 图表语义角色** 映射,落盘 `<产出根>/diagram-style.md`——见下方【图表(diagram)场景】。

### 6. 按约束产出 + 打磨细节
遵守下方【约束】硬规则与【细节】清单,产出 HTML/CSS 写入产出根(第 1 步确认的)。预览已在第 1 步启动,每次保存自动刷新,边写边看。

### 7. 验收(闭环)
按【验收】清单逐项自检 + 预览确认。**未全过 → 回第 6 步修,过了才交付。**

### 8. 交付
返回:产出文件路径 + 预览 URL + 所选风格名 + 验收清单结果。

## 风格源(多源,可插拔)
zdesign **不绑定单一库**。选风格时按优先级尝试多个源,任一命中即可:

**A. DESIGN.md 库(token 现成,直接消费)**
- `getdesign` 官方库(首选):`npx -y getdesign@latest add <brand>`(73+ 品牌,如 linear.app / stripe / notion / vercel / apple…)。菜单可从 [awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) 的 README 抓取(68 条分类索引)。
- 本地 `DESIGN.md`:用户项目里已有的,直接 Read。
- 任意 YAML / DESIGN.md 文件:符合 token 格式即可。

**B. 参考驱动(库内没有时,现场蒸馏成 token)**
当 A 类都查不到该风格(如 **shadcn**、或官方设计系统 Material 3 / Apple HIG / IBM Carbon / Polaris / Fluent…),从参考来源蒸馏出一份 DESIGN.md(YAML frontmatter):
- 官方规范页 / 品牌官网 URL → WebFetch 抓 → 提炼 token
- 截图 → 视觉分析提炼 token
- 已知范式(如 shadcn 的 zinc 色阶 + ring-offset)→ 直接落 token
蒸馏出的 DESIGN.md 后续当 A 类本地源复用。
