---
name: zapply
icon: "⚙️"
description: "Use when the user wants to drive an openspec change to completion — take a requirement (or an existing change) and run the execution loop: main agent opens the change (proposal/design/tasks), delegates implementation to the craftsman agent, verifies with openspec validate/status, and archives on success. Use when the user says 'implement this', '把需求落地', '跑一下这个 change', '执行 #4'. For ZenTao bug-driven fixes use zgoal; for viewing specs/logs use zview; for design artifacts use zdesign."
---

# zapply

OpenSpec 执行闭环 skill:**需求 → 主智能体开 change → craftsman 实施 → verify → archive**。

定位对称:`zgoal` 管"禅道 bug → fix → PR",`zapply` 管"任意需求/任务 → 落地 → 归档"。共用 openspec + craftsman;zapply **不碰禅道、不开 PR,止于 archive**。

## 工作流

### 1. 收需求 + 开 change(双模式)

**入口分流**:
- 用户给**需求描述** → 主智能体从头开 change(下方 A)
- 用户给**已有 change 路径** → 跳过开 change,直接进第 2 步

**A. 开 change**(`openspec/` 不存在先 `openspec init`):

```bash
openspec new change <yyyy-mm-dd>-<kebab-slug> --description "..."
```

CLI 不可用则手建 `openspec/changes/<name>/`。在 change 目录写三个文件:

| 文件 | 内容 |
|------|------|
| `proposal.md` | 需求复述 + 要解决的问题 + 成功标准 |
| `design.md` | 技术方案 + 取舍(明确哪些做/哪些不做) |
| `tasks.md` | checkbox 清单,粒度到"可独立验证" |

命名:`<yyyy-mm-dd>-<kebab-slug>`,如 `2026-08-20-add-export`。

### 2. 下发 craftsman 执行

下发前先确认 `tasks.md` 粒度足够;太粗就**先细化**(主智能体有权细化 tasks,craftsman 只认细化后清单)。

按 `references/craftsman-prompt.md` 起子智能体 **craftsman**,prompt 必须含:

```markdown
## 上下文
- Change 路径:<change-dir>
- 方案约束:<design.md 核心约束摘要——必做项 + 明确不做的>
- 任务清单:<tasks.md 全量>

## 交付物(必须返回)
- 分支名
- 修改文件列表(git diff --name-only)
- 测试/lint 输出(通过/失败摘要)
- 任务完成度(x/y)
- 未完成项与原因、风险、歧义点
```

**执行原则**:
- craftsman 只改代码 + 勾 tasks.md;**禁止修改 proposal.md / design.md**
- 设计歧义:按最小惊讶原则实现,在报告中标注"歧义点 + 我的选择"
- 不顺手做与任务无关的重构/优化

### 3. 核实(双门禁:openspec verify + code review)

收到报告后,**主智能体跑结构核实,再起独立 code-reviewer 做代码审查**:

**3a. openspec 结构核实**(主智能体自己跑):

```bash
openspec validate <change-dir>    # 校验 change 的 MODIFIED 需求与主 specs 一致性
openspec status --change <name>   # 查看阻塞项
```

> 命令名以本地 `openspec --help` 为准;部分版本该环节叫 verify。

**3b. 代码审查**(起子智能体 **code-reviewer**,按 `references/code-reviewer-prompt.md`):
- **只读**审查分支 diff(相对 base),核对:偏离 design.md 约束?bug / 逻辑错误 / 边界遗漏 / 安全问题?craftsman 报告是否属实(声明的任务真实现了吗)?
- 输出按严重度分级:**blocker**(必须修才能归档)与 **suggestion**(不阻塞,交付时汇报)
- 审查者必须独立于 craftsman 与主智能体,不自审、不修代码

**3c. 主智能体汇总**:validate/status 结果 + code review 报告 + 抽查 diff 与 `git status`(分支干净、无游离文件)

**结果分支**:

| 场景 | 处理 |
|------|------|
| validate 通过 + 无 blocker | → 第 4 步归档(suggestion 一并汇报给用户) |
| 实施问题(任务未完成/测试失败/blocker) | 汇报差异 → 用户选:**重跑 craftsman(带修正上下文)/ 手动修 / 中止** |
| 方案问题(需求理解偏差/设计本身有误) | **主智能体改 proposal.md / design.md / tasks.md** → 回到第 2 步 |

**重跑 craftsman 必须带修正上下文**:上一轮核实差异(validate 结果 + code review blocker)+ 用户决策,结构化追加进 prompt,要求先解决指出的问题、报告时逐条回应。

### 4. 归档

```bash
openspec archive <change-name> --yes
```

> `--yes` 必带(agent 非交互 stdin 关闭时跳过确认);归档默认合并 delta specs 并校验,`--skip-specs` 仅用于纯工具类工作。

归档后汇报:

```markdown
✅ Change 已完成并归档
- change:openspec/changes/<name>/
- 归档:openspec/archive/<name>/
- 分支:<name>
- 任务完成度:x/y
- 修改文件:n 个
```

提示一句:"需要开 PR / merge 分支请说一声"(zapply 止于 archive,不开 PR)。

## 边界

- **不碰禅道**(zgoal 的事)
- **不直接写业务代码**,全部委托 craftsman
- proposal/design 的生成与调整只在主智能体手里,craftsman 只执行
- 核实 = openspec validate + code-reviewer **双门禁**;blocker 未清零不归档
- verify 失败**不自动重试**,必须用户决策
- **归档前双门禁必须全过**
- 止于 archive,不开 PR、不 push

## 可视化进度(zdashboard)

执行过程中可拉起 dashboard 看进度:

```bash
npx zdashboard@latest --mode apply --dir <项目根> --open
```

面板展示:进行中的 change 卡片(名称 + 任务完成度百分比) + 点击展开 proposal/design/tasks 全文。文件变更即时刷新。

## 资产

- `references/craftsman-prompt.md` — craftsman 子智能体 prompt 模板(含重跑变体与交付物规范)
- `references/code-reviewer-prompt.md` — code-reviewer 审查 prompt 模板(分级输出规范)
