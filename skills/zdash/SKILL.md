---
name: zdash
icon: "📊"
description: "Use when the user wants to open, start, or restart the local visualization panel for this project — 拉起 zdashboard 面板查看各 skill 的产物（执行进度 / 批量驾驶舱 / 设计预览 / 文档视图）。Pure launcher. Triggers on '打开面板', '启动面板', '拉起dashboard', '看板', '重启面板', '开个面板看看'. Does not read or write any business data."
---

# zdash

面板启动器：唯一职责是在当前项目根**拉起或复用 zdashboard**，把 URL 给用户。不理解任何业务语义，不读写任何数据。

## 约定背景

所有 skill 的可视化产物统一写入 `<项目根>/.zdev/` 下的各自子目录（`apply/`、`design/` 等），由 zdashboard 内置插件按固定路径读取展示。本 skill 对内容不做任何判断。

## 启动

```bash
npx zdashboard@latest --dir <项目根> --open
```

1. 直接执行上述命令即可：
   - 同目录已有活实例 → 自动复用并打开（**exit 0，非失败**，勿当异常重试）
   - 实例已死或无记录 → 自动起新实例
2. 把输出的 URL 给用户；需要直达某页可在 URL 后加 `#<mode>`（如 `#apply-batch`、`#review`、`#bugs`、`#design`）
3. 升级 zdashboard 后必须加 `--restart` 强制重开（旧进程会驻留旧版本代码）
4. 多项目并行用 `--dir` 区分根目录；端口被占自动 +1，无需干预

## 边界

- 不写任何数据、不改任何配置（凭据类配置如 `.zdev/config.yaml` 由各业务 skill 自管）
- 不判断哪个面板「有没有东西」——空面板让用户自行切换侧边栏
- 止步于打开浏览器；页内交互归对应业务 skill
