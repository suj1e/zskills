---
name: zgoal
description: "Use when the user wants to check ZenTao (禅道) bugs and drive one to a fix — list bugs via the official REST OpenAPI (read-only), pick one, open an openspec change as the fix plan (proposal/design/tasks), implement on a branch, track progress by checking off tasks.md, and open a PR. Progress lives in openspec only; ZenTao is never written. For viewing specs/logs/bug list read-only use zview; for doc alignment use zreview."
---

# zgoal

bug 修复闭环 skill:**禅道看 bug(只读)→ openspec 开修复目标 → 分支实施 → tasks 勾进度 → 开 PR**。

定位对称:zdesign 出设计、zview 看项目、zreview 对齐文档,zgoal 管"把一个 bug 修到开 PR"。本质是开目标——MVP 阶段目标 = bug。

## 工作流

### 1. 配(一次性)
查 `<项目根>/.zgoal/config.yaml`;没有 → 引导用户创建并**提醒加 .gitignore + chmod 600**:
```yaml
url: https://zentao.example.com
account: me
password: "***"      # 或 token: "***"(免登录)
product: 3           # bug 列表按产品拉(必填)
```

用户不知道 product ID 时:先凭 url/account/password 取 token,再用 api.md 的产品列表端点查出来让用户选。

### 2. 看 bug(只读)
按 `references/zentao-api.md`:取 token → `GET /products/{product}/bugs` → 会话内出紧凑表(ID / 标题 / 严重度 / 状态 / 指派),默认关注 `active`。用户挑一个,或直接给 bug ID 进下一步。
列表也可在 zview-dashboard 的「Bugs」视图看(≥0.2.0)。

### 3. 开目标(openspec)
拉 bug 详情,建 change `openspec/changes/fix-<bugID>-<slug>/`(CLI 可用则 `openspec change new`,否则手建):
- **proposal.md**:bug 复述 + 禅道链接(`{url}/bug-view-{id}.html`)+ 根因分析
- **design.md**:修复方案 + 取舍
- **tasks.md**:checkbox 任务清单(能独立验证的粒度)

### 4. 执行
开分支 `fix/<bugID>-<slug>` → 按方案实施 → **每完成一个 task 立刻勾 tasks.md**(进度唯一真相在这里)→ 常规测试 / lint。

### 5. 看进度
```bash
npx zview-dashboard@latest --dir <项目根> --open
```
openspec 进度 + bug 列表一站看(需 zview-dashboard ≥ 0.2.0;旧版降级为仅会话内表格,不阻塞)。

### 6. 开 PR
push → `gh pr create`,body 含:bug 链接、change 路径、tasks 完成度(如 `3/5`)。
**合并后提示用户**:禅道手动关 bug(本 skill 纯只读)+ `openspec archive` 归档。

## 边界
- **禅道只读**:绝不调写接口(创建 / 解决 / 关闭 / 激活 / 评论 bug 一律不做)
- 只写 `openspec/`、代码、分支;不动 `.zgoal/` 之外的配置
- 凭据只存 `.zgoal/config.yaml`,不落日志、不进 git、不回显明文

## 资产
- `references/zentao-api.md` — 端点 / curl 范式 / 字段表 / 错误对照(调用禅道的唯一依据)
