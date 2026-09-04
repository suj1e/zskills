# feat-zshow-skill

## Why
讨论逻辑/流程/结构时纯文字说不清——需要"会话内可视化讲解"角色：伪代码/调用树/组件树/文件树/diff/Mermaid/单文件 HTML，即讲即走零沉淀。与 zdraw 边界清晰：zshow 交付"懂"，zdraw 交付图资产文件。

## What Changes
- 新增 `skills/zshow/`（用户引入的 show-me 按家规合规化：name 对齐目录、icon、中英触发词、正文中文、`.zdev/show/` 落盘契约、与 zdraw 边界）
- 修复：test-zs SKILLS 数组补 "zdraw"（此前遗漏，其专项断言从未运行）
- test-zs py_compile 改探测式（python3 → python 回退，规避 Windows 商店占位符）
- 配套：README Skills 表、AGENTS.md、版本 0.12.0 → 0.13.0

## 验收标准
- just test 全绿（SKILLS 含 zdraw + zshow，zdraw 专项断言首次真实运行且通过）
- 版本双文件对齐 0.13.0
