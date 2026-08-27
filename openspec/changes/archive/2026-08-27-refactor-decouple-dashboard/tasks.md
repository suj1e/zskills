# Tasks

## 1. 删除三个 skill
- [x] git rm skills/zgoal（含 references/zentao-api.md）
- [x] git rm skills/zreview
- [x] git rm skills/zview

## 2. 数据路径迁移
- [x] git mv .zapply/batch-state.schema.json → skills/zapply/references/
- [x] sed：zapply 系列 .zapply/ → .zdev/apply/

## 3. zapply 收尾
- [x] frontmatter 去 zgoal/zview 指针
- [x] 定位对称句重写（去禅道）
- [x] 删旧版「多 change 并行编排」整节 → 指向 batch
- [x] 边界去「不碰禅道」条目
- [x] 资产清单补 batch-prompt / craftsman-batch-prompt / batch-state.schema

## 4. zdesign 契约化
- [x] 核心理念与首句去 dashboard 化
- [x] 第 1 步启动块替换为 zdash 指针 + 产出根 .zdev/design/
- [x] 删三处断链 assets 引用（starter.html / button.html / diagram-starter.html）
- [x] 资产节仅保留 references/ 三项

## 5. zdoc
- [x] description 去 zview 指针
- [x] 删「如果 zdashboard 已启动」条目
- [x] 图路径改约定；交付视角措辞修正

## 6. 图路径约定落文
- [x] zarchitect step8 → change diagrams/
- [x] zdebug step4 → change diagrams/
- [x] ztest step5 → change diagrams/
- [x] zdoc step5 → change diagrams/ + docs/images 回落

## 7. 校验
- [x] 全库 grep 无残留指针/启动命令（zdash 自身除外）
- [ ] openspec validate 通过
