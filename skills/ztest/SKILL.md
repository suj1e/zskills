---
name: ztest
icon: "🧪"
description: "Use when the user wants a test strategy for a feature, bug fix, or any code change — reads the existing proposal/design, identifies what needs testing, and produces a test plan appended to the openspec change documents. Triggers on '怎么测', '测试方案', '覆盖率', 'test plan', '怎么保证质量'. For executing the actual tests use craftsman."
---

# ztest

测试策略设计 skill:**读方案 → 出测试计划 → 分层策略 → 覆盖率目标 → 追加到 openspec change 文档**。

定位对称:`zarchitect` 出技术方案,`ztest` 出验证方案。两者互补——方案决定"做什么",测试策略决定"怎么证明做对了"。

## 何时触发
- 用户说"怎么测"、"测试方案"、"覆盖率"、"test plan"、"怎么保证质量"
- zarchitect 出方案后自动触发(出测试计划)
- zapply 开 change 后自动触发(为每个 change 补测试策略)
- Bug 修复、性能优化、增量需求等任何需要写代码的场景

## 工作流

### 1. 读方案
读取目标 change 目录下的现有文档:
- `proposal.md` — 理解需求和目标
- `design.md` — 理解技术方案和模块划分
- `tasks.md` — 理解实施任务拆解

没有现成方案时:
- 用 `Explore` 扫描代码库理解现有架构
- 读取相关模块的代码和已有测试
- 必要时找用户确认需求边界

### 2. 分析测试边界
- **产品漏洞检查**:逻辑闭环、边界条件、异常流、用户场景覆盖
- **需求拆解**:按模块/层次拆解,识别依赖关系和优先级
- **现有代码对照**:兼容性、影响面、技术债
- **性能考量**(如适用):瓶颈在哪、优化空间、trade-off
- **设计模式建议**(如适用):适用场景、模式选型、侵入程度

输出:`需求/问题清单 + 拆解结构 + 关键风险`

### 3. 追加测试策略到 design.md
在 `design.md` 末尾追加 `## 测试策略` 章节:

```markdown
## 测试策略

### 分层策略
- 单元测试:<哪些模块/函数,覆盖什么场景>
- 集成测试:<哪些接口/数据流,覆盖什么场景>
- E2E 测试:<哪些用户旅程,覆盖什么场景>

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

### 5. 画图（图文并茂，必须）
使用 `diagram-design` 技能生成测试相关图表:
- **测试金字塔**:展示单/集/E2E 比例
- **数据流图**:展示测试数据如何流入/流出
- **架构图**(如适用):展示测试环境和生产环境的隔离

图产出到该 change 目录下的 `diagrams/`,并在 `design.md` 测试策略章节中引用相对路径。

### 6. 交付
输出:修改后的 `design.md`(含测试策略) + 修改后的 `tasks.md`(含测试验收标准) + 图示

## 约束
1. 只出测试策略,不写测试代码——代码由 craftsman 按 TDD 执行
2. 测试策略追加到 `design.md` 末尾,测试验收标准追加到 `tasks.md` 每个 task 后面——不创建自定义文件
3. 测试用例必须覆盖边界条件、异常流、并发场景——不能只测 happy path
4. 覆盖率目标必须量化,不能写"尽量覆盖"——核心模块必须有明确百分比
5. 测试金字塔必须可视化——没有图视为不完整
6. 测试策略是方案的必要组成部分,不是可选项——zarchitect 出方案后必须补齐
