# zdraw · 验收速查

> 交付前逐项自检。**任一未过 → 回炉,不交付。**

## 结构与预算

- [ ] 结构先行:节点/边清单先于视觉;> 6 节点时清单经用户确认
- [ ] 复杂度预算内(≤9 节点、≤12 边);超出已拆 overview + detail
- [ ] 坐标来自 layout 脚本(coords.json),无手估

## 布局(按 layout-rules.md 自检)

- [ ] 跨轴连线全部正交圆角(r=8),无对角斜线
- [ ] 箭头标签有遮罩 + 与连线留 6–10px 可见间隙,不压线、不与节点重叠
- [ ] 同边多连线附着点 ≥12px 扇形展开;无重叠连线,交叉用桥
- [ ] 连线不穿无关节点(过境例外必须虚线 + 标签在可见端)
- [ ] 坐标/字号/间距 4px 网格(末位 1/2/3/5/6/7/9 → 改)
- [ ] 图例是底部水平条带;箭头先画节点后画(z-order 线压盒下)

## 双交付铁律

- [ ] 可编辑源文件在(.excalidraw 或 .drawio,按场景路由)
- [ ] 渲染 .svg 在;浏览器打开亲眼确认(连线/标签/间距与预期一致)
- [ ] .excalidraw 元数据字段全套(seed/version/versionNonce/isDeleted/opacity),编辑器能打开
- [ ] .drawio 被 draw.io 正常解析(节点可拖动、边保持吸附)

## 品牌化(有品牌诉求时追加)

- [ ] 颜色/字体全部来自 `.zdev/design/diagram-style.md` 语义角色,无硬编码散色
- [ ] accent 元素总数 ≤2(焦点节点/主箭头合计),普通节点一律 ink/muted/soft
- [ ] 标题品牌 display;节点名品牌 sans;技术子标签 mono(缺失退化已在 diagram-style.md 披露)
- [ ] diagram-style.md 落盘 .zdev/design/ 且 source-design 标注

## 尺寸与交付

- [ ] 尺寸预设对位场景(doc-inline / slide-16x9…);字号阶梯随尺寸缩放(slide 节点名 16px)
- [ ] .svg 有 `role="img"` + prefixed `title`/`desc`(title 是 svg 第一个子元素)
- [ ] 交付报告含:文件清单表(源文件+svg 各自用途)、类型/场景/尺寸、品牌来源(有则报 diagram-style.md 路径)
