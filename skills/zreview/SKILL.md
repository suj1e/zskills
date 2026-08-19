---
name: zreview
icon: "✅"
description: "Use when the user wants to write/align product or technical docs - new product briefs, PRDs, design docs - through a review workflow. Acts as AI reviewer: drafts the doc if absent, generates sharp review questions by framework (goals/users/metrics/risks...), then launches zdashboard for item-by-item alignment (answer/accept/dismiss) until the doc passes. Use when aligning on requirements or decisions before implementation."
---

# zreview

文档对齐 skill:**起草(可选)-> AI 评审官提对齐项 -> zdashboard 逐项对齐 -> 通过**。

定位对称:`zdesign` 出设计、`zview` 看项目,zreview 管"写文档并对齐"。

## 工作流

### 1. 收文档
- 用户已有文档 -> 用它(确认放评审目录,默认 `.zreview/`)
- 没有 -> **访谈式起草**:问目标/用户/成功标准/范围,按模板成文(brief.md / prd.md),存 `.zreview/`

### 2. 生成评审项(AI 评审官)
通读文档,按框架生成尖锐问题写 `review.yaml`(status: reviewing):

- **默认框架(8 类)**:目标 / 用户 / 问题定义 / 方案 / 指标 / 边界 / 风险 / 竞品
- **技术文档可换**:目标 / 取舍 / 接口 / 兼容 / 风险 / 回滚

要求:
- 每项 3-8 个问题,直击含糊处(数字无来源、边界未定义、指标不可度量)
- severity:high(阻断级含糊)/ medium / low
- 每项带 `doc` 字段挂到对应文档;id 用 q1/q2… 递增

### 3. 拉起评审台
```bash
npx zdashboard@latest --mode review --dir .zreview --open
```
默认端口 4200。给用户 URL。

### 4. 引导对齐
- 左栏切文档、按状态筛;右侧卡片逐项【答复/采纳/驳回】,全部处理完点顶栏【通过评审】
- 写操作实时落盘 review.yaml;关掉 dashboard 进度不丢

### 5. 出口建议
- 产品类通过后 -> 建议 `/zdesign` 出原型
- 技术类通过后 -> 建议入 openspec(`openspec archive`)归档,后续 `/zview` 查看

## 边界
- 单人 + AI 评审官场景;多人协作(署名/同步)不在范围
- 只写 `.zreview/` 目录;不改项目其他文件
- 评审数据是本地 yaml,无数据库
