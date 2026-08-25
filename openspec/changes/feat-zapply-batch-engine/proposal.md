# feat-zapply-batch-engine

## 问题
zapply 目前只支持单 change 串行执行。当有多个独立/半独立变更时，无法批量处理，效率低下，人工监督成本高。

## 方案
新增 `zapply batch` 子模式，实现批量并行执行引擎：

1. **批量扫描**：扫描 `openspec/changes/` 下所有未完成的 change
2. **依赖拓扑排序**：解析 `proposal.md` 的 `## 依赖` 节，构建 DAG，自动分层
3. **并行执行**：按批次并行执行，默认并行度 2，可配置
4. **Checkpoint 机制**：记录每个 change 的详细进度（基于 tasks.md），支持断点续跑
5. **状态持久化**：`.zapply/batch-state.json` 记录全局状态
6. **失败隔离**：单个 change 失败不影响其他，自动标记并继续
7. **自动重试**：失败自动重试 2 次（可配置）

## 范围
- `skills/zapply/SKILL.md`：新增 batch 模式完整指令
- `skills/zapply/references/batch-prompt.md`：新建，batch 执行 prompt
- `skills/zapply/references/craftsman-prompt.md`：更新，加入 checkpoint 和自动重试
- `.zapply/batch-state.schema.json`：状态格式定义

## 验收标准
- 可执行 `zapply batch` 启动批量执行
- 支持 `--parallel N` 控制并行度，默认 2
- 支持 `--continue` 断点续跑
- 每个 change 失败不影响其他 change
- 状态持久化到 `.zapply/batch-state.json`
- 自动重试机制生效（最多 2 次）
- Checkpoint 记录每个任务粒度的进度
