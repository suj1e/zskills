# AGENTS.md — zskills

个人 ZCode **skill 集合**（工作流编排层）。子智能体放姊妹仓 [zagents](https://github.com/suj1e/zagents)，可视化面板是独立仓 [zdashboard](https://github.com/suj1e/zdashboard)。三仓分工：**zskills 编排、zagents 执行、zdashboard 展示**——本仓不启动任何服务、不写展示逻辑。

## 结构

```
skills/<name>/SKILL.md     # 每个 skill 一个目录；references/ 放配套模板
openspec/                  # 变更管理（changes/ + archive/），openspec CLI
test-zs                    # 静态冒烟测试（bash，无运行时依赖）
justfile                   # just test → bash test-zs
.zcode-plugin/plugin.json  # 插件版本（与 marketplace.json 保持一致）
marketplace.json           # 市场清单
```

现有 12 个 skill：zapply（执行+验收，含 batch 子模式）/ zarchitect（方案设计）/ zverify（实现核实）/ zscenario（场景测试执行） / zdash（面板启动器）/ ztest / zdraw（图表，.excalidraw/.drawio 双源交付）/ zshow（会话内可视化讲解）/ zdesign / zdocs / zpush（推送安全网）/ zasset。

## 常用命令

```bash
just test                                        # 冒烟测试（当前 113 项，必须全绿）
openspec validate <change> --type change         # 校验 change
openspec archive <change> --yes                  # 归档
```

新增/改名 skill 后必须同步：`test-zs` 的 `SKILLS=(...)` 数组、README 的 Skills 表、`.zcode-plugin/plugin.json` 与 `marketplace.json` 两处版本号、以及 `openspec new change` 记录变更。插件版本 bump 后需客户端重装才生效（旧缓存不会自动同步）。

## 硬规则（违者等于破坏架构）

1. **面板零耦合**：全库只允许 `zdash` 提及 zdashboard / 写启动命令。其余 skill 一律不启动服务、不写展示逻辑——产物落盘约定目录，面板按约读取。
2. **产物落盘契约**：可视化产物 → `.zdev/<域>/`（apply）；原型 → `prototypes/`；挂在 change 的图 → `openspec/changes/<slug>/diagrams/`；独立文档 → `docs/`、配图 `docs/diagrams/`；设计源与资产 → `design/`（`brands/` 品牌源归档、`assets/` 图形资产）；场景测试报告 → `.zdev/scenario/<date>-<场景>.html`（自包含单文件，不 commit）。前三者随仓库 commit + push。
3. **交付纪律**：所有 skill 的完成态 =「写入 + commit + push」，直接提交 main。
4. **batch run 结构**（`.zdev/apply/<runId>/`）：只有 `brief.md` / `state.json` / `report.md` 三件，**禁止子目录、禁止搬家、禁止第二账本**（todo/summary 类派生文件一律不建）。`report.md` 出现即结案；活动战线 = 无 report 的 run；同一 change 任何时刻至多被一个战线占用；全局 craftsman 并发预算 ≤ 4。
5. **🔧[人工] 标记**：tasks.md 中该前缀条目 = 用户亲自执行（SQL/外部配置/人眼验证），craftsman 跳过永不勾选；push 前由 zpush 安全网扫描确认。
6. **镜像维护**：15 维审查清单在 `skills/zapply/references/code-reviewer-prompt.md` 与 zagents `agents/zapply-reviewer.md` **双向同步**；craftsman 执行原则同理（TDD、DESIGN.md 强制）。改任一侧必须同步另一侧。
7. **通知义务**：skill 在语义时刻（结案/冲突停/parked/**待人工项**）必须触发通知——调用规范路径 `~/.zdev/bin/notify.sh <event> "<title>" "<body>"`（event 用 `done` / `needs-you`；**存在 🔧[人工] 待办时一律 `needs-you`**,全清才是 `done`）。**异步不阻塞交付**：脚本后台发送、失败自动进死信补投，调用方不等待不重试。通知配置机器级收敛在 `~/.zdev/config.yaml` 的 `notify` 节，换 webhook 平台只改 config；**skill 文本与任何 git 仓里不得出现 webhook URL/secret**。脚本未部署时从本仓 `scripts/notify.sh` 复制过去。

## 通知配置（~/.zdev/config.yaml，机器级，不进任何 git 仓）

```yaml
notify:
  default: bark            # 主通道;写数组即 fan-out 多通道
  level: timeSensitive     # 透传给通道(仅 bark 消费)
  # group: zskills         # 缺省取项目目录名
  channels:
    bark:
      type: bark           # URL 拼参
      url: https://api.day.app/<key>
    feishu:
      type: feishu         # bot webhook,JSON {"msg_type":"text",...}
      url: https://open.feishu.cn/open-apis/bot/v2/hook/<token>
    dingtalk:
      type: dingtalk       # {"msgtype":"text",...}
      url: https://oapi.dingtalk.com/robot/send?access_token=<token>
    generic:               # 未知类型兜底:POST JSON {event,title,body,group,level}
      type: generic
      url: https://example.com/hook
```

常用：`notify.sh test`（链路自测）/ `notify.sh retry`（手动补投死信）。死信账本 `~/.zdev/notify/dead.jsonl`（上限 50 条）。

## 写 SKILL 的约定

- frontmatter：`name` / `icon` / `description`——**description 是触发面**，中英触发词都要写；正文中文。
- 结构：定位一句话 → 何时触发 → 工作流（编号步骤）→ 边界 → 资产清单。产物路径必须符合上面的落盘契约。
- 禁止在 SKILL 中发明伪 CLI 语法（如 `zapply batch --flag`）——用"意图路由表"表达会话语义。
- 结构性规则一旦在讨论中定稿，写成显式条款钉进 SKILL，不留口头约定。

## 已知坑

- Windows + Git Bash：add/commit 时的 `LF will be replaced by CRLF` 警告是良性的，忽略。
- `openspec new change` 名称只允许小写字母/数字/连字符；纯流程类 change 在 `.openspec.yaml` 加 `skip_specs: true` 才能 validate 通过。
- npx 拉包按 spec 字符串分槽缓存，多版本槽位共存属正常；需要确定版本时"先 `npm view --prefer-online` 解析、再钉具体版本执行"。
