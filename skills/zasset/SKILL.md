---
name: zasset
icon: "🖌️"
description: "Use when the user needs a standalone graphic asset produced — logo, favicon/app icons, icon sets, OG share images, banners/covers, posters, badges, empty-state/error-page illustrations. Triggers on '做个logo', '图标', 'favicon', '分享图', 'banner', '海报', '插画', 'badge'. Vector-first: SVG master files plus size exports, brand tone shared with zdesign's brand sources. For full UI pages/screens use zdesign; for structural diagrams use diagram-design."
---

# zasset

独立图形资产 skill:**定场景 → 定基调 → SVG 探索精修 → 变体导出 → 过三测交付**。

凡是「单个视觉成品」——logo、图标组、favicon、分享图、banner、海报、插画、badge——都归它;页面归 zdesign,结构图归 diagram-design。

## 核心理念

- **矢量优先**:SVG 母版是唯一真相源,PNG/ICO 只是按需导出的产物,禁止位图起稿再描。
- **品牌基调共享**:颜色/字体的调性来自 `.zdev/design/brands/<slug>/DESIGN.md`(与 zdesign 同源共享),保证 logo 和界面一个调性。
- **完善交付**:产物必须过缩放/单色/对比度三测,未全过回炉,绝不交付半成品。
- **统一输出根**:所有产出写入 `.zdev/design/assets/<slug>/`,skill 不询问输出路径。

## 场景矩阵(速览,精确规格见 references)

| 分类 | 产物 | 必出变体 |
|---|---|---|
| 品牌标识 | logo(字标/图形标/组合标)、monogram | 正片/反白/纯黑/纯白 + 暗色模式 |
| 图标系统 | favicon 组、app 图标、界面图标组 | 全尺寸导出(见 scene-matrix) |
| 社媒传播 | OG 分享图、README banner、公众号封面 | 固定画幅各一张 |
| 插画资产 | 空状态、404/500 配图、onboarding 引导图 | 至少深浅底两版 |
| 物料延展 | 海报、badge、名片样式 | 正片即可 |

## 工作流

### 1. 定场景
确认:哪类资产?用在什么媒介(网页/app/印刷/社媒)?目标尺寸?深底还是浅底?有无已有品牌资料?
**判据前置**:如果用户要的其实是完整页面/界面 → 转 `zdesign`;只是结构图示无品牌诉求 → 转 `diagram-design`,不抢活。

### 2. 定基调(与 zdesign 共享品牌源)
查找顺序:`.zdev/design/brands/<slug>/DESIGN.md`(本地已归档,直接用)→ 没有则现场蒸馏(官网 URL 抓取 / 截图分析 / 已知范式),落盘回填 `brands/` 归档——从此同品牌零成本复跑。
没有既定品牌时,与用户确认 2-3 个色调方向再继续,不要擅自拍板配色。

### 3. 探索
并排出 2-3 个方向的 SVG 初稿,交用户选向。初稿就要有几何骨架(网格对齐、比例关系明确),不做随手涂鸦稿。

### 4. 精修
选中方向上做光学修正(视觉重量均衡)、网格对齐、极小尺寸可辨识度调整。每改一轮浏览器亲眼看一眼。

### 5. 变体与导出
按【场景矩阵】和 `references/scene-matrix.md` 出全套:
- 变体:正片/反白/纯黑/纯白,需要暗色模式的场景补 `prefers-color-scheme` 双色版本
- 导出:从 SVG 母版按场景规格导出 PNG/ICO 各尺寸(浏览器打开母版逐个截图导出)
- 探索阶段未选中方向的草稿移入 `<slug>/explore/` 留痕,不混在交付目录

### 6. 门禁(闭环)
按 `references/quality-checklist.md` 逐项自检:**缩放测试(16px 可辨识)/ 单色测试 / 对比度 AA**,外加 SVG 工程质量。未全过 → 回第 4 步修,过了才交付。

### 7. 交付
返回:文件清单表(文件名/用途/尺寸)+ 所用品牌基调来源 + 验收结果。
logo 场景额外附 mini brand guide(见 quality-checklist 模板):色值表、最小使用尺寸、禁用示例。

## 【约束】硬规则

1. **矢量强制**:SVG 母版为真源,导出物不得反向编辑;SVG 内禁止内嵌位图。
2. **原创性红线**:可以参考风格取向,**禁止临摹或近似知名品牌 logo**——用户拿某大厂 logo 说"照这个来",要提醒侵权风险并改为风格级参考。
3. **字体版权**:大字标/banner 大字所用字体必须核商用授权;未确认授权的字体只出风格稿并列出免费可商用候选(思源黑体/霞鹜文楷等),不直接交付成品。
4. **防 AI 感红线**:禁 emoji 充当图标主体、禁默认 indigo/violet 当主色、禁渐变涂色替代真实造型、几何关系必须有据(网格/黄金比/等距)不凭感觉。
5. **SVG 工程质量**:viewBox 规范、id 全局唯一、路径合并去冗余、单文件体积克制(质量损失为零的前提下精简,一般 < 512KB)。

## 【验收】交付前自检(logo/图标类必做)

- [ ] 缩放到 16px 仍能认出主体轮廓
- [ ] 转纯黑后形态完整不糊(单色测试)
- [ ] 与常用底色的对比度达 AA(文字元素必达)
- [ ] 全套变体齐全且相互一致
- [ ] 浏览器打开成品亲眼确认(web 场景必做)——深浅底下都不破
- [ ] SVG 工程质量过关(无内嵌位图/id 唯一/体积合理)

**未全过 → 回炉,绝不交付半成品。**

## 输出格式

```
## 产出
<slug> @ .zdev/design/assets/<slug>/
| 文件 | 用途 | 尺寸 |

## 基调
<品牌 slug + DESIGN.md 来源(本地归档/现场蒸馏)/未指定自拟>

## 验收
<quality-checklist 逐项 ✓>

## 待确认(可选)
<授权风险/风格偏好等遗留项>
```

## 资产
- `references/scene-matrix.md` — 各场景精确规格:logo 变体矩阵、favicon/app 图标尺寸表、OG/banner 画幅、插画清单
- `references/quality-checklist.md` — 三测门禁细则 + SVG 工程质量检查 + mini brand guide 模板
