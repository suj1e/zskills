---
name: zpush
icon: "🚦"
description: "Use whenever anything is about to be git-pushed — user says 'push', '推送', '提交上线', or a delivery skill (zarchitect / zdocs / zapply) is about to push. Runs the pre-push safety net: pending 🔧[人工] manual actions, dirty worktree, branch sanity, force-push confirmation. Pure gatekeeper: no merge, no archive, no code changes."
---

# zpush

推送规范 skill:**推送前的唯一安全网**。任何 push——交付 skill 的收尾推送、用户随口一句"push 一下"——都先过这里。它让"推之前查什么"全库只住一个地方。

## 安全网扫描(按序)

1. **🔧[人工] 未执行项(最高优先)**
   - 扫描源:本会话归档 change 的 `tasks.md` + 各战线 impl-report 的「待人工执行清单」(至少含最近终态 run)
   - 收集未勾选的 `- [ ] 🔧[人工]` 行,逐条列出(动作 / 目标环境),问用户:
     - (a) 已执行,推送
     - (b) 先去执行,稍后再推
     - (c) 照推——自担风险,**必须写入对应 impl-report/变更记录,不静默**
2. **merge/归档一致性(收尾完整性)**
   - 遍历本地分支,分支名 = change 名(zapply 约定),排除基线与 archive/ 已有目录:
     - `git log <base>..<branch>` 非空 且 `openspec/changes/<branch>/` 存在 → **已核实未合并**:问用户 (a) merge 后推 (b) 跳过该分支照推+留痕
     - 分支已全并入但 `openspec/changes/<dir>/` 仍在 → **已合并未归档**:问 (a) 先 `openspec archive` 再推 (b) 照推+留痕
   - 用户说明"故意保留分支 / 暂不归档" → 留痕跳过,本会话不再重复追问
3. **工作区卫生**:`git status --porcelain` 有游离未提交文件 → 列出问用户(一并提交推送 / 先留着)
4. **分支 sanity**:确认推送分支 = 预期基线;feature 分支要当基线推、或基线名字对不上 → 拦下确认
5. **force push**:任何 `-f` 一律要求用户显式复述目标后确认,不给默认

## 决策协议

有拦截项 → 只给三选一:**已处理照推 / 先处理后推 / 强行推+留痕**;无拦截项 → 放行,一句话报「安全网通过」。禁止为凑数加检查拖慢正常推送。

## 边界

- 不做 merge / archive / 开 change(归 zapply);不协调测试(ztest 的事)
- 不改代码、不产文档——自身唯一的 git 写操作 = 用户确认后的 `git push`
- 各交付 skill(zarchitect / zdocs / zapply)推送前引用本安全网,推送动作仍由它们自己的交付流程收尾
