# zskills

个人 ZCode skill 集合。

每个 skill 放在 `skills/<name>/SKILL.md`,被 ZCode 自动发现和调度。

> 走"宁缺毋滥"原则:只放真正会用的、能减轻重复劳动的 skill。不预防性铺设一堆编排剧本。

## 已有

_(暂无。有真正想用的 skill 再往 `skills/` 里加。)_

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
