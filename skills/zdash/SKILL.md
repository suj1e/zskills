---
name: zdash
icon: "📊"
description: "Use when the user wants to open, start, restart, re-pull the visualization panel, or run it in local-dev mode — 拉起/重启/重拉 zdashboard（执行进度 / 批量驾驶舱 / 设计预览 / 文档视图），或跑本地源码版面板联调。Pure launcher. Triggers on '打开面板', '启动面板', '拉起dashboard', '看板', '重启面板', '重拉面板', '面板更新了', '面板不对劲', '本地面板', '联调模式'. Does not read or write any business data."
---

# zdash

面板启动器：在当前项目根**拉起 / 复用 / 重拉 / 本地联调** zdashboard，把 URL 给用户。不理解任何业务语义，不读写任何数据。

## 约定背景

所有 skill 的可视化产物统一写入 `<项目根>/.zdev/` 下各自子目录（`apply/`、`design/` 等），由 zdashboard 内置插件按固定路径读取展示。**端口与实例由 zdashboard 自己记录**在 `<项目根>/.zdev/dashboard.json`（pid / port / root / startedAt），复用判断全靠它——zdash 只消费，不重复记账。

## 三种模式（按用户意图分流）

### 1. 打开（默认）

```bash
npx zdashboard@latest --dir <项目根> --open
```

- 同目录已有活实例 → 复用并打开（**exit 0，非失败**，勿当异常重试）；无 → 新起
- URL 给用户；直达某页加 `#<mode>`（现有模式：`#apply`、`#apply-batch`、`#view`、`#stats`、`#just`、`#design`）
- 端口被占自动 +1，无需干预
- 注意：复用不会升级版本——新发布的版本来**重拉模式**

### 2. 重拉（触发词：重拉 / 重启面板 / 面板更新了 / 面板不对劲）

```bash
npx zdashboard@latest --dir <项目根> --open --restart
```

- `--restart` 杀旧起新，保证跑到**最新发布版**——dashboard 迭代频繁，复用旧进程会驻留旧代码
- 判断口诀：**怀疑面板不是最新，不要诊断，直接重拉**

### 3. 本地联调（触发词：本地面板 / 联调模式 / 跑源码面板）

给面板开发者用——跑本地源码而非 npm 包：

1. **定位源码目录**，优先级：用户当场给的路径 → 兄弟目录约定 `<项目根>/../zdashboard` → 问用户
2. **构建并启动**（在源码目录执行）：

   ```bash
   pnpm build && node dist/cli.js --dir <项目根> --open --restart
   ```

   `--restart` 顶掉可能在跑的 npm 版实例；改了源码后重跑这两条即是热重拉
3. 汇报必须标注「**本地联调版**」；切回正式版 = 模式 1 加 `--restart`

## 边界

- 不写业务数据、不改配置；凭据等敏感配置由各业务 skill 自管
- 不判空面板、不解释页内内容——止步浏览器
- `.zdev/dashboard.json` 的 pid/port 由 zdashboard 维护，zdash 只消费
