---
name: zarchitect
icon: "🏗️"
description: "Use when the user wants to design a solution — technical architecture, module breakdown, interface design, flow restructuring, or anything that needs thinking before coding. Triggers on '帮我设计一下', '怎么架构', '方案设计', '技术选型'. For design artifacts preview use zdesign; for viewing existing specs use zview."
---

# zarchitect

方案设计 skill:**探索 → 多轮 brainstorm → 画图 → 图文并茂的设计文档 → 开 openspec change**。

## 何时触发
- 用户说"帮我设计一下"、"怎么架构"、"方案设计"、"技术选型"
- 涉及多个模块/服务/接口变更，需要先出方案再落地
- 架构拆分、流程梳理、数据流设计
- 需要画架构图/流程图/时序图让用户理解

## 工作流

### 1. 探索
- 优先用 `openspec view` 看现有规范和变更；如果项目未初始化 openspec 或命令失败，跳过，直接用 `Explore` 扫描代码库
- 用 `Explore` 子智能体做广域代码库扫描，理解现有架构和依赖关系
- 必要时用 `WebSearch` / `WebFetch` 查外部资料

### 2. 多轮交互 ask user 4~6 questions
基于探索结果，主动抛出 4-6 个关键问题（边界、优先级、约束、不想碰的东西、deadline、现有系统里你不知道的细节）。这一轮聚焦在「理解问题」，不在解决方案上——和用户来回对话，直到双方对「问题是什么、往哪个方向解」达成初步共识。

### 3. 抛出初步思路
基于共识，主动抛出 2-3 个方向草图（文字描述 + 各自的 trade-off）。

### 4. 来回对话
用户可能推翻你的假设、补充你没想到的约束、或者指出现有系统里有你不知道的东西。继续多轮交互。

### 5. 再次对齐确认
经过方向调整后，再次和用户确认「问题定义 + 推荐方向」达成共识。不要跳过这个确认就直接写文档。

### 6. 正式方案设计
在共识基础上输出完整方案。

### 7. 画图（图文并茂，必须）
使用 `diagram-design` 技能生成架构图、流程图、时序图、数据流图、ER 图等。
常用类型：architecture、flowchart、sequence、data-flow、component、state-machine、erd。
图产出后放在项目目录下的 `docs/design/` 或 `openspec/designs/`，并在设计文档中引用路径。
如果设计方案涉及页面/UI，使用 `zdesign` 技能生成带品牌风格的 HTML/CSS 设计稿。

### 8. 写文档
输出结构化设计文档，包含：背景与目标、现有系统分析、方案设计（图文）、接口/数据契约、实施步骤、风险与 trade-off、开放问题。

### 9. 开 Change
执行 `openspec new change <yyyy-mm-dd>-<kebab-slug> --description "..."`，在 `openspec/changes/<slug>/` 下写入 `proposal.md` 和 `design.md`，让设计方案进入可执行状态。

### 10. 交付
列出「设计方案 + 关键图 + 推荐方案 + 开放问题 + openspec change 路径」，交给用户决策。

## 输出格式
## 背景与目标
<一段话说明为什么要做这个设计>

## 现有系统分析
- <现有架构的关键组件和依赖关系>
- <已知限制或技术债>

## 方案设计
### 方案 A：<名称>
- 思路：<核心思路>
- 图示：<图文件路径>
- 优点：<...>
- 缺点：<...>

### 方案 B：<名称>（可选）
- ...

## 推荐方案
<推荐哪个方案 + 理由>

## 接口 / 数据契约
<如有，列出关键接口签名、数据结构、消息格式>

## 实施步骤
1. <步骤 1>
2. <步骤 2>
...

## 风险与 Trade-off
- <风险 1>：<缓解措施>
- <开放问题 1>：<需要用户确认的点>

## 图示索引
| 图 | 路径 | 说明 |
|---|---|---|
| <架构图> | <路径> | <说明> |

## OpenSpec Change
- <change 路径：openspec/changes/<slug>/proposal.md>

## 约束
1. 不修改代码、不执行 Git 操作——只出方案和图。
2. 方案必须附带图——没有图的设计文档视为不完整。
3. 有多个可行方案时，列出 trade-off，不自行拍板"就这么干"。
4. 遇到安全、合规、性能敏感的设计点，明确标注为「需确认」。
5. 不编造不存在的 API 或框架能力——不确定的先查，查不到就写「待确认」。
6. 方案输出后开 openspec change 进入可执行状态，不等于自己开始实施。
