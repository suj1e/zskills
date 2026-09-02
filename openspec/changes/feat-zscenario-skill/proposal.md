# feat-zscenario-skill

## Why
现有家族覆盖了策略（ztest：怎么测）、静态存在性（zverify：做了没）、TDD 内环执行（craftsman），但缺**动态执行**——给定逻辑场景真跑系统并出黑盒报告。"测试时没有场景测试报告、指定逻辑场景看不到报告"即此空缺。

## What Changes
- 新增 `skills/zscenario/`：场景测试执行 + HTML 报告
  - 输入：口述逻辑场景 / 文档场景章节 / change 验收标准
  - 用例集：主路径+边界+异常，标注执行手段与环境
  - 执行：测试套件筛选 / API 黑盒调用 / playwright UI 驱动（截图）/ 移动模拟器
  - 报告：`.zdev/scenario/<date>-<场景>.html` 自包含单文件（内联 CSS，截图 base64 内嵌，有品牌源套语义色）
  - 边界：仅 dev/test 环境、不改源码、🔧[人工] 列清单不代做、不 commit
- 配套：test-zs SKILLS、README、AGENTS.md 落盘契约、版本 0.8.0 → 0.9.0

## 验收标准
- just test 全绿（SKILLS 含 zscenario、无面板/npx 耦合）
- openspec validate 通过；版本双文件对齐 0.9.0
