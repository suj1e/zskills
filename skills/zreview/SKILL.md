---
name: zreview
icon: "✅"
description: "Use when the user wants to review and decompose a batch of documents — product briefs, PRDs, design docs, specs, presentations, spreadsheets. Scans and parses docx/pptx/xlsx/md/pdf, extracts requirements, detects conflicts/gaps/ambiguities across documents, generates review items, and launches zdashboard for item-by-item alignment. Use when the user says 'review these docs', '评审这批文档', '需求拆解', '看看有没有冲突'."
---

# zreview

多文档需求评审与拆解 skill:**喂一批文档 → 扫描解析 → 预审摘要 → zdashboard 分组对齐 → 输出报告 + 下一站建议**。

定位对称:`zdesign` 出设计、`zview` 看项目、`zarchitect` 出方案、`zapply` 落地,zreview 管"读一堆文档并评审拆解"。

## 何时触发
- 用户给一批文档(docx / pptx / xlsx / md / pdf / txt),"评审一下"、"看看有没有冲突"、"帮我拆解"
- 用户给文件夹路径,里面是需求/产品/技术文档
- 多文档交叉比对:找冲突、缺口、歧义、重复

## 工作流

### 1. 收文档集

用户给**文件夹路径**或**文件列表**。

扫描目录,识别可解析文档:
- `.md` / `.markdown` / `.txt` — 直接读取
- `.docx` — 用 `docx` skill 解析
- `.pptx` — 用 `pptx` skill 解析
- `.xlsx` / `.xls` / `.csv` — 用 `xlsx` skill 解析
- `.pdf` — 用 `pdf` skill 解析

汇总文档清单(文件名 + 类型 + 大小),展示给用户确认。用户可剔除不需要的文档。

### 2. 扫描解析

逐份解析,输出到 `.zreview/docs/` 目录:

- 每份文档 = 一个 `.md` 文件,文件名 = 原文件名(扩展名改为 `.md`)
- 文件头加 frontmatter 标注来源:
  ```yaml
  ---
  source: docs/brief.docx
  parsedAt: "2026-08-24T10:00:00Z"
  ---
  ```
- 解析出的纯文本放在 frontmatter 之后
- 表格(xlsx)转 markdown 表格,ppt 每页用 `---` 分隔

### 3. 预审摘要

通读所有解析后的文档,输出 **5 行以内** 的预审摘要:

```
扫描 5 份文档,提取 23 个需求点:
- 4 处冲突(目标用户/支付方式/...)
- 7 处缺口(性能指标/权限模型/...)
- 3 处歧义("快速响应"/"灵活配置"/...)
- 建议优先看:冲突 > 缺口 > 歧义
```

展示给用户,用户可以:
- 确认摘要,进入下一步
- 调整重点:"冲突不用管,只看缺口和歧义"
- 补充文档

### 4. 拉评审台

```bash
npx zdashboard@latest --mode review --dir .zreview --open
```

给用户 URL。

### 5. 生成评审项

在 `.zreview/review.yaml` 中写入评审项,按 **5 种类型** 生成:

```yaml
status: reviewing
summary: "扫描 5 份文档,提取 23 个需求点,发现 4 处冲突、7 处缺口、3 处歧义"

items:
  # 冲突:两篇以上文档对同一事实/需求表述矛盾
  - id: c1
    type: conflict
    severity: high
    state: open
    title: "目标用户范围不一致"
    sources:
      - doc: docs/brief.md
        quote: "目标用户是企业客户(B2B)"
      - doc: docs/prd.xlsx
        quote: "支持个人用户注册"
    question: "确认目标用户范围?"
    answer: ""

  # 缺口:文档提到功能/需求但未定义清楚
  - id: g1
    type: gap
    severity: medium
    state: open
    title: "支付方式未定义"
    doc: docs/prd.xlsx
    context: "第 3 章提到支付功能,但未说明支持哪些支付渠道"
    question: "需要支持哪些支付方式?"
    answer: ""

  # 歧义:表述模糊需要澄清
  - id: a1
    type: ambiguity
    severity: medium
    state: open
    doc: docs/requirements.md
    context: "'系统应快速响应'——未定义性能指标"
    question: "'快速'的具体指标是什么?"
    answer: ""

  # 拆解:需求按模块/功能/里程碑拆解
  - id: d1
    type: decomposition
    severity: low
    state: open
    title: "用户管理模块"
    priority: high
    children:
      - id: d1-1
        type: decomposition
        title: "登录注册"
        priority: high
        state: open
        children:
          - id: d1-1-1
            type: decomposition
            title: "手机号注册"
            priority: high
            state: open
          - id: d1-1-2
            type: decomposition
            title: "第三方登录"
            priority: medium
            state: open
      - id: d1-2
        type: decomposition
        title: "用户信息管理"
        priority: medium
        state: open

diagrams:
  - path: diagrams/decomposition.html
    title: "需求拆解图"
    type: tree
  - path: diagrams/issues.html
    title: "问题分布图"
    type: bar
```

**类型定义:**

| type | 含义 | severity 默认 | 生成规则 |
|------|------|--------------|----------|
| `conflict` | 多文档对同一事实/需求表述矛盾 | high | 同一概念在不同文档中有矛盾描述 |
| `gap` | 文档提到但未定义清楚 | medium | 功能被提及但缺少关键细节(参数/边界/流程) |
| `ambiguity` | 表述模糊需要澄清 | low | 措辞含糊("可能"/"适当"/"快速")无可度量标准 |
| `decomposition` | 需求拆解为模块/功能 | low | 从需求中提取功能点,按层次组织 |

**生成要求:**
- 冲突必须有 `sources`(至少两份文档引用)
- 缺口和歧义必须有 `context`(说明为什么这是个问题)
- 拆解粒度:一个 change = 一个可独立验证的模块/功能
- 拆解树深度不超过 3 层
- id 格式:`c1-c2`(冲突)、`g1-g2`(缺口)、`a1-a2`(歧义)、`d1-d2`(拆解)

### 5.5 生成可视化(必须)

评审项生成后,**必须**使用 `diagram-design` skill 生成以下图表,存到 `.zreview/diagrams/`:

**图 1: 需求拆解图** (decomposition diagram)
- 从 `decomposition` 类型 item 提取树形结构
- 使用 diagram-design 的 **tree** 类型
- 文件名: `.zreview/diagrams/decomposition.html`
- 展示模块 → 功能 → 子功能 的层次结构,标注 priority(高/中/低)

**图 2: 问题分布图** (issue distribution)
- 统计 conflict/gap/ambiguity 数量
- 使用 diagram-design 的 **bar** 或 **quadrant** 类型
- 文件名: `.zreview/diagrams/issues.html`
- 展示问题类型分布和严重度

**图 3: 需求全景图** (requirements overview, 可选)
- 如果文档涉及系统架构/数据流,使用 diagram-design 生成架构图/数据流图
- 文件名: `.zreview/diagrams/overview.html`
- 根据文档内容选择合适类型:architecture / data-flow / sequence 等

在 review.yaml 末尾追加 diagrams 节:

```yaml
diagrams:
  - path: diagrams/decomposition.html
    title: "需求拆解图"
    type: tree
  - path: diagrams/issues.html
    title: "问题分布图"
    type: bar
```

### 6. 引导对齐

在 zdashboard 评审视图中逐项处理:

**冲突项:**
- 并排展示两份文档的原文引用
- 用户选择采纳哪方,或给出 reconciled 答案

**缺口项:**
- 展示上下文,用户补充缺失信息

**歧义项:**
- 展示模糊表述,用户澄清或给出量化标准

**拆解项:**
- 树形结构展示,可展开/折叠
- 可调整 priority(high/medium/low)
- 可新增/删除子项
- 可修改 title
- 不可拖拽排序(先不做,复杂度高)

**操作按钮:**
- 答复 + 采纳 / 驳回 / 撤销(同旧流程)
- 拆解项额外:新增子项 / 删除 / 改 priority

**全部处理完后**点顶栏【通过评审】。

### 7. 输出报告 + 出口建议

评审通过后,生成结构化报告:

```markdown
## 评审摘要
- 文档:5 份
- 需求点:23 个
- 冲突:4 处(已解决 4)
- 缺口:7 处(已解决 7)
- 歧义:3 处(已解决 3)
- 拆解:3 个模块 / 8 个功能

## 未解决问题
(无,或列出确实无法确定的问题)

## 下一站建议
- 技术类 → `/zarchitect` 出技术方案
- 产品类 → `/zdesign` 出原型
- 需求已清晰 → `/zapply` 直接落地
```

## 边界
- 单人 + AI 评审官场景;多人协作(署名/同步)不在范围
- 评审数据是本地 yaml,无数据库
- 只写 `.zreview/` 目录;不改项目其他文件
- 拆解粒度止于模块/功能,不细化到 tasks.md(那是 zapply 的事)
- 文档解析用对应 skill,不在本 skill 内实现解析器
