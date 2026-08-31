---
name: zdash
icon: "📊"
description: "Use when the user wants to open, start, restart, or re-pull the visualization panel — 拉起/重启/重拉 zdashboard（执行进度 / 批量驾驶舱 / 设计预览 / 文档视图）。Pure launcher. Triggers on '打开面板', '启动面板', '拉起dashboard', '看板', '重启面板', '重拉面板', '面板更新了', '面板不对劲'. Does not read or write any business data."
---

# zdash

面板启动器：在当前项目根**拉起 / 复用 / 重拉** zdashboard，把 URL 给用户。不理解任何业务语义，不读写任何数据。

## 约定背景

所有 skill 的可视化产物统一写入 `<项目根>/.zdev/` 下各自子目录（`apply/`、`design/` 等），由 zdashboard 内置插件按固定路径读取展示。**端口与实例由 zdashboard 自己记录**在 `<项目根>/.zdev/dashboard.json`（pid / port / root / startedAt），复用判断全靠它——zdash 只消费，不重复记账。

## 两种模式（按用户意图分流）

### 1. 打开（默认）

```bash
nohup npx zdashboard@latest --dir <项目根> --open > .zdev/dashboard.log 2>&1 &
```

- **后台驻留是默认姿势**：进程脱离会话存活，命令立即返回，不阻塞对话（用 Bash 工具的后台执行或 `nohup … &`）
- 日志统一落 `.zdev/dashboard.log`——「面板不对劲」时先看它
- 同目录已有活实例 → 复用并打开（**exit 0，非失败**，勿当异常重试）；无 → 新起
- URL 给用户；直达某页加 `#<mode>`（现有模式：`#market`、`#view`、`#stats`、`#just`、`#design`）
- 端口被占自动 +1，无需干预
- 注意：**复用不会升级版本**——发包后想看新版，走重拉模式
- npx 缓存按 spec 字符串分槽，多版本槽位共存属正常；重拉模式钉版本号后天然命中正确槽位

### 2. 重拉（触发词：重拉 / 重启面板 / 面板更新了 / 面板不对劲）

**先解析后钉版**——`@latest` 受 npx 多槽位缓存影响，钉具体版本号最稳：

```bash
VER=$(npm view zdashboard version --prefer-online) && nohup npx -y zdashboard@$VER --dir <项目根> --open --restart > .zdev/dashboard.log 2>&1 &
```

- `npm view --prefer-online` 绕过本地元数据缓存，实时拿 registry 的 latest
- 钉 `@<具体版本>` 直接命中对应缓存槽，绕开 tag 解析歧义与历史老槽位
- `--restart` 杀旧起新——**后台驻留的实例活得久，复用永远给你旧版 UI**；判断口诀：怀疑面板不是最新，不要诊断，直接重拉

## 边界

- 不写业务数据、不改配置；凭据等敏感配置由各业务 skill 自管
- 不判空面板、不解释页内内容——止步浏览器
- `.zdev/dashboard.json` 的 pid/port 由 zdashboard 维护，zdash 只消费
- 已知边界：Windows 下 pid 回收快，活探针可能误判僵尸实例为存活——表现即"复用了不存在的端口"；遇到打不开的面板，直接重拉
- 驻留进程的启停诊断：状态看 `.zdev/dashboard.json`，日志看 `.zdev/dashboard.log`
