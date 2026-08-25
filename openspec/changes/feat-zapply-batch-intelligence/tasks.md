# Tasks

## 1. AI 语义依赖推断
- [ ] 在 batch-prompt.md 中加入 LLM 分析指令
- [ ] 定义依赖推断 prompt 模板
- [ ] 实现未声明依赖的识别逻辑
- [ ] 测试准确率（目标 ≥ 80%）

## 2. 冲突预检测
- [ ] 实现文件路径扫描逻辑（解析 design.md / tasks.md）
- [ ] 定义冲突检测算法（交集分析）
- [ ] 在 batch-prompt.md 中加入冲突检测指令
- [ ] 输出冲突报告和建议

## 3. 自动修复机制
- [ ] 编译失败自动修复：
  - [ ] 自动 `pnpm install` / `npm install`
  - [ ] 自动 `git pull` / rebase
  - [ ] 失败则报告
- [ ] 测试失败自动分析：
  - [ ] 识别 flaky test（超时、随机失败）
  - [ ] 识别真实 bug（编译错误、断言失败）
  - [ ] 自动重试 flaky test
- [ ] 工作树冲突自动解决：
  - [ ] `git stash` → `rebase` → `pop`
  - [ ] 冲突无法解决则报告

## 4. 渐进式信任
- [ ] 定义 `.zapply/history.json` 格式
- [ ] 实现用户决策记录（并行度调整、跳过项、快速通过项）
- [ ] 实现策略自动调整逻辑
- [ ] 在 batch-prompt.md 中加入历史参考指令

## 5. 测试和验证
- [ ] 验证 proposal 通过 `openspec validate`
- [ ] 模拟各种失败场景，验证自动修复
- [ ] 验证渐进式信任不影响原有功能
