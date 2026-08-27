# feat-zdash-skill

## Why
各 skill 的 SKILL.md 中散落着 zdashboard 启动命令，且已出现三种不一致的启动习惯（`--dir <项目根>` / `--mode review --dir .zreview` / 含糊描述）。skill 与 dashboard 双向耦合：dashboard 挂了 skill 文档也要改。

## What Changes
- 新建 `skills/zdash/`：纯面板启动器 skill，唯一职责是在项目根拉起/复用 zdashboard 并把 URL 给用户
- zdash 吸收全部散落的启动知识（实例复用 exit 0、`--restart` 升级规则、端口自增、`#<mode>` 深链）
- zdash 不理解任何业务语义、不读写任何数据

## 验收标准
- `skills/zdash/SKILL.md` 存在且 frontmatter 完整（name/icon/description）
- 文档内含复用/重启/深链/多项目四条规则
- 无业务逻辑、无数据写入
