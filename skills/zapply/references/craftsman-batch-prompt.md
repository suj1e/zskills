# Craftsman Batch 执行 Prompt 变体

在 `zapply batch` 模式下，craftsman 除了交付最终结果外，还必须在每完成一个 task 后**汇报进度**，以便主智能体更新 checkpoint。

## 变更点（相对首次模板）

在首次模板的「交付物」之前，追加：

```markdown
## Batch 模式进度汇报

你运行在 batch 模式中，主智能体需要实时知道你的进度。

**每完成一个 task 后，在报告中追加一行**：
```
[CHECKPOINT] task:<task序号>/<总task数> completed:"<当前完成的task描述>"
```

示例：
```
[CHECKPOINT] task:3/8 completed:"实现 OAuth token 刷新接口"
```

**全部完成后，追加汇总行**：
```
[DONE] tasks:<完成数>/<总数> coverage:<覆盖率%> tests:<通过数>/<总测试数>
```

示例：
```
[DONE] tasks:8/8 coverage:94.2 tests:42/42
```

**如果中途遇到无法继续的错误，追加**：
```
[BLOCKED] reason:<错误原因> detail:<详细信息>
```

示例：
```
[BLOCKED] reason:第三方 API 凭证过期 detail:OAuth provider 返回 401，测试环境 token 已失效
```
```

## 交付物（batch 模式必须返回）

- 分支名 / worktree 路径
- 修改文件列表（`git diff --name-only`）
- 测试/lint 输出（通过/失败摘要）
- 覆盖率报告（按 design.md 测试策略的目标逐项核对）
- 任务完成度（x/y）
- **Checkpoint 汇报**（每完成一个 task 一行 `[CHECKPOINT]`）
- **最终汇总**（`[DONE]` 或 `[BLOCKED]` 一行）
- 未完成项与原因、风险、歧义点

## 重跑变体（batch 模式）

在重跑变体的「本轮要求」末尾追加：

```markdown
5. batch 模式下继续汇报 checkpoint：每完成一个 task 追加 `[CHECKPOINT]` 行
6. 如果仍然无法完成，追加 `[BLOCKED]` 行说明原因
```
