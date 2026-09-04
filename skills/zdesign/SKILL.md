---
name: zdesign
icon: "🎨"
description: "Use when the user wants concrete UI/visual design produced for a product prototype — landing pages, web app screens, app screens, components, or visual style exploration. Routes to the right taste-skill for direction, generates HTML/CSS that follows it, self-verifies against quality gates, and delivers polished artifacts. For design taste/guidance alone without producing artifacts, frontend-design may suffice; use zdesign when actual design artifacts are needed. Diagrams of any kind (architecture, flowchart, ER, whiteboard sketches — branded or not) route to zdraw; standalone graphic assets (logo, favicon/app icons, OG share images, banners, posters, illustrations) route to zasset instead."
---

# zdesign

产品原型阶段的视觉产出 skill。**taste-skill 定调 → 模型交付 HTML/CSS 原型**。

## 核心理念

- **taste-skill 驱动**：所有视觉决策来自 taste-skill 的品味判断，模型不自由发挥。
- **完善交付，不是半成品**：产出必须过【约束】【细节】【验收】三道关，未全过则回炉。
- **轻量自洽**：产出是纯 HTML/CSS（零运行时依赖），浏览器直接打开即所见。
- **统一输出根**：原型统一写入 `prototypes/`，skill 不询问输出路径。

## 何时触发

- 产品原型需要视觉稿时
- 用户说"做个原型"、"设计一下这个页面"、"UI 长什么样"、"帮我 visual design"
- zarchitect 方案阶段需要视觉原型时

**非这里的活**：
- 任何图（架构/流程/ER/白板草图）→ `zdraw`
- 独立图形资产（logo/favicon/banner/插画）→ `zasset`

## 产物契约

- `DESIGN.md`（项目根目录，项目级视觉真相来源；存在即消费，不存在则首次产出）
- `prototypes/<name>.html`（正式原型）
- `prototypes/taste-options/`（临时目录，仅首次无 DESIGN.md 时使用，决策后删除）

## 工作流

### 1. 确认任务

确认：做什么（landing / app screen / component / flow / 风格探索）？给谁用？有无参考？目标设备与断点？

### 2. 检查 DESIGN.md 是否存在

**存在 → Case B（有 DESIGN.md 路径）**
**不存在 → Case A（无 DESIGN.md 路径）**

---

### Case A：无 DESIGN.md（首次）

```
taste-skill 定品味（从零定方向）
    ↓
出 2-3 个 HTML 例子 → prototypes/taste-options/
    ↓
用户选一个（或组合/微调）
    ↓
提炼为 DESIGN.md（项目根目录）+ 删除 taste-options/
    ↓
产出正式原型 → prototypes/<name>.html
    ↓
质量门禁自检
    ↓
交付
```

**步骤详情**：

1. **taste-skill 定品味**：调用合适的 taste-skill（见下方「taste-skill 路由表」），输出品味判断报告（方向、调性、参考、禁忌）。
2. **出 taste-options**：基于品味判断，产 2-3 个不同方向的 HTML 示例，写入 `prototypes/taste-options/`，命名可读（如 `option-a.html`、`option-b.html`、`option-c.html`）。
3. **用户决策**：展示给用户，收集反馈，确定最终方向。
4. **提炼 DESIGN.md**：将选定方向落地为项目根目录 `DESIGN.md`（含 token 级设计系统 + 调性描述 + 禁忌清单）。
5. **清理**：删除 `prototypes/taste-options/` 目录。
6. **产出正式原型**：基于 DESIGN.md 产出完整原型。
7. **质量门禁自检**：过【约束】【细节】【验收】三道关。
8. **交付**：返回文件路径 + 验收结果。

---

### Case B：有 DESIGN.md

```
taste-skill 定品味（基于现有 DESIGN.md 确认/微调方向）
    ↓
直接产出正式原型 → prototypes/<name>.html
    ↓
质量门禁自检
    ↓
交付
```

**步骤详情**：

1. **taste-skill 定品味**：调用合适的 taste-skill，输入包含现有 `DESIGN.md` 内容，确认或微调方向。
2. **直接产出正式原型**：基于 DESIGN.md 产出完整原型。
3. **质量门禁自检**：过【约束】【细节】【验收】三道关。
4. **交付**：返回文件路径 + 验收结果。

> **注意**：有 DESIGN.md 时不走 taste-options，直接产出。 tasted-skill 的作用是防止模型理解偏离用户最新意图。

---

## taste-skill 路由表

每次调用 zdesign 时，根据 brief 特征智能选择最合适的 taste-skill：

| 用户意图 / brief 特征 | 路由到 |
|---|---|
| 常规产品原型，无特殊风格要求 | `taste-skill`（v2） |
| 移动端为主 | `imagegen-frontend-mobile` 或 `taste-skill` |
| 需要先看参考图再动手 | `image-to-code-skill` |
| 重构现有项目 | `redesign-skill` |
| 柔和、高端质感 | `soft-skill` |
| 简洁编辑风格 | `minimalist-skill` |
| 瑞士/先锋/高对比 | `brutalist-skill` |
| 需要导出 DESIGN.md | `stitch-skill` |
| 品牌套件需求 | `brandkit` |
| GPT/Codex 环境 | `gpt-tasteskill` |
| 防止半成品/占位符 | 任何 taste-skill + `output-skill` |

**调用规范**：`Skill: <taste-skill-name>`

---

## 品味落地 DESIGN.md

taste-skill 输出品味判断报告后，提炼为项目根目录 `DESIGN.md`：

```markdown
---
colors:
  primary: "#hex"
  surface: "#hex"
  text: "#hex"
typography:
  display: "Font Name"
  body: "Font Name"
  scale: [12, 14, 16, 20, 24, 32, 48]
rounded: "8px"
spacing: "8px"
---

# 设计方向

**调性**：一句话描述整体气质
**参考**：列出参考链接
**禁忌**：列出忌用清单
```

**DESIGN.md 是项目级视觉真相来源**，后续 zdraw、zasset、zdesign 本身均可消费。

---

## 产出 + 打磨

1. **token → CSS 变量**：将 DESIGN.md 的 token 映射成 `:root` CSS 变量（如 `--color-primary`、`--surface-1`、`--font-display`、`--radius-md`、`--space-lg`）。**全程引用变量，绝不硬编码 hex / px 常数**。
2. **遵守约束硬规则**：见下方【约束】。
3. **打磨细节**：见下方【细节】清单。
4. **浏览器自查**：产出过程中随时可用浏览器打开文件自查。

---

## 【约束】硬规则（产出时强制）

1. **token 强制**：颜色 / 字号 / 圆角 / 间距 100% 来自 DESIGN.md → CSS 变量。禁止硬编码。
2. **防 AI 感红线**：禁默认 indigo / violet 充当主色、禁 emoji 当图标、禁等权重三栏网格、禁"渐变涂色标题"、字号严格按 type scale 不漂移。
3. **响应式**：至少 mobile / desktop 两断点，触控目标 ≥ 44px，内容不横向溢出。
4. **a11y 基础**：语义化标签、文字对比度达 AA、`:focus` 可见、图片有 alt。

---

## 【细节】打磨清单

- **状态完整**：默认 / hover / active / focus / disabled；空 / 加载 / 错误 / 成功。
- **真实文案**：不留 Lorem ipsum、"Button"、"Title"，用贴合场景的占位文案。
- **视觉层级**：主次分明，留白节奏遵循 spacing 阶梯。
- **对齐与栅格**：全局一致。
- **微交互**：过渡用 token 的 motion，克制不浮夸。

---

## 【验收】交付前自检

- [ ] 所有颜色 / 字号 / 圆角 / 间距都引用 CSS 变量（无硬编码）
- [ ] 视觉调性与 DESIGN.md 一致
- [ ] 覆盖需求的所有功能与状态
- [ ] mobile / desktop 响应式都不破
- [ ] a11y 基础过关（对比度 / 语义 / focus）
- [ ] 浏览器打开成品页亲眼确认（web 必做）——调性 / 响应式 / 交互状态与预期一致

**未全过 → 回炉，绝不交付半成品。**

---

## 输出语言（固定，不推导）

产出语言**只有 HTML/CSS**。

## 输出格式

交付时给出：产出文件路径（`prototypes/` 下）+ DESIGN.md 路径 + 验收清单结果（逐项 ✓）。

## 资产

- `references/quality-checklist.md` — 约束 / 细节 / 验收的详细速查
