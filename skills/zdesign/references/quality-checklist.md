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
