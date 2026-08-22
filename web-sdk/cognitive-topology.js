
class TopoSpaceCognitiveTopology extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={layers:{},memories:[]};}
 connectedCallback(){this.render()} setData(d){this.data=d||{};this.render()}
 render(){const d=this.data,l=d.layers||{},mem=d.memories||[];const groups=["working","episodic","semantic"];
 this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:Inter,system-ui}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.layer{background:#121d30;border-radius:12px;padding:14px;min-height:180px}.n{font-size:24px;font-weight:800}.m{font-size:11px;padding:7px;border:1px solid #344966;border-radius:8px;margin-top:7px}@media(max-width:720px){.grid{grid-template-columns:1fr}}</style><b>Topological Cognitive Memory</b><div class="grid">${groups.map(g=>`<div class="layer"><div>${g.toUpperCase()}</div><div class="n">${l[g]||0}</div>${mem.filter(x=>x.layer===g).slice(0,8).map(x=>`<div class="m">${x.id} · ${(x.utility||0).toFixed(2)}</div>`).join("")}</div>`).join("")}</div>`}
}
customElements.define("topospace-cognitive-topology",TopoSpaceCognitiveTopology);
window.TopoSpaceCognitiveTopologySDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-cognitive-topology");h.replaceChildren(e);e.setData(data);return e;}};
