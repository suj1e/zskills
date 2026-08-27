---
name: zdoc
icon: "📝"
description: "Use when the user wants to write or update documentation — README, API docs, code comments, changelog, user guides, migration docs, onboarding guides. Triggers on '写文档', '更新 README', '写 API 文档', 'changelog', '文档整理'. For design artifact authoring use zdesign."
---

# zdoc

文档编排 skill:**接单定纲 → 收集素材 → 协调配图 → 派发 docwriter 执笔 → 验收 → commit+push 交付**。

zdoc 自己不逐字执笔——写作由 `docwriter` 子智能体(zagents 提供)完成,它自带"示例必真实 / 绝不编造 / 术语锁定"三纪律;未装则本 skill 按同款纪律兜底自写。

## 何时触发
- 用户说"写文档"、"更新 README"、"写 API 文档"、"changelog"、"文档整理"
- 新功能上线后需要写文档（README、API 文档、使用指南）
- 架构变更后需要更新架构文档或迁移指南
- 代码注释过少或过时，需要补充/整理
- 需要写 changelog（版本变更记录）
- 需要写 onboarding 文档（新成员上手指南）
- 需要整理现有文档，统一风格和结构
- zarchitect 出完设计方案后，需要把方案转化为可读的设计文档

## 工作流

### 1. 接单：明确文档类型和目标读者
和用户确认：
- 文档类型（README / API 文档 / changelog / 迁移指南 / 代码注释 / 设计文档）
- 目标读者（终端用户 / 开发者 / 运维 / 新成员）
- 输出路径（如已知；未指定则按项目惯例——README 在根目录、其余在 `docs/`）

### 2. 收集素材
- 用 `Read` 阅读源码、注释、设计文档
- 用 `Explore` 子智能体扫描代码库，理解整体结构和模块职责
- 用 `WebSearch` / `WebFetch` 查外部资料（同类项目的文档风格、行业规范）
- 查看现有文档的风格、术语、结构，保持一致性

### 3. 大纲确认
确定文档大纲和关键要点，用层级列表展示给用户确认（长文档必须确认）。

### 4. 配图（图文并茂，必须——编排层职责）
使用 `diagram-design` 技能生成文档所需图表：
- 架构图（architecture）/ 流程图（flowchart）/ 时序图（sequence）/ ER 图（erd）/ 数据流图（data-flow）

**落盘契约**：服务于 openspec change 的放对应 change 目录下的 `diagrams/`;README、changelog 等独立文档的配图回落 `docs/diagrams/`。
涉及页面/UI 设计的转介 `zdesign` 产出带品牌风格的设计稿。

### 5. 派发执笔（docwriter）
组装**指令五要素**交给 `docwriter`(可后台执行):

| 要素 | 内容 |
|------|------|
| 类型 + 模式 | 新写 / 优化 / 调整 |
| 读者 | 谁,理解水平如何 |
| 大纲 | 第 3 步确认过的章节结构 |
| 素材索引 | 文件路径 : 为何相关 / 重点段落 |
| 落盘目标 | 输出路径 + 图表清单(已产出的相对路径) |

> 不要灌任何额外风格范文正文——纪律(docwriter 自带):示例必摘真实代码、绝不编造、术语锁定。未装 docwriter 则自写并执行同款三纪律。

### 6. 验收
- 章节结构与确认过的大纲对齐(偏离须有理由)
- 取证依据可信:抽查 2-3 处代码示例与源码一致
- 图示以相对路径正确嵌入且文件存在
- 术语全文一义;面向读者的深度合适
- 待确认清单被显式列出而非悄悄略过

### 7. 交付 = 写入 + commit + push
全部文件落盘并验收通过后:

```bash
git add <涉及文档与图> && git commit -m "docs: <主题>" && git push
```

交付完成态 = 文件在库里、远端已同步(沿 zarchitect 先例)。汇报包含:文件路径清单 + 图示索引 + 待确认项。

## 输出格式

````markdown
## 文档类型
<README / API 文档 / CHANGELOG / 迁移指南 / 设计文档 / 其他>

## 目标读者
<终端用户 / 开发者 / 运维 / 新成员>

## 完整内容
<正文图文并茂,含相对路径图引>

## 图示索引
| 图 | 相对路径 | 说明 |

## 待补充（可选）
<不确定、需用户确认的内容>
````

## 约束
1. **不改业务代码**——文档与图是唯一产物;交付以「写入 + commit + push」为完成态,飘在会话里的内容等于没写。
2. 保持与现有文档的风格一致（术语、格式、语气），不引入全新风格。
3. 不编造 API 行为或代码逻辑——不确定先读源码,读不懂标「待补充」。
4. 面向用户的技术文档避免内部实现细节;面向开发者的文档可以到实现细节。
5. 代码示例必须与实际代码一致,手写示意必须显式标注。
6. changelog 时间倒序,每条注明变更类型（feat / fix / refactor / docs 等）。
7. 文档必须图文并茂——没有图的 README / 设计文档视为不完整。
