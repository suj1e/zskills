---
name: ztest
icon: "🧪"
description: "Use when a test strategy is needed — auto-invoked by zarchitect right after opening changes, routed back by zapply when its pre-execution check finds a missing strategy section, or fired directly by the user. Reads proposal/design/tasks and appends the test plan into the change documents (layered strategy, quantified coverage targets, per-task acceptance criteria). Triggers on '怎么测', '测试方案', '覆盖率', 'test plan', '怎么保证质量', '补测试策略'. For executing the actual tests use craftsman."
---

# ztest

测试策略设计 skill:**读方案 → 分析测试边界 → 设计策略 + 场景 → 追加进 change 文档 → 金字塔图 + 场景覆盖图 → 交付**。

定位对称:`zarchitect` 出技术方案,`ztest` 出验证方案。两者互补——方案决定"做什么",测试策略决定"怎么证明做对了"。

## 何时触发
- **zarchitect 自动调用**:第 8 步,change 开好后逐个补测试计划
- **zapply 路由**:执行前校验发现缺「测试策略」→ 拦截并引导到这里补齐
- **用户主动发起**:"怎么测"、"测试方案"、"覆盖率"、"test plan"、"怎么保证质量"、"补测试策略"
- Bug 修复、性能优化、增量需求等任何需要写代码的场景

## 工作流

### 1. 读方案
读取目标 change 目录下的现有文档:
- `proposal.md` — 理解需求和目标
- `design.md` — 理解技术方案和模块划分
- `tasks.md` — 理解实施任务拆解

**没有对应 change 时**:只做会话内口头建议,**不写任何文件**(落盘必须挂靠 change);用户要正式产出 → 引导先走 `zarchitect` 出方案开 change,再回来补测试策略

### 2. 分析测试边界(测试视角,非方案视角)
- **可测性分析**:依赖注入点/seam 是否存在、外部依赖如何 mock、测试环境与数据可达性
- **风险驱动重点**:本次变更影响面、复杂度热点、历史易错区
- **场景清单初稿**:边界值 / 异常流 / 并发竞态 / 权限与数据隔离
- **现有测试资产盘点**:已有测试、fixture、工厂、基建,标明可复用项与缺口

输出:`测试重点 + 场景清单 + 资产缺口`

### 3. 追加测试策略到 design.md
在 `design.md` 末尾追加 `## 测试策略` 章节:

```markdown
## 测试策略

### 分层策略
- 单元测试:<哪些模块/函数,覆盖什么场景>
- 集成测试:<哪些接口/数据流,覆盖什么场景>
- E2E 测试:<哪些用户旅程,覆盖什么场景>
- 回归范围:<哪些既有测试/相邻功能会受影响,需要一并回归>

### 覆盖率目标
- 核心模块:<具体百分比 + 必须覆盖的场景>
- 非核心模块:<具体百分比 + 必须覆盖的场景>

### 测试数据方案
- fixture / mock / 真实数据 / 工厂模式
- 测试环境要求和隔离策略

### 边界/异常/并发场景
<清单,不能只测 happy path>

### 性能测试(如适用)
<压测场景 + 阈值 + 工具>
```

### 4. 追加测试验收标准到 tasks.md
在 `tasks.md` 的每个 task 后面追加测试验收标准:

```markdown
- [ ] <task 描述>
  - 测试:<这个 task 怎么验证,具体到断言/场景>
  - 验收标准:<通过/失败的标准>
```

示例:
```markdown
- [ ] 实现用户登录接口
  - 测试:写单元测试覆盖成功/失败/边界(token 过期/无效密码)
  - 验收标准:单元测试通过 + 集成测试通过 + 覆盖率 >= 90%
```

### 5. 图文并茂(必须——让用户看明白"要怎么验")
使用 `diagram-design` 技能生成两张:
- **测试金字塔**:单/集/E2E 的数量与占比
- **场景覆盖图**:核心用户旅程或关键业务场景 → 映射到测试层与验证点(含边界/异常),让用户一眼看清"每个场景由哪张网兜着"

图产出到该 change 目录下的 `diagrams/`,并在 `design.md` 测试策略章节中引用相对路径。

### 6. 交付
输出:修改后的 `design.md`(含测试策略) + 修改后的 `tasks.md`(含测试验收标准) + 图示

## 约束
1. 只出测试策略,不写测试代码——代码由 craftsman 按 TDD 执行
2. 测试策略追加到 `design.md` 末尾,测试验收标准追加到 `tasks.md` 每个 task 后面——不创建自定义文件
3. 测试用例必须覆盖边界条件、异常流、并发场景——不能只测 happy path
4. 覆盖率目标必须量化,不能写"尽量覆盖"——核心模块必须有明确百分比
5. 测试金字塔与场景覆盖图必须可视化——缺图视为不完整
6. 测试策略是方案的必要组成部分,不是可选项——zarchitect 出方案后必须补齐
