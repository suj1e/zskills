# zgoal — 禅道 bug 修复闭环 skill 设计文档

- 日期:2026-08-18
- 状态:已确认(4 项决策经用户拍板)
- 涉及仓库:`suj1e/zskills`(skill 本体)、`suj1e/zdashboard`(bug 列表视图)

## 背景与动机

家族已有 zdesign(出设计)/ zview(看项目)/ zreview(对齐文档),缺"把一个 bug 修到开 PR"的闭环。用户典型流:查禅道 bug → 开 openspec 修复方案 → 执行更新进度 → 开 PR。

## 已确认决策

| # | 决策 | 选择 |
|---|---|---|
| D1 | 禅道回写 | **纯只读**:绝不调任何写接口(创建/解决/关闭/评论都不做),进度唯一真相在 openspec tasks.md |
| D2 | 凭据 | **项目本地配置文件** `.zgoal/config.yaml`(gitignore + chmod 600) |
| D3 | dashboard | **不造新的**:bug 列表 + openspec 进度都走 zdashboard(4190) |
| D4 | 命名/范围 | **zgoal**;MVP:**bug 即目标**(非 bug 目标源将来再扩展) |

## 设计

### zgoal 工作流(6 步)

1. **配**(一次性):查 `.zgoal/config.yaml`,没有则引导创建(url/account/password 或 token/product)并提醒 gitignore。
2. **看 bug(只读)**:按 `references/zentao-api.md` 取 token → `GET /products/{id}/bugs` → 会话内紧凑表(ID/标题/严重度/状态/指派);用户挑一个或直接给 ID。
3. **开目标**:拉 bug 详情 → openspec change `openspec/changes/fix-<bugID>-<slug>/`:proposal.md(bug 复述 + 禅道链接 + 根因)、design.md(方案+取舍)、tasks.md(checkbox 清单)。
4. **执行**:分支 `fix/<bugID>-<slug>` → 实施 → **每完成一个 task 即勾 tasks.md** → 常规测试/lint。
5. **看进度**:`npx zdashboard@latest --mode view --dir <项目根> --open`——openspec 进度 + bug 列表一站看(需 zdashboard ≥ 1.0.0)。
6. **开 PR**:`gh pr create`,body 含 bug 链接、change 路径、tasks 完成度;合并后提示手动关禅道 bug + `openspec archive`。

### ZenTao API(v1,官方文档核实)

- 认证:`POST {url}/api.php/v1/tokens` body `{"account","password"}` → `{"token"}`;后续请求 Header `Token: <token>`。
- 列表:`GET {url}/api.php/v1/products/{productID}/bugs?page=1&limit=100` → `{page,total,limit,bugs[]}`。
- 详情:`GET {url}/api.php/v1/bugs/{id}`(404 时用 web 详情页兜底)。
- 状态语义:`active` / `resolved` / `closed`;severity 1-4(1 最严重)。
- 前提:禅道开启 RESTful API v1;`{"error":"not found"}` = 路径拼错或未开启。

### 配置文件格式(`.zgoal/config.yaml`)

```yaml
url: https://zentao.example.com
account: me
password: "***"      # 或 token: "***"(免登录)
product: 3           # bug 列表按产品拉(MVP 必填)
```

### zview 扩展(zskills 侧)

SKILL.md 探测清单加第 4 项:`.zgoal/config.yaml` 存在 → 禅道 bug 列表能力(只读);引导使用加「Bugs」视图说明;边界注明 bug 修复动作用 zgoal。

### zdashboard 扩展(0.1.7 → 1.0.0)

- `detect.ts`:加 `hasBugs = exists(.zgoal/config.yaml)`,随 `/__files` 下发。
- 新 `src/server/bugs.ts`:读配置(扁平 yaml 极简解析)→ 取 token(内存缓存)→ 拉产品 bugs(限 100 条,8s 超时);**只代理 GET,绝不转发写方法**。
- `index.ts`:加 `GET /__bugs` 路由(JSON:bugs/total/error);启动日志加 bugs 探测位。
- 前端:FileTree 顶部「Bugs」入口(lucide Bug 图标,只在 hasBugs 时显示,样式对齐「服务日志」);新 `viewers/BugViewer.tsx`:状态筛选(全部/active/resolved/closed)+ 表格(#ID/标题/严重度 S1-S4 徽标/状态徽标/指派),行内 window.open 跳禅道详情(`{url}/bug-view-{id}.html`)。
- 测试:`test-server/scripts/mock-zentao.js`(tokens + bugs 两端点)+ `test-server/.zgoal/config.yaml` fixture;验证 build、接口、浏览器渲染。

### 调度边界

"看禅道 bug 并驱动修复开 PR" → zgoal;"看方案/日志/bug 列表(只读)" → zview;"写文档对齐" → zreview;"出设计" → zdesign。

## 错误处理

| 情况 | 处理 |
|---|---|
| token 401/失败 | 检查凭据;提示禅道是否开启 RESTful API v1 |
| `error: not found` | 路径拼错或 API 未开启,对照 api.md |
| 无 openspec | 先 `openspec init` 再开 change |
| gh 未登录 | 提示 `gh auth login` |
| dashboard 版本 < 0.2.0 | zgoal 第 5 步降级为仅会话内表格,不阻塞 |

## 非目标

- 不做禅道任何写操作(自动解决/关闭/评论)
- 不做非 bug 目标源、多禅道实例、bug 批量看板
- 不做 openspec 之外的进度存储

## 验证

- zskills:引用路径完整 + 工作流干跑走查
- zdashboard:build 通过;mock 禅道 + test-server 起服,`/__files` 带 hasBugs、`/__bugs` 返回 3 条假数据;浏览器截图确认 Bugs 入口与表格渲染
