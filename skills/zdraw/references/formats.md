# zdraw · 源文件生成规范(.excalidraw / .drawio)

> 源文件是**给人继续编辑的**——骨架规范、坐标来自 layout 脚本、语义角色来自 brand-mapping。禁止手估坐标,禁止硬编码品牌色。

## .excalidraw(JSON)

最小合法骨架:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "zdraw",
  "elements": [
    {
      "id": "n1", "type": "rectangle", "x": 120, "y": 80,
      "width": 160, "height": 48, "angle": 0,
      "strokeColor": "#0b0c0e", "backgroundColor": "#ffffff",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "roundness": { "type": 3 },
      "groupIds": [], "frameId": null, "boundElements": [{"id": "t1", "type": "text"}],
      "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": false,
      "opacity": 100, "link": null, "locked": false
    },
    {
      "id": "t1", "type": "text", "x": 140, "y": 96,
      "width": 120, "height": 16, "text": "节点名",
      "fontSize": 12, "fontFamily": 2, "textAlign": "center",
      "verticalAlign": "middle", "containerId": "n1",
      "strokeColor": "#0b0c0e", "backgroundColor": "transparent",
      "angle": 0, "strokeStyle": "solid", "strokeWidth": 1,
      "roughness": 1, "seed": 2, "version": 1, "versionNonce": 2,
      "isDeleted": false, "opacity": 100, "groupIds": [],
      "frameId": null, "boundElements": null, "link": null, "locked": false
    },
    {
      "id": "e1", "type": "arrow",
      "x": 280, "y": 104, "points": [[0, 0], [80, 0]],
      "width": 80, "height": 0, "startArrowhead": null, "endArrowhead": "arrow",
      "strokeColor": "#8a8f98", "backgroundColor": "transparent",
      "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
      "seed": 3, "version": 1, "versionNonce": 3, "isDeleted": false,
      "opacity": 100, "angle": 0, "groupIds": [], "frameId": null,
      "boundElements": null, "link": null, "locked": false
    }
  ],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": null },
  "files": {}
}
```

要点:
- 节点 = `rectangle` + 绑定 `text`(`containerId` 指回 rect,`boundElements` 双向)
- 边 = `arrow`,`points` 相对起点;虚线 `strokeStyle: "dashed"`(可选/异步/返回)
- 必填元字段全套带齐(seed/version/versionNonce/isDeleted/opacity…),缺了编辑器打不开
- 手绘感由 `roughness` 控制:白板 1(潦草)/ 正式 0(架构);`roundness: {"type": 3}` 圆角

## .drawio(XML)

最小合法骨架:

```xml
<mxfile host="zdraw">
  <diagram id="d1" name="页名">
    <mxGraphModel dx="800" dy="600" grid="0" gridSize="4" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="n1" value="节点名" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0b0c0e;fontColor=#0b0c0e;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="120" y="80" width="160" height="48" as="geometry"/>
        </mxCell>
        <mxCell id="e1" value="标签" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#8a8f98;fontColor=#8a8f98;fontSize=10;html=1;" edge="1" parent="1" source="n1" target="n2">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

要点:
- 节点 = `vertex` mxCell;边 = `edge` mxCell 带 `source`/`target`(连接点由编辑器自动吸附)
- style 串是分号分隔键值——**语义角色直接注入这里**(fillColor/strokeColor/fontColor)
- 正交走线 `edgeStyle=orthogonalEdgeStyle;rounded=1`;虚线加 `dashed=1`
- `gridSize="4"` 呼应 4px 网格

## 渲染与导出

| 目标 | 方式 |
|---|---|
| `.svg` | `scripts/zdraw_layout.py --svg out.svg`(内置,正交圆角+标签遮罩+箭头三件套) |
| PNG | 用户要求才做:无头 chromium 截 .svg 的 viewBox,或 drawio CLI `drawio -x -f png` |
| .drawio → SVG | `drawio -x -f svg file.drawio`(装有 drawio 桌面版时);否则改用脚本 SVG 交付 |
| .excalidraw → 图 | excalidraw.com 打开 / VSCode 插件;编辑器内可导出 PNG/SVG |

**导出是手动动作**——用户没要求不主动产出 PNG。
