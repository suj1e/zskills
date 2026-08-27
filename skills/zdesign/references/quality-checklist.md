# zdesign 质量速查

SKILL.md 里的【约束】【细节】【验收】的展开版。产出前/交付前对照过一遍。

## 约束(硬规则,违反即回炉)

### token 强制
- [ ] 每个颜色都是 `var(--color-*)`,无硬编码 hex
- [ ] 每个字号都是 `var(--fs-*)` + 对应 line-height/letter-spacing,按 type scale
- [ ] 圆角用 `var(--radius-*)`,间距用 `var(--space-*)`
- [ ] `:root` 变量集与所选 DESIGN.md 一一对应

### 防 AI 感红线
- [ ] 主色不是默认 indigo (#4F46E5) / violet,而是 DESIGN.md 指定的品牌色
- [ ] 没有 emoji 当功能图标(用 SVG / 图标字体)
- [ ] 没有"等权重三栏 feature 卡"这种模板感布局
- [ ] 标题没有 gradient text-fill
- [ ] 字号严格在 type scale 上,没有随机 17px / 23px

### 响应式
- [ ] mobile (≤640) + desktop 两断点都验证
- [ ] 触控目标 ≥ 44×44px
- [ ] 无横向溢出 / 内容被裁切

### a11y 基础
- [ ] 语义标签(header/main/nav/button 等),非 div 满天飞
- [ ] 文字对比度 ≥ AA(正文 4.5:1,大字 3:1)
- [ ] `:focus-visible` 有可见焦点环
- [ ] 图片有 alt,图标按钮有 aria-label

## 细节(打磨清单)

- [ ] 按钮四态:hover / active / focus / disabled
- [ ] 数据四态:空 / 加载 / 错误 / 成功(适用时)
- [ ] 文案真实,无 Lorem / "Button" / "Title"
- [ ] 留白遵循 spacing 阶梯,节奏一致
- [ ] 对齐统一(同一栅格)
- [ ] 过渡用 token motion,克制(150–250ms ease 为主)

## 验收(交付闸门)

- [ ] 约束全部 ✓
- [ ] 细节该有的都有
- [ ] 视觉调性 = 所选 DESIGN.md
- [ ] 需求功能/状态全覆盖
- [ ] 浏览器打开,亲眼看过 mobile + desktop

**任一未过 → 回炉,不交付。**

---

# 图表专项(diagram 产出追加)

UI 产出的约束/细节/验收照常适用;图表另有以下硬项。语义角色映射细则见 `diagram-style-mapping.md`,兜底布局规则见 `diagram-basics.md`。

## 约束(硬规则)

- [ ] 所有图表颜色/字体来自 `<产出根>/diagram-style.md` 语义角色,无硬编码
- [ ] **accent 元素总数 ≤2**(焦点节点/主箭头合计),普通节点一律 ink/muted/soft
- [ ] 标题用品牌 display 字体;节点名用品牌 sans;技术子标签用 mono(品牌无 mono 退化 Geist Mono 且已在 diagram-style.md 披露)
- [ ] 布局语法来自实际拉到的语法源,版本/来源已记录

## 布局(按语法源规则自检)

- [ ] 跨轴连线全部正交圆角(r=8),无对角斜线
- [ ] 箭头标签有不透明遮罩 + 与连线留 6–10px 可见间隙,不压线、不与节点重叠
- [ ] 同边多连线附着点 ≥12px 扇形展开;无重叠/共享连线,交叉用桥
- [ ] 连线不穿无关节点(过境例外必须虚线 + 标签在可见端)
- [ ] 复杂度预算内(≤9 节点、≤12 箭头),超出拆 overview + detail
- [ ] 坐标/字号/间距 4px 网格
- [ ] 图例是底部水平条带,不在图内;箭头先画节点后画

## a11y 与交付

- [ ] SVG 有 `role="img"` + prefixed `title`/`desc`(title 是 svg 第一个子元素)
- [ ] 场景对位:文档配图可导出 PNG/SVG(手动,不问不导);内嵌图随宿主页面自适应;单图符合所选尺寸预设(字号阶梯随尺寸缩放)
- [ ] 浏览器打开,亲眼确认过
- [ ] 交付报告含:diagram-style.md 路径、所选品牌、**所用 diagram-design 版本 + 语法源级别(最新 main / 本地缓存 / 兜底)**

**任一未过 → 回炉,不交付。**
