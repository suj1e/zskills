#!/usr/bin/env bash
# notify.sh — zskills 通知义务执行器(机器级,规范路径 ~/.zdev/bin/notify.sh)
#
# 语义与通道分离:调用方只喊事件,通道在 ~/.zdev/config.yaml 的 notify 节配置。
# 换 webhook 平台 = 改 config,zapply 等 skill 一个字不动。
#
# 用法:
#   notify.sh <event> <title> <body>     # 发通知(异步,立即返回)
#   notify.sh test                       # 发一条测试通知
#   notify.sh retry                      # 补投死信(前台,带输出)
#
# 设计约定(改前先读 AGENTS.md 通知义务条款):
# - 异步:发送 daemonize 到后台,curl --max-time 10,主流程零阻塞
# - 失败:重试 2 次(退避 2s/5s)→ 死信 ~/.zdev/notify/dead.jsonl(上限 50 条,满了丢最旧)
# - 幂等取舍:补投宁可重复不可漏报(HTTP 响应丢失时可能重复一条,接受)
# - secret 防泄漏:输出 mask URL token;死信只存 channel 名不存 URL
# - 未配置 notify 节 = 静默跳过(零打扰)
set -euo pipefail

ZDEV_DIR="${ZDEV_DIR:-$HOME/.zdev}"
CONFIG_FILE="$ZDEV_DIR/config.yaml"
DEAD_DIR="$ZDEV_DIR/notify"
DEAD_FILE="$DEAD_DIR/dead.jsonl"
DEAD_MAX=50
CURL_MAX_TIME=10

# ---------- yaml 极简读取(只支持两层缩进的 key: value) ----------
# 用法: cfg_get "notify.default" → 输出值或空
cfg_get() {
  local key="$1" leaf
  leaf="${key##*.}"
  awk -v leaf="$leaf" '
    /^[[:space:]]*#/ {next}
    $0 ~ "^[[:space:]]*"leaf":[[:space:]]*" {
      sub("^[[:space:]]*"leaf":[[:space:]]*", "")
      sub(/[[:space:]]+#.*$/, "")
      gsub(/^["'\'']|["'\'']$/, "")
      print
      exit
    }
  ' "$CONFIG_FILE" 2>/dev/null
}

# default 通道列表(单值或 YAML 数组都归一成多行)
cfg_channels() {
  awk '
    /^[[:space:]]*#/ {next}
    /^default:/        {in_def=1; sub(/^default:[[:space:]]*/, ""); if ($0 != "") {print; exit} next}
    in_def && /^[[:space:]]*-[[:space:]]*/ {sub(/^[[:space:]]*-[[:space:]]*/, ""); gsub(/^["'\'']|["'\'']$/, ""); print; next}
    in_def && /^[^[:space:]]/ {exit}
  ' "$CONFIG_FILE" 2>/dev/null
}

mask_url() {
  # 把 URL 中 token 部分打码(key/最后一个路径段或 access_token 参数)
  sed -E 's|(https?://[^/]+/[^/?]+/)[^/?]+|\1***|g; s|access_token=[^&" ]+|access_token=***|g; s|hook/[^" ]+|hook/***|g'
}

json_escape() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | awk '{printf "%s\\n", $0}' | sed -e 's/\\n$//'
}

# ---------- 通道适配器(各平台 payload 拼装,新增平台加一个 case) ----------
# 入参: type url title body group level event;成功输出 nothing,失败 exit 非 0
send_channel() {
  local type="$1" url="$2" title="$3" body="$4" group="$5" level="$6" event="$7"
  local t b g payload
  t=$(json_escape "$title"); b=$(json_escape "$body"); g=$(json_escape "$group")
  case "$type" in
    bark)
      # GET 拼参格式(title/body 走 query,绕开路径段数坑)
      local enc_t enc_b
      enc_t=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$title")
      enc_b=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$body")
      curl -sS --max-time "$CURL_MAX_TIME" \
        "${url}?title=${enc_t}&body=${enc_b}&group=${group}&level=${level}" >/dev/null
      ;;
    feishu)
      payload="{\"msg_type\":\"text\",\"content\":{\"text\":\"$(json_escape "[$group] $title
$body")\"}}"
      curl -sS --max-time "$CURL_MAX_TIME" -H 'Content-Type: application/json' \
        -d "$payload" "$url" >/dev/null
      ;;
    dingtalk)
      payload="{\"msgtype\":\"text\",\"text\":{\"content\":\"$(json_escape "[$group] $title
$body")\"}}"
      curl -sS --max-time "$CURL_MAX_TIME" -H 'Content-Type: application/json' \
        -d "$payload" "$url" >/dev/null
      ;;
    generic|*)
      # 兜底:POST JSON {event,title,body,group,level}——未识别 type 也走这里试一把
      payload="{\"event\":\"$(json_escape "$event")\",\"title\":\"$t\",\"body\":\"$b\",\"group\":\"$g\",\"level\":\"$(json_escape "$level")\"}"
      curl -sS --max-time "$CURL_MAX_TIME" -H 'Content-Type: application/json' \
        -d "$payload" "$url" >/dev/null
      ;;
  esac
}

# 对单个通道:重试 2 次 → 仍败写死信。返回 0=最终成功,1=进死信
deliver() {
  local ch_name="$1" ch_type="$2" ch_url="$3" title="$4" body="$5" group="$6" level="$7" event="$8"
  local attempt=0 delays=(0 2 5)
  for attempt in 0 1 2; do
    sleep "${delays[$attempt]}" || true
    if send_channel "$ch_type" "$ch_url" "$title" "$body" "$group" "$level" 2>/dev/null; then
      return 0
    fi
  done
  # 死信(只存 channel 名,不存 URL)
  mkdir -p "$DEAD_DIR"
  printf '{"time":"%s","event":"%s","channel":"%s","title":"%s","body":"%s"}\n' \
    "$(date +%FT%T)" "$(json_escape "$event")" "$ch_name" "$(json_escape "$title")" "$(json_escape "$body")" \
    >> "$DEAD_FILE"
  return 1
}

# 死信上限:超过 DEAD_MAX 丢最旧
trim_dead() {
  [[ -f "$DEAD_FILE" ]] || return 0
  local n
  n=$(wc -l < "$DEAD_FILE" | tr -d ' ')
  if (( n > DEAD_MAX )); then
    tail -n "$DEAD_MAX" "$DEAD_FILE" > "${DEAD_FILE}.tmp" && mv "${DEAD_FILE}.tmp" "$DEAD_FILE"
  fi
}

# 补投死信(前台;供手动 retry 与 Stop hook 后台包一层)
retry_dead() {
  [[ -f "$DEAD_FILE" ]] || { echo "no dead letters"; return 0; }
  local tmp="${DEAD_FILE}.sending"
  mv "$DEAD_FILE" "$tmp"
  touch "$DEAD_FILE"
  local failed=0 line ch_name event title body
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    ch_name=$(printf '%s' "$line" | sed -nE 's/.*"channel":"([^"]*)".*/\1/p')
    event=$(printf '%s' "$line" | sed -nE 's/.*"event":"([^"]*)".*/\1/p')
    title=$(printf '%s' "$line" | sed -nE 's/.*"title":"([^"]*)".*/\1/p')
    body=$(printf '%s' "$line" | sed -nE 's/.*"body":"([^"]*)".*/\1/p')
    ch_type=$(cfg_get "notify.channels.${ch_name}.type")
    ch_url=$(cfg_get "notify.channels.${ch_name}.url")
    if [[ -n "$ch_type" && -n "$ch_url" ]] && \
       send_channel "$ch_type" "$ch_url" "$title" "$body" "$(group_default)" "$(cfg_get notify.level)" "$event" 2>/dev/null; then
      echo "redelivered: [$ch_name] $title"
    else
      printf '%s\n' "$line" >> "$DEAD_FILE"   # 还不行,收回死信
      failed=$((failed+1))
    fi
  done < "$tmp"
  rm -f "$tmp"
  trim_dead
  (( failed == 0 )) || { echo "$failed dead letter(s) still pending"; return 1; }
  return 0
}

group_default() {
  # group:配置优先,缺省取项目目录名
  local g
  g=$(cfg_get notify.group)
  [[ -n "$g" ]] && { echo "$g"; return; }
  basename "${ZCODE_PROJECT_DIR:-$PWD}"
}

# ---------- 主入口 ----------
event="${1:-}"
title="${2:-}"
body="${3:-}"

case "$event" in
  test)
    title="zskills · notify test"
    body="通知链路自测:看到这条说明 notify.sh → config → 通道全通"
    ;;
  retry)
    retry_dead
    exit $?
    ;;
  ""|-h|--help|help)
    sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
esac
[[ -n "$title" ]] || { echo "usage: notify.sh <event> <title> <body> | test | retry" >&2; exit 1; }

# 未配置 → 静默跳过
[[ -f "$CONFIG_FILE" ]] || exit 0
grep -q '^notify:' "$CONFIG_FILE" 2>/dev/null || exit 0

level=$(cfg_get notify.level); level="${level:-timeSensitive}"
group=$(group_default)

# 补投旧死信(后台,不阻塞本次发送;失败静默留给下次)
( retry_dead >/dev/null 2>&1 || true ) &

# fan-out:default 单值或数组
sent_fail=0
while IFS= read -r ch_name; do
  [[ -z "$ch_name" ]] && continue
  ch_type=$(cfg_get "notify.channels.${ch_name}.type")
  ch_url=$(cfg_get "notify.channels.${ch_name}.url")
  if [[ -z "$ch_type" || -z "$ch_url" ]]; then
    echo "notify: channel '$ch_name' misconfigured (skip)" >&2
    continue
  fi
  # 异步:整个"重试+死信"过程 daemonize,主流程立即返回
  ( deliver "$ch_name" "$ch_type" "$ch_url" "$title" "$body" "$group" "$level" "$event" ) >/dev/null 2>&1 &
done < <(cfg_channels)
disown -a 2>/dev/null || true
exit 0
