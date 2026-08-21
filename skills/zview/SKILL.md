---
name: zview
icon: "👁️"
description: "Use when the user wants to view/browse a project's technical docs or specs — openspec proposals/designs/tasks, docs folder — or to run justfile recipes and watch live service logs, or to browse the read-only ZenTao (禅道) bug list when .zgoal/config.yaml exists. Detects openspec/docs/justfile/.zgoal in the project and launches zdashboard for structured spec preview plus real-time just log streaming (start/stop/restart) plus the Bugs view. For UI design artifacts preview use zdesign instead; for driving a bug to a fix/PR use zgoal."
---

# zview

项目洞察 skill:**先拉起 zdashboard → 再看方案文档 + 服务实时日志**。

定位与 zdesign 对称:`zdesign` 看设计产出,`zview` 看项目本身(方案 + 运行)。

## 工作流

### 1. 立即拉起 dashboard
**先于一切**,直接执行:
```bash
npx zdashboard@latest --mode view --dir <项目根> --open
```
默认端口 4190;占用自动顺延。把 URL 给用户,让用户看到界面。

### 2. 探测项目(cwd)
在拉起 dashboard 的同时或之后,探测项目结构:
- `openspec/` 存在 → 方案文档(openspec 结构感知:进行中 / archive / specs)
- `docs/` 存在 → 文档聚合
- `justfile` / `just --list` 可用 → 日志能力(recipes 启停 + 实时流)
- `.zgoal/config.yaml` 存在 → 禅道 bug 列表能力(只读,需 zdashboard ≥ 1.0.0)

把命中的能力告诉用户(如:"检测到 openspec + justfile + .zgoal,可看方案、日志和禅道 bug 列表")。

### 3. 引导使用
- 看方案:左侧文件树点 proposal.md / design.md / tasks.md
- 看日志:点树顶部「服务日志」→ 选 recipe → 启动;支持停止 / 重启 / 清屏,日志 ANSI 彩色 + 自动跟随
- 看禅道 bug:点树顶部「Bugs」→ 列表(#ID / 标题 / 严重度 / 状态 / 指派),按状态筛(全部 / active / resolved / closed),点行跳禅道详情;**只读**
- 文件变更即时刷新;顶栏电源按钮可停止服务

## 边界
- 只读预览,不解析方案内容、不改 openspec(归档等操作用 openspec CLI)
- 日志仅内存本次会话,不做持久化
- bug 数据只读来自禅道(凭据在 .zgoal/config.yaml,由 zgoal 管);修复动作(开 openspec / 开 PR)用 zgoal
- 用户要"看设计原型/token 色板"时 → 用 zdesign
