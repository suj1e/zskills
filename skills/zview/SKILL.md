---
name: zview
icon: "👁️"
description: "Use when the user wants to view/browse a project's technical docs or specs — openspec proposals/designs/tasks, docs folder — or to run justfile recipes and watch live service logs, or to browse the read-only ZenTao (禅道) bug list when .zdev/config.yaml exists. Detects openspec/docs/justfile/.zdev in the project and launches zdashboard for structured spec preview plus real-time just log streaming (start/stop/restart) plus the Bugs view. For UI design artifacts preview use zdesign instead; for driving a bug to a fix/PR use zgoal."
---

# zview

项目洞察 skill:**拉起 zdashboard → 看方案文档 + 服务实时日志**。

定位与 zdesign 对称:`zdesign` 看设计产出,`zview` 看项目本身(方案 + 运行)。

## 工作流

### 1. 检查/拉起 dashboard
先检查 zdashboard 是否已在运行(访问 `http://localhost:4190/__config`):
- 能访问 → 已有实例在运行,询问用户:「检测到 zdashboard 已在运行,直接使用现有实例还是重新拉最新版?」
  - 用户选「直接使用」→ 沿用当前实例
  - 用户选「重新拉最新版」→ 继续下面的启动流程
- 不能访问 → 直接拉起最新版

拉起:
```bash
npx zdashboard@latest --dir <项目根> --open
```
默认端口 4190;占用自动顺延。把 URL 给用户。

### 2. 探测项目(cwd)
在拉起 dashboard 的同时或之后,探测项目结构:
- `openspec/` 存在 → 方案文档(openspec 结构感知:进行中 / archive / specs)
- `docs/` 存在 → 文档聚合
- `justfile` / `just --list` 可用 → 日志能力(recipes 启停 + 实时流)
- `.zdev/config.yaml` 存在 → 禅道 bug 列表能力(只读,需 zdashboard ≥ 1.0.0)

把命中的能力告诉用户(如:"检测到 openspec + justfile + .zdev,可看方案、日志和禅道 bug 列表")。

### 3. 引导使用
- 看方案:左侧文件树点 proposal.md / design.md / tasks.md
- 看日志:点树顶部「服务日志」→ 选 recipe → 启动;支持停止 / 重启 / 清屏,日志 ANSI 彩色 + 自动跟随
- 看禅道 bug:点树顶部「Bugs」→ 列表(#ID / 标题 / 严重度 / 状态 / 指派),按状态筛(全部 / active / resolved / closed),点行跳禅道详情;**只读**
- 文件变更即时刷新;顶栏电源按钮可停止服务

## 边界
- 只读预览,不解析方案内容、不改 openspec(归档等操作用 openspec CLI)
- 日志仅内存本次会话,不做持久化
- bug 数据只读来自禅道(凭据在 `.zdev/config.yaml`,由 zgoal 管);修复动作(开 openspec / 开 PR)用 zgoal
- 用户要"看设计原型/token 色板"时 → 用 zdesign
