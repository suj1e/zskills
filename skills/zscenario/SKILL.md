---
name: zscenario
icon: "🎬"
description: "Use when the user wants a logical scenario actually executed and a test report produced — black-box testing by running test suites, API calls, browser UI, or emulators. Triggers on '场景测试', '黑盒测试', '测试报告', '跑一遍这个场景', '验证场景', 'scenario test'. Executes in dev/test environments only; never touches production, never modifies source code."
---

# zscenario

场景测试执行 skill:**接场景 → 设计用例 → 真实执行 → HTML 报告落 `.zdev/scenario/`**。

回答的问题:"这个逻辑场景,系统跑起来到底对不对?"——不是策略(ztest)、不是静态存在性(zverify),是**动态行为验证**。

## 何时触发
- 用户说"场景测试"、"黑盒测试"、"测试报告"、"跑一遍这个场景"、"验证场景"
- 给定一个逻辑场景(下单后取消应退款…),想知道系统实际行为
- change 验收标准写完了,想真跑一遍看结果
- 上线前对关键场景做回归执行

## 工作流

### 1. 接场景
三种来源汇入同一管道:用户口述逻辑场景 / 产品文档场景章节 / change 验收标准。
拆成**步骤清单**:前置条件 + 操作序列 + 每步预期——**复述确认**后再动手。

### 2. 设计用例
每个场景派生用例集:主路径 + 边界 + 异常(并发按需)。每条用例标注:
- **执行手段**:项目测试套件 / API 调用 / Web UI 驱动 / 移动模拟器 / 人工
- **环境**:dev / test(只在开发测试环境执行,不碰生产)

### 3. 执行(按手段真实跑)
- **测试套件**:筛选场景相关用例运行(`vitest -t "<关键词>"` / `pytest -k "<关键词>"`)
- **API 黑盒**:按步骤真实调用接口,断言状态码与响应结构;保留请求/响应全文
- **Web UI**:playwright 驱动浏览器走场景,**每关键步截图**
- **移动端**:android-emulator / ios-simulator 跑场景,读日志 + 截图
- 失败保留现场:响应全文 / 截图 / 相关日志摘录,不许只写"测试失败"

### 4. 生成 HTML 报告
`.zdev/scenario/<yyyy-MM-dd>-<场景名>.html`——**自包含单文件**(内联 CSS,零运行时依赖;项目存在 DESIGN.md 品牌源则套用其语义色,无则干净中性风):

- **场景卡**:前置条件 + 步骤序列 + 环境说明
- **用例矩阵**:通过 / 失败 / 阻塞 / 待人工 一览
- **用例详情**(每条):步骤 → 预期 → 实际 → 判定 → 证据(响应 JSON / **截图 base64 内嵌** / 日志摘录)
- **失败分析**:失败原因 + 复现路径
- **🔧[人工] 待办清单**:无法自动化验证的步骤列给用户

### 5. 交付
报告路径给用户(浏览器打开),会话内给摘要(通过率 + 失败要点)。
失败项修不修、怎么修——走 zapply,由用户点名;`.zdev/scenario/` 不 commit,删留随意。

## 边界
- 只在开发 / 测试环境执行,**不碰生产**
- 不修改业务源码——失败如实报告,修复是 zapply 的事
- 🔧[人工] 步骤列清单不代做
- 与家族分工:ztest 出策略(怎么测)/ zverify 静态存在性(做了没)/ **zscenario 动态行为(跑起来对不对)**/ craftsman 只在 TDD 内环跑测试

## 资产
- 无 references;报告模板与判定规则内联于工作流
