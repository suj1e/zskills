---
name: zdesign
description: "Use when the user wants concrete UI/visual design produced — landing pages, web app screens, app screens, components, or visual style exploration. Picks a design system, generates HTML/CSS that strictly follows it, runs a live preview, self-verifies, and delivers polished artifacts (never half-baked). Independent of OpenDesign. For design taste/guidance alone, frontend-design may suffice; use zdesign when actual design artifacts are needed."
---

# zdesign

独立的视觉 / 界面设计 skill。**选一套设计系统 → 产出严格遵循它的 HTML/CSS → 调用 zdesign-dashboard 包实时预览 → 过质量门禁才交付**。不依赖 OpenDesign。

## 核心理念

- **设计系统驱动**:所有视觉决策(配色 / 字体 / 圆角 / 间距)来自选定的 `DESIGN.md`,不自由发挥。
- **完善交付,不是半成品**:产出必须过【约束】【细节】【验收】三道关,未全过则回炉。
- **轻量自洽**:产出是纯 HTML/CSS(零运行时依赖);实时预览由独立包 `zdesign-dashboard` 提供。

## 工作流

### 1. 理解任务 + 确认产出根
先确认产出根(强制询问,默认推荐 `.zdesign/`):
- **独立设计** -> 产出根 = `cwd`(整个文件夹就是为设计而生)
- **已有项目**(默认)-> 产出根 = `cwd/.zdesign/`(隔离,不污染项目)
- **自定义** -> 用户填的任意路径(cwd 不是项目根时用这个填项目根)

产出根确定后本次会话沿用,不写持久配置;产出根已存在 / 非空时只写入新文件,不清空。

再确认:做什么(web 页面 / 应用界面 / 组件 / 风格探索 / app 屏)?给谁用?有无参考?目标设备与断点?

### 2. 选风格(动态发现,可插拔源)
风格菜单默认来自 [awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) 的 README —— 68 个品牌,9 大分类(AI / 开发工具 / 后端 / SaaS / 设计工具 / 金融 / 电商 / 媒体 / 汽车)。

- 用 WebFetch 抓 `https://raw.githubusercontent.com/VoltAgent/awesome-claude-design/main/README.md`
- 解析出品牌清单(`slug` + 一句话描述 + 分类)。slug 就是 getdesign.md 的品牌路径,如 `linear.app`、`stripe`、`notion`、`vercel`、`apple`。
- **按分类**展示给用户选;**视觉探索**场景并排 2-3 个对比。
- 用户也可直接指定("用 Linear 风格")。

### 3. 取 DESIGN.md(官方 CLI,拿完整 token)
选定品牌后,在一个临时目录运行:
```bash
npx -y getdesign@latest add <brand-slug>
```
产出的 `DESIGN.md` 是 YAML frontmatter,含完整 token:`colors` / `typography`(type scale)/ `rounded` / `spacing` / `components` / `layout` / `shadows` / `motion` / do's & don'ts。读它,这是本次产出的唯一视觉真相来源。

> 若无网络 / CLI 不可用,可改用 WebFetch 抓 `https://getdesign.md/<brand-slug>/design-md` 兜底。

### 4. token → CSS 变量
把 DESIGN.md 的 YAML token 映射成 `:root` CSS 变量(如 `--color-primary`、`--surface-1`、`--font-display`、`--radius-md`、`--space-lg`)。**产出全程引用变量,绝不硬编码 hex / px 常数**。参考 `assets/templates/starter.html` 的映射范式。

### 5. 按约束产出 + 打磨细节
遵守下方【约束】硬规则与【细节】清单,产出 HTML/CSS 写入产出根(第 1 步确认的)。

### 6. 起实时预览(调用 zdesign-dashboard 包)
```bash
npx zdesign-dashboard --dir <产出根> --open
```
预览由独立 npm 包 `zdesign-dashboard` 提供(无需自带,npx 自动拉起)。浏览器自动打开,每次保存自动刷新。把 URL 给用户。端口默认 4173,被占用自动顺延(`--port` 可指定),多项目并行不冲突。

### 7. 验收(闭环)
按【验收】清单逐项自检 + 预览确认。**未全过 → 回第 5 步修,过了才交付。**

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

**选源顺序**:先 `npx getdesign add <brand>` 探库 → 再本地 → 都没有则参考驱动蒸馏。任一源拿到的 DESIGN.md 都是本次产出的唯一视觉真相。

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
- [ ] 预览打开、亲眼确认过

**未全过 → 回炉,绝不交付半成品。**

## app 场景
DESIGN.md 的 token 同样适用。但实时预览 server 服务 web;app 产出 SwiftUI / Compose / Flutter 代码,把 token 映射到各平台颜色 / 字体 API,指引用户在模拟器或真机查看。移动端规则薄弱时可参考 `references/`。

## 输出格式
交付时给出:产出根 + 文件路径 + 预览 URL(web)+ 所选风格名 + 验收清单结果(逐项 ✓)。

## 资产
- 实时预览由独立 npm 包 `zdesign-dashboard` 提供,见第 6 步(`npx zdesign-dashboard --dir <产出根> --open`)
- `assets/templates/starter.html` — token → CSS 变量的骨架范式
- `assets/components/button.html` — 组件如何消费 token 的示范
- `references/quality-checklist.md` — 约束 / 细节 / 验收的详细速查
