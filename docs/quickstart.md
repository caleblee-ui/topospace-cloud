
# Quickstart

## Python

```bash
pip install -e .
```

Core runtime modules are framework-neutral. Start the reference API with:

```bash
python api/server.py
```

## Web

Copy `web-sdk/topospace-graph-v1.1.js` into your app and mount:

```html
<script src="/topospace-graph-v1.1.js"></script>
<div id="graph"></div>
<script>
TopoSpaceGraphV11SDK.mount("#graph", payload);
</script>
```
