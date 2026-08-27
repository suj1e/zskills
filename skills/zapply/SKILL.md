---
name: zapply
icon: "⚙️"
description: "Use when the user wants to EXECUTE and VERIFY existing openspec change(s) — delegate implementation to the craftsman agent (TDD, git worktree isolation), run the three verification gates (openspec validate + test-strategy check + independent code review), smartly merge, and archive. Use when the user says 'implement this', '把需求落地', '跑一下这个 change', '执行 #4', '批量执行', 'batch'. Requirement WITHOUT a change yet, or wanting proposal/design/tests authored first → route to zarchitect."
---

# zapply

OpenSpec 执行与验收 skill:**已有 change → craftsman 实施 → 三门禁核实 → 智能 merge → archive**。

`zapply` 管「既定方案的落地与验收」。开 change(proposal/design/tasks 的编写)是 `zarchitect` 的事,测试策略由 `ztest` 产出;zapply 对它们的产物做核查与执行,不代笔。**不开 PR,止于 archive**。

## 工作流

### 1. 定位 change + 前置校验

**入口分流**:
- 用户给**已有 change**(路径或名称) → 单 change 流程(第 2 步起)
- 用户给**多个 change / 一个前缀**(zarchitect 拆分产物) → 走下方 batch 子模式
- 用户只有**需求描述、尚无 change** → zapply 不开 change;引导先走 `zarchitect`(出方案 + 开 change + 经 ztest 补测试策略),拿到 change 再回来执行
- **前提校验**(任一缺失即拦截):`tasks.md` 存在且粒度可独立验证(太粗主智能体可细化);`design.md` 含「## 测试策略」章节且每个 task 带验收标准——缺测试策略 → 引导先跑 `ztest`,补齐再执行

### 2. 下发 craftsman 执行(TDD,git worktree 隔离)

下发前先确认 `tasks.md` 粒度足够;太粗就**先细化**(主智能体有权细化 tasks,craftsman 只认细化后清单)。

**建 worktree**(单/多 change 统一,主目录零污染、失败可干净放弃):
```bash
git worktree add -b <change-name> .zworktree/<change-name> <base>
```
- `<base>` = 当前基线分支;提醒用户项目 `.gitignore` 加 `.zworktree/`
- **前提:change 文档已提交**(openspec/changes/ 随 git 提交,worktree 从基线切出即包含 proposal/design/tasks)——开 change 后先 commit 再建 worktree
- craftsman 工作目录 = `.zworktree/<change-name>/`(deps 不共享,进去先装)
- tasks.md 就在 worktree 里直接勾,**勾选与代码一起提交在 change 分支上**(merge 后进度自动同步回主目录)

按 `references/craftsman-prompt.md` **完整模板**起子智能体 **craftsman**,用**后台执行**下发(不阻塞会话等结果;完成通知到达后再进第 2.5 步。多 change 并行时同时后台起多个)。核心要求:

**执行原则**:
- craftsman 按 **TDD 红→绿→重构**实现每个 task:先写测试确认失败 → 最小实现跑绿 → 重构保持绿
- 测试必须遵循 `design.md`「测试策略」章节 + `tasks.md` 每个 task 的测试验收标准
- craftsman 只在 worktree 内工作:改代码 + 勾 tasks.md(勾选与代码一起提交在 change 分支);**禁止修改 proposal.md / design.md**
- 设计歧义:按最小惊讶原则实现,并在报告中标注"歧义点 + 我的选择"
- 不顺手做与任务无关的重构/优化
- **不写死魔法常量**:业务阈值/超时/重试/分页等提为命名常量或配置
- **不造轮子,按阶梯**:标准库 → 项目已有 → 成熟开源库(非平凡需求,报告新增依赖+理由+锁定版本)→ 琐碎工具手写;框架级重依赖不在 craftsman 决定范围,停下报告

**交付物**(除模板要求外,必须含覆盖率报告——按 design.md 测试策略目标逐项核对)

### 2.5. 简化润色(可选)

craftsman 交付后、三门禁**之前**,若装有 `code-simplifier` 子智能体,后台起它**在 worktree 内**对分支 diff 做清晰度/一致性简化(保持功能,后台执行):
- 安全网:simplifier 改完**必须复跑全部测试,仍绿才继续**;红了就打回 craftsman/回滚其简化
- 未装 code-simplifier 或用户说跳过 → 直接进第 3 步
- 定位:让 code-reviewer 审的是**最终形态**,结论不过期

### 3. 核实(三门禁:openspec verify + 测试策略核查 + code review)

收到报告后,**主智能体跑结构核实 + 测试核查,再起独立 code-reviewer 做代码审查**:

**3a. openspec 结构核实**(主智能体自己跑):

```bash
openspec validate <change-dir>    # 校验 change 的 MODIFIED 需求与主 specs 一致性
openspec status --change <name>   # 查看阻塞项
```

> 命令名以本地 `openspec --help` 为准;部分版本该环节叫 verify。

**3b. 测试策略核查**(主智能体自己跑):
- 检查 `design.md` 是否包含 `## 测试策略` 章节
- 检查 `tasks.md` 每个 task 是否包含测试验收标准
- 抽查:实际写的测试代码是否覆盖了 design.md「测试策略」章节中指定的场景(边界/异常/并发)
- 覆盖率是否达到 design.md 中设定的目标

**3c. 代码审查**(优先起子智能体 **`zapply-reviewer`**——分层审查:依赖决策阶梯 + 14 维自审,再内调内置 code-reviewer 深审;zagents 仓库提供。dispatch **只注入上下文四要素**:change 路径 / 审查分支 / 方案约束摘要 / craftsman 交付报告要点,**不要灌任何清单模板正文**,清单它自带。未装则降级:派内置 `code-reviewer`,按 `references/code-reviewer-prompt.md` 填充模板派发):
- **只读**审查分支 diff(相对 base),核对 14 维:设计约束、bug/边界/安全、架构合理性、原则与模式、**禁止魔法常量**、**禁止造轮子**、死代码残留、错误与资源、并发与事务、性能、**测试策略遵循**、测试与兼容、依赖与文档同步、风格整洁度、craftsman 报告属实
- 输出按严重度分级:**blocker**(优先修,清零才能归档)与 **suggestion**(同样下发修复,优先级次之;确实不该修的说明理由)
- 审查者必须独立于 craftsman 与主智能体,不自审、不修代码

**3d. 主智能体汇总**:validate/status 结果 + 测试策略核查结果 + code review 报告 + 抽查 diff 与 `git status`(分支干净、无游离文件)。抽查≠复审:全量审查是 reviewer 的职责,主智能体只抽核心任务对应的 2-3 个文件,对照报告验证"声称改的真的改了、无漏报",不做全量重复审查

**结果分支**:

| 场景 | 处理 |
|------|------|
| validate 通过 + 测试策略核查通过 + 无 blocker | → 第 4 步分支收尾(merge 后勾选同步回主目录)→ 第 5 步归档(suggestion 已修复或附不修理由,一并汇报给用户) |
| 测试策略未覆盖/覆盖率不达标 | 汇报差异 → 用户选:**重跑 craftsman(带修正上下文)/ 手动修 / 中止** |
| 实施问题(任务未完成/测试失败/blocker) | 汇报差异 → 用户选:**重跑 craftsman(带修正上下文)/ 手动修 / 中止** |
| 方案问题(需求理解偏差/设计本身有误) | **主智能体改 proposal.md / design.md / tasks.md** → 回到第 2 步 |

**重跑 craftsman 必须带修正上下文**:上一轮核实差异(validate 结果 + code review 全量条目——blocker 优先、suggestion 次之)+ 用户决策,结构化追加进 prompt,要求先 blocker 后 suggestion 逐条解决,报告时逐条回应。

### 4. 分支收尾(主智能体智能 merge)

三门禁通过后**主智能体直接执行智能 merge**,不再逐步询问:**先 merge 再归档**——craftsman 的 tasks.md 勾选提交在 change 分支上,merge 才能把勾选同步回主目录;先归档会把 change 目录挪走,merge 时撞 modify/delete 冲突。

```bash
git checkout <base> && git merge <name> && git branch -d <name>
git worktree remove .zworktree/<name>
```

- 多 change(batch)场景:严格按依赖拓扑序 merge,依赖前缀相同的串行
- **只在这两种情况停下问用户**:merge 冲突(报告冲突点,不强行解)/ 用户明确说过该分支要先留
- 其余情形 merge 完在汇报里带一句结果即可
- 边界不变:只做本地 merge,**不 push、不开 PR**

### 5. 归档

```bash
openspec archive <change-name> --yes
```

> `--yes` 必带(agent 非交互 stdin 关闭时跳过确认);归档默认合并 delta specs 并校验,`--skip-specs` 仅用于纯工具类工作。

归档后汇报:

```markdown
✅ Change 已完成并归档
- change:openspec/changes/<name>/
- 归档:openspec/archive/<name>/
- 分支:<name>(基线:<base>,已 merge / 保留)
- 任务完成度:x/y
- 修改文件:n 个
```

## zapply batch 子模式

当用户有**多个待执行变更**（方案拆分产物、迭代需求集等）时，使用 `batch` 子模式自动编排执行。

### 入口(意图路由,非 CLI 参数)

zapply 是 skill 不是命令——以下均为会话语义,主智能体据此分流:

| 用户说 | 动作 |
|--------|------|
| 「批量执行 / batch / 这批 change 都跑了」 | 进入下方完整流程(默认并行度 2,可在确认环节调整) |
| 「看看批量进度」 | 读 `.zdev/apply/batch-state.json` 向用户汇报批次与 checkpoint |
| 「继续跑 / continue」 | 读 state 断点续跑,跳过已完成项 |
| 「跳过 X」「重试 X」「暂停」「恢复」 | 更新对应状态并写回 state 文件 |

### 完整流程（按 `references/batch-prompt.md` 执行）

1. **扫描**：扫描 `openspec/changes/` 下所有未归档变更
2. **分析**：提取依赖、检测文件冲突、识别风险项（含测试策略缺失→拦截回 ztest）
3. **确认**：展示执行计划（依赖图 + 批次 + 风险项），等待用户确认
4. **执行**：按批次并行调度 craftsman，后台执行
5. **监控**：实时读取 checkpoint 进度，处理异常（环境类故障自动修复,实现类问题带修正上下文自动重跑）
6. **核实**：每项逐一过**三门禁**(validate + 测试策略核查 + code-reviewer);blocker 自动带修正上下文重跑 craftsman 至清零,suggestion 一并修复;仍不过 → 该项 failed/parked,**不阻塞其他项**
7. **合并归档**：本批全过后按依赖序**智能 merge**,归档,生成执行报告

### 关键机制

| 机制 | 说明 |
|------|------|
| **依赖拓扑排序** | 读取 `proposal.md` 的 `## 依赖` 节，自动分层 |
| **冲突预检测** | 扫描 `design.md` / `tasks.md` 涉及的文件路径，提前发现冲突 |
| **Checkpoint** | 记录每个 task 级进度，支持断点续跑 |
| **失败隔离** | 单个 change 失败不影响其他，自动标记并继续 |
| **自动重试** | 失败自动重试 2 次（可配置） |
| **三门禁照常** | batch 不是降级通道:每项逐一批 validate + 测试核查 + code-reviewer,quality bar 与单 change 完全一致 |
| **智能 merge** | 主智能体按依赖序执行;冲突停下问用户 |
| **状态持久化** | `.zdev/apply/batch-state.json` 记录全局状态 |

### Craftsman 批量模式

batch 模式下使用 `references/craftsman-batch-prompt.md` 代替普通模板。craftsman 需要在每完成一个 task 后汇报 `[CHECKPOINT]` 进度，全部完成后汇报 `[DONE]` 或 `[BLOCKED]`。

### 边界

- **默认全自动**：启动后自动分析、自动执行、自动过门禁,只在(计划确认 / 门禁耗尽仍失败 / merge 冲突)三点停
- **失败不阻塞**：单个 change 失败不影响其他,自动重试 2 次后仍失败才通知
- **parked 项**：高风险项（依赖不明确、影响范围大）自动标记为 parked，需用户确认后执行

## 边界

- **不直接写业务代码**,全部委托 craftsman
- proposal/design 的生成与调整只在主智能体手里,craftsman 只执行
- 核实 = openspec validate + 测试策略核查 + code-reviewer **三门禁**;blocker 未清零不归档
- **单 change 模式**：verify 失败**不自动重试**,必须用户决策
- **batch 模式**：失败自动重试最多 2 次，仍失败才通知用户
- **归档前三门禁必须全过**
- 止于 archive,不开 PR、不 push

## 产出与约定

- 批量状态持久化:`.zdev/apply/batch-state.json`(schema 见资产);单 change 进度天然在 openspec/changes/ 与 worktree 分支上

## 资产

- `references/craftsman-prompt.md` — craftsman 子智能体 prompt 模板(含重跑变体与交付物规范)
- `references/code-reviewer-prompt.md` — code-reviewer 审查 prompt 模板(分级输出规范)
- `references/batch-prompt.md` — batch 子模式主智能体编排 prompt(扫描/分析/确认/执行/报告全流程)
- `references/craftsman-batch-prompt.md` — batch 模式 craftsman 变体(CHECKPOINT/DONE/BLOCKED 协议)
- `references/batch-state.schema.json` — `.zdev/apply/batch-state.json` 状态格式定义
