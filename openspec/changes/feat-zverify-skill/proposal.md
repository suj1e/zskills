# feat-zverify-skill

## Why
现有 8 个 skill 覆盖了"做"（zarchitect 出方案、zapply 执行验收），但缺"验真"——用户有产品文档或口述的功能清单，想知道**实际代码实现了多少、做成什么样**（如"报告里的图表实现，我需要一一核对"），无 skill 认领。与已删 zreview 区别：那是开发前评审拆解，zverify 是开发后实现核实。

## What Changes
- 新增 `skills/zverify/`：功能点 ↔ 代码实现一致性核查
  - 输入双源平等：产品文档（docx/pptx/xlsx/md/pdf）或用户口述清单
  - 工作流：提功能点清单（含实现判据对齐）→ 按模块聚类定证据锚点 → 后台并行派发只读探索子智能体（Explore / code-explorer）取证 → 四态裁定（✅/🟡/❌/⚠️，低置信度强制二次复核）→ 报告会话内交付(默认零落盘,用户要求才存档)
  - 差距清单只列不流转，转 zarchitect 由用户点名
  - 边界：只读核查（可跑测试/构建作辅助证据，不改源码）；`.zdev/verify/` 不 commit
- 配套：test-zs SKILLS 数组、README Skills 表、AGENTS.md、版本 0.7.0 → 0.8.0

## 验收标准
- `just test` 全绿（SKILLS 含 zverify、全局约定检查通过：无 npx、无面板耦合）
- `openspec validate feat-zverify-skill --type change` 通过
- 版本双文件对齐 0.8.0
