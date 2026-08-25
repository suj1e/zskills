# Tasks

## 1. 定义 batch 状态 schema
- [ ] 创建 `.zapply/batch-state.schema.json`
- [ ] 定义状态结构：changes、当前批次、并行度、日志、checkpoint

## 2. 编写 batch-prompt.md
- [ ] 创建 `skills/zapply/references/batch-prompt.md`
- [ ] 定义 batch 执行指令：扫描 → 分析 → 确认 → 执行 → 监控 → 报告
- [ ] 加入并行控制逻辑
- [ ] 加入 checkpoint 读写指令
- [ ] 加入状态持久化指令

## 3. 更新 craftsman-prompt.md
- [ ] 在现有 prompt 中加入 batch 模式支持
- [ ] 加入 checkpoint 进度汇报格式
- [ ] 加入自动重试机制（失败时如何报告）

## 4. 更新 SKILL.md
- [ ] 在 zapply SKILL.md 中新增 batch 子模式描述
- [ ] 定义 `zapply batch [--parallel N] [--continue]` 接口
- [ ] 描述执行流程和交互点
- [ ] 更新 frontmatter triggers

## 5. 测试和验证
- [ ] 验证 proposal 通过 `openspec validate`
- [ ] 验证 tasks 计数正确
- [ ] 在测试仓库中 dry-run batch 流程
