
class TopoSpaceAdaptiveTopologyPanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render()} setData(d){this.data=d||{};this.render()}
 render(){const d=this.data;this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#eef4ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:Inter,system-ui}.g{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.c{background:#121d30;padding:13px;border-radius:10px}.v{font-size:20px;font-weight:800;margin-top:5px}@media(max-width:720px){.g{grid-template-columns:1fr 1fr}}</style><b>Adaptive Topological Runtime</b><div class="g"><div class="c">Dynamic p<div class="v">${d.p||2}</div></div><div class="c">Adaptive ε<div class="v">${Number(d.epsilon||0).toFixed(3)}</div></div><div class="c">Token reduction<div class="v">${Number(100*(d.reduction||0)).toFixed(1)}%</div></div><div class="c">Cache hit<div class="v">${d.cache?"YES":"NO"}</div></div></div>`}
}
customElements.define("topospace-adaptive-topology-panel",TopoSpaceAdaptiveTopologyPanel);
window.TopoSpaceAdaptiveTopologyPanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-adaptive-topology-panel");h.replaceChildren(e);e.setData(data);return e;}};
