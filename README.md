# zskills

个人 ZCode skill 集合。

每个 skill 放在 `skills/<name>/SKILL.md`,被 ZCode 自动发现和调度。

> 走"宁缺毋滥"原则:只放真正会用的、能减轻重复劳动的 skill。不预防性铺设一堆编排剧本。

## 已有

- **zdesign** — 视觉/界面设计 skill。选一套设计系统(消费 [awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) 的 68 个 `DESIGN.md`),产出严格遵循它的 HTML/CSS,自带实时预览(node watch + SSE)和三层质量门禁(约束/细节/验收)。不依赖 OpenDesign。
- **zview** — 项目洞察 skill。探测项目结构(openspec/docs/justfile/.zgoal),拉起 zdashboard 看方案文档、服务实时日志、禅道 bug 列表(只读)。
- **zreview** — 文档对齐 skill。起草(可选)→ AI 评审官按框架提尖锐问题 → zdashboard 逐项对齐 → 通过。
- **zgoal** — bug 修复闭环 skill。禅道看 bug(只读)→ openspec 开修复目标 → 分支实施 → tasks 勾进度 → 开 PR。
- **zapply** — OpenSpec 执行闭环 skill。需求(或已有 change)→ 主智能体开 change → 下发 craftsman 实施 → openspec validate 核实 → archive 归档。不碰禅道、不开 PR,止于 archive。

## 怎么用

作为本地插件添加(开发用):

```
/plugin add /path/to/zskills
```

或从 git 安装:在 ZCode 的 Discover 标签 `+` 里加 `https://github.com/suj1e/zskills.git`。

## 怎么加新 skill

```
skills/
└── <skill-name>/
    └── SKILL.md
```

SKILL.md 格式:

```markdown
---
name: skill-name
description: Use when ...(何时触发,只写何时用不写做什么)
---

# skill-name

正文...
```

`description` 是关键——它决定 ZCode 在什么场景调度这个 skill。要写清"何时该用"。

## License

MIT
