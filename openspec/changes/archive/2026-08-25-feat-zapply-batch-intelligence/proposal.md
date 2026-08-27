# feat-zapply-batch-intelligence

## 问题
1. 依赖推断依赖人工声明，未声明的依赖无法识别
2. 并行执行时文件冲突无法预检测
3. 失败后只能重试，无法自动修复
4. 没有学习机制，每次执行重复相同决策

## 方案
引入 AI 驱动智能增强：

1. **AI 语义依赖推断**：用 LLM 分析 `proposal.md` + `design.md`，推断隐含依赖关系
2. **冲突预检测**：扫描 `design.md` / `tasks.md` 涉及的文件路径，提前发现文件级冲突
3. **自动修复**：
   - 编译失败 → 自动 `pnpm install` / `git pull` / 重新 rebase
   - 测试失败 → 分析日志，区分 flaky test 和真实 bug
   - 工作树冲突 → 自动 `git stash` → `rebase` → `pop`
4. **渐进式信任**：记录用户决策历史（`.zapply/history.json`），自动调整策略：
   - 用户上次调整了并行度 → 记住偏好
   - 用户跳过了某类 change → 下次自动跳过
   - 用户快速通过了某类 change → 下次自动执行

## 范围
- `skills/zapply/references/batch-prompt.md`：新增 AI 分析和自动修复指令
- `.zapply/history.json`：决策历史存储格式
- `skills/zapply/SKILL.md`：更新 batch 模式指令

## 验收标准
- 未声明的依赖可被 AI 识别（准确率 ≥ 80%）
- 文件冲突在启动前可被检测
- 编译/测试/冲突失败可自动修复（成功率 ≥ 80%）
- 系统记录用户决策并自动调整下次执行策略
- 渐进式信任不影响原有功能
