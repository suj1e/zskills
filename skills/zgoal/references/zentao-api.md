# ZenTao OpenAPI v1 速查(zgoal 调用禅道的唯一依据)

官方 RESTful API v1([文档](https://www.zentao.net/book/api/1397.html))。前提:禅道已开启 RESTful API v1 功能。

## 认证

```bash
curl -s -X POST "$ZTAO/api.php/v1/tokens" \
  -H "Content-Type: application/json" \
  -d '{"account":"me","password":"***"}'
# → {"token":"xxxxx"}
```

后续所有请求带 Header:`Token: <token>`。配置里有 `token:` 字段时跳过这步。

## 端点(只读三件套)

| 用途 | 方法 + 路径 | 返回 |
|---|---|---|
| 取 token | `POST /api.php/v1/tokens` | `{token}` |
| 产品列表 | `GET /api.php/v1/products` | `{products:[{id,name,...}]}` |
| bug 列表 | `GET /api.php/v1/products/{productID}/bugs?page=1&limit=100` | `{page,total,limit,bugs:[...]}` |
| bug 详情 | `GET /api.php/v1/bugs/{bugID}` | bug 对象全字段 |

```bash
TOKEN=$(curl -s -X POST "$ZTAO/api.php/v1/tokens" -H "Content-Type: application/json" \
  -d "{\"account\":\"$ACC\",\"password\":\"$PWD\"}" | jq -r .token)

# 列表(紧凑表用)
curl -s "$ZTAO/api.php/v1/products/$PRODUCT/bugs?page=1&limit=100" \
  -H "Token: $TOKEN" | jq -r '.bugs[] | [.id,.title,.severity,.pri,.status,.assignedTo] | @tsv'

# 产品列表(配置时用户不知道 product ID,用这个查)
curl -s "$ZTAO/api.php/v1/products?page=1&limit=100" \
  -H "Token: $TOKEN" | jq -r '.products[] | [.id,.name] | @tsv'

# 详情(开 openspec 前拉)
curl -s "$ZTAO/api.php/v1/bugs/$BUGID" -H "Token: $TOKEN" | jq .
```

## 字段表

| 字段 | 语义 |
|---|---|
| `id` / `title` | 编号 / 标题 |
| `severity` | 1-4,1 最严重 |
| `pri` | 优先级 1-4 |
| `status` | `active`(处理中)/ `resolved`(已解决待验证)/ `closed`(已关闭) |
| `assignedTo` / `openedBy` / `resolvedBy` | 当前指派 / 创建者 / 解决者 |
| `steps` | 重现步骤(HTML) |
| `product` / `module` / `openedBuild` | 归属 |

## 错误对照

| 现象 | 原因与处理 |
|---|---|
| 401 / token 为空 | 凭据错(核对 config.yaml),或账号无 API 权限 |
| `{"error":"not found"}` | 路径拼错或禅道未开启 RESTful API v1(后台开启) |
| 超时 | url 错 / 内网不通;确认 config.yaml 的 url 是禅道根地址(带 `http(s)://`,不带 `/api.php`) |

## 只读红线

本 skill 只允许上表四个只读调用(token / 产品列表 / bug 列表 / bug 详情)。禅道的 bug 创建 / 解决 / 关闭 / 激活 / 确认 / 评论等写接口**一律不调**——修复闭环的信息全部活在 openspec,禅道状态由用户合并 PR 后手动处理。
