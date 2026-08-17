---
name: zview
description: "Use when the user wants to view/browse a project's technical docs or specs — openspec proposals/designs/tasks, docs folder — or to run justfile recipes and watch live service logs. Detects openspec/docs/justfile in the project and launches zview-dashboard for structured spec preview plus real-time just log streaming (start/stop/restart). For UI design artifacts preview use zdesign instead."
---

# zview

项目洞察 skill:**探测项目结构 → 拉起 zview-dashboard → 看方案文档 + 看服务实时日志**。

定位与 zdesign 对称:`zdesign` 看设计产出,`zview` 看项目本身(方案 + 运行)。

## 工作流

### 1. 探测项目(cwd)
- `openspec/` 存在 → 方案文档(openspec 结构感知:进行中 / 归档 / 能力 Specs)
- `docs/` 存在 → 文档聚合
- `justfile` / `just --list` 可用 → 日志能力(recipes 启停 + 实时流)

把命中的能力告诉用户(如:"检测到 openspec + justfile,可看方案和日志")。

### 2. 拉起 dashboard
```bash
npx zview-dashboard@latest --dir <项目根> --open
```
默认端口 4190(与 zdesign-dashboard 的 4173 错开,可并行);占用自动顺延。把 URL 给用户。

### 3. 引导使用
- 看方案:左侧文件树点 proposal.md / design.md / tasks.md
- 看日志:点树顶部「服务日志」→ 选 recipe → 启动;支持停止 / 重启 / 清屏,日志 ANSI 彩色 + 自动跟随
- 文件变更即时刷新;顶栏电源按钮可停止服务

## 边界
- 只读预览,不解析方案内容、不改 openspec(归档等操作用 openspec CLI)
- 日志仅内存本次会话,不做持久化
- 用户要"看设计原型/token 色板"时 → 用 zdesign(zdesign-dashboard)
