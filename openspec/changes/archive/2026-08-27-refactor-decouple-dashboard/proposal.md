# refactor-decouple-dashboard

## Why
契约定稿：skill 零启动命令、可视化产物统一写入 `<项目根>/.zdev/<域>/`、图随 change 走。深度使用反馈：zarchitect 完全覆盖 zreview 的文档分析场景；禅道闭环与项目导览不再需要。据此裁剪 skill 库并完成解耦。

## What Changes
- **删除 3 个 skill**：`zgoal`、`zreview`、`zview`（含各自 references）
- 新建 `zdash` 纯启动器（详见 feat-zdash-skill）
- **数据路径迁移**：`.zapply/` → `.zdev/apply/`；batch-state.schema.json 移入 `skills/zapply/references/`
- **指针清理**：全部 description/定位对称/边界中的 zgoal/zview/zreview/禅道 引用移除
- **zapply**：删除旧版「多 change 并行编排」章节，统一指向 batch 子模式；资产清单补齐 batch 三件套
- **zdesign**：产出根收窄为 `.zdev/design/`；删断链 assets 引用与启动命令块；预览职责归 zdash
- **zdoc**：删 dashboard 访问句、修正交付视角措辞
- **图路径约定落文**：zarchitect/zdebug/ztest/zdoc 统一为 `openspec/changes/<slug>/diagrams/`，独立文档配图回落 `docs/images/`

## 验收标准
- skills/ 仅剩 zapply / zarchitect / zdash / zdebug / zdesign / zdoc / ztest 七个
- grep 无 `npx zdashboard` 启动命令出现在 zdash 以外的任何 skill
- grep 无 zgoal / zview / zreview / 禅道 残留引用
- 各产物路径符合 `.zdev/<域>/` 与 change `diagrams/` 约定
- openspec validate 通过
