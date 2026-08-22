
class TopoSpaceOptimizationV2Panel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data;
  this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:Inter,system-ui}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.c{background:#121d30;padding:13px;border-radius:10px}.v{font-size:20px;font-weight:800;margin-top:5px}@media(max-width:720px){.grid{grid-template-columns:1fr 1fr}}</style><b>Optimization Engine v2</b><div class="grid"><div class="c">Token reduction<div class="v">${Number(100*(d.reduction||0)).toFixed(1)}%</div></div><div class="c">Topology shells<div class="v">${d.shells||0}</div></div><div class="c">Visited shells<div class="v">${d.visited||0}</div></div><div class="c">Memory compaction<div class="v">${Number(100*(d.compaction||0)).toFixed(1)}%</div></div></div>`;
 }
}
customElements.define("topospace-optimization-v2-panel",TopoSpaceOptimizationV2Panel);
window.TopoSpaceOptimizationV2PanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-optimization-v2-panel");h.replaceChildren(e);e.setData(data);return e;}};
