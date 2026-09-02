# zskills

个人 ZCode **skill 集合**——工作流编排层。

> 三仓分工:[zagents](https://github.com/suj1e/zagents) 放子智能体(执行者),本仓放 skills(编排),[zdashboard](https://github.com/suj1e/zdashboard) 是可视化面板(独立项目)。skill 不启动任何服务、不写展示逻辑——产物落盘约定目录,由面板按约读取。

## 约定速览

| 事物 | 位置 |
|------|------|
| 可视化产物根 | `.zdev/<域>/`(apply、design…) |
| 挂 change 的图 | `openspec/changes/<slug>/diagrams/` |
| 独立文档 / 其配图 | `docs/` · `docs/diagrams/` |
| 设计资产 | `.zdev/design/`(含 `brands/` 品牌源归档) |
| batch run | `.zdev/apply/<runId>/{brief,state.json,report}`——report 出现即结案,零子目录零搬家 |

交付纪律统一为「写入 + commit + push」。

## Skills(10)

| Skill | 一句话 |
|-------|--------|
| ⚙️ [zapply](skills/zapply/SKILL.md) | 已有 change 的执行与验收闭环(craftsman TDD + 三门禁 + 智能 merge + 归档);多 change 走 batch 子模式(run 隔离 / 三维排序 / plan+report 落盘) |
| 🏗️ [zarchitect](skills/zarchitect/SKILL.md) | 方案设计全流程:四路输入 → 需求澄清硬门槛 → 头脑风暴对齐 → 开 change + 图 + ztest → commit+push;Bug 深查委派 doctor |
| 📊 [zdash](skills/zdash/SKILL.md) | 面板纯启动器(全库唯一知道 zdashboard 怎么拉的地方) |
| 🧪 [ztest](skills/ztest/SKILL.md) | 测试策略:分层 + 量化覆盖率 + 逐任务验收标准 + 金字塔/场景覆盖双图 |
| 🎨 [zdesign](skills/zdesign/SKILL.md) | 品牌 UI/图表产出:.zdev/design/ 输出根,getdesign 选风格,brands/ 归档复用 |
| 📝 [zdocs](skills/zdocs/SKILL.md) | 文档编排:五要素派发 docswriter 执笔,自己不动笔 |
| 🚦 [zpush](skills/zpush/SKILL.md) | 推送安全网:人工动作扫描 + 工作区卫生 + 分支 sanity + force 确认;全库唯一管"推之前查什么"的地方 |
| 🔎 [zverify](skills/zverify/SKILL.md) | 功能点↔代码实现一致性核查:文档/口述双源,只读代理并行取证,四态裁定会话内汇报(默认零落盘) |
| 🎬 [zscenario](skills/zscenario/SKILL.md) | 场景测试执行:逻辑场景→用例集→真实执行(套件/API/UI/模拟器),自包含 HTML 报告落 `.zdev/scenario/` |
| 🔍 *(已并入)* | Bug 排查能力归 zarchitect(Path D)+ doctor 子智能体 |

## Agents 配套(zagents)

craftsman(编码执行)· doctor(根因+蓝图)· docswriter(执笔)· zapply-reviewer(分层审查)· glean(检索)

## 更新

marketplace 版本随改动提升;客户端更新/重装 zskills 插件后生效(旧缓存不会自动同步)。

MIT License.
