---
name: zgoal
icon: "🎯"
description: "Use when the user wants to check ZenTao (禅道) bugs and drive one to a fix — list bugs via the official REST OpenAPI (read-only), pick one, open an openspec change as the fix plan (proposal/design/tasks), implement on a branch, track progress by checking off tasks.md, and open a PR. Progress lives in openspec only; ZenTao is never written. For viewing specs/logs/bug list read-only use zview; for doc alignment use zreview."
---

# zgoal

bug 修复闭环 skill:**先拉起 zdashboard → 禅道看 bug(只读)→ openspec 开修复目标 → 分支实施 → tasks 勾进度 → 开 PR**。

定位对称:zdesign 出设计、zview 看项目、zreview 对齐文档,zgoal 管"把一个 bug 修到开 PR"。本质是开目标——MVP 阶段目标 = bug。

## 工作流

### 1. 拉起 dashboard
直接执行:

```bash
npx zdashboard@latest --dir <项目根> --open
```

- 同目录已有活实例:直接复用并打开(**exit 0,非失败**——skill 判断启动成败时,复用不算异常,勿重试)
- 实例已死或无记录:自动起新实例,端口占用自动顺延
- 强制重开(升级 zdashboard 后**必须加**,否则仍用旧版进程):`--restart`;`--page` 与复用兼容,直达对应工作区

把 URL 给用户,让用户看到项目概览 + 文件树。

### 2. 配(一次性)
在 dashboard 运行的同时,查 `<项目根>/.zdev/config.yaml`;没有 → 引导用户创建并**提醒加 .gitignore + chmod 600**:
```yaml
url: https://zentao.example.com
account: me
password: "***"      # 或 token: "***"(免登录)
product: 3           # bug 列表按产品拉(必填)
```

用户不知道 product ID 时:先凭 url/account/password 取 token,再用 api.md 的产品列表端点查出来让用户选。

### 3. 看 bug(只读)
配好后,在已运行的 zdashboard 中切换到 Bugs 视图(侧边栏「禅道 Bugs」),让用户在 Bugs 视图里看和筛(「我的」= 指派给自己的,默认选中)。会话里给一句汇总(如"23 条,我的 8 · active 15 / resolved 6 / closed 2")并问用户挑哪个(或直接给 bug ID)。

### 4. 开目标(openspec)
拉 bug 详情,建 change `openspec/changes/fix-<bugID>-<slug>/`(CLI 可用则 `openspec change new`,否则手建):
- **proposal.md**:bug 复述 + 禅道链接(`{url}/bug-view-{id}.html`)+ 根因分析
- **design.md**:修复方案 + 取舍
- **tasks.md**:checkbox 任务清单(能独立验证的粒度)

Change 开好并提交后,**触发 `ztest` 补测试策略**(design.md 追加「测试策略」+ tasks.md 追加验收标准,同 zapply)。

### 5. 执行(与 zapply 同机制)
- **worktree 隔离**:`git worktree add -b fix/<bugID>-<slug> .zworktree/fix-<bugID>-<slug> <base>`(前提:change 文档已提交)
- 下发 **craftsman** 按 TDD 执行(用 zapply skill 的 craftsman-prompt 模板,后台执行);小 bug 可主智能体自己实施,同样 TDD
- tasks.md 在 worktree 内直接勾,勾选随分支提交
- 常规测试 / lint + 覆盖率核对

### 6. 看进度
在 zdashboard 中切回 view 模式看进度(第 1 步起的实例复用):
```
侧边栏点「项目浏览」即可
```
openspec 进度 + bug 列表一站看(需 zdashboard ≥ 1.0.0;旧版降级为仅会话内表格,不阻塞)。

### 7. 开 PR
三门禁核实(openspec validate + 测试策略核查 + code review,同 zapply)通过后:merge 分支回基线(询问用户)→ 归档 → push → `gh pr create`,body 含:bug 链接、change 路径、tasks 完成度(如 `3/5`)。PR 创建后清理 worktree:`git worktree remove .zworktree/fix-<bugID>-<slug>`。
**合并后提示用户**:禅道手动关 bug(本 skill 纯只读)+ `openspec archive` 归档。

## 边界
- **禅道只读**:绝不调写接口(创建 / 解决 / 关闭 / 激活 / 评论 bug 一律不做)
- 只写 `openspec/`、代码、分支;不动 `.zdev/` 之外的配置
- 凭据只存 `.zdev/config.yaml`,不落日志、不进 git、不回显明文

## 资产
- `references/zentao-api.md` — 端点 / curl 范式 / 字段表 / 错误对照(调用禅道的唯一依据)
