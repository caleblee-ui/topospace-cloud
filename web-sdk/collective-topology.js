
class TopoSpaceCollectiveTopology extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={agents:[],shared:[]};}
 connectedCallback(){this.render()} setData(d){this.data=d||{};this.render()}
 render(){
  const agents=this.data.agents||[],shared=this.data.shared||[];
  this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:Inter,system-ui}.wrap{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{background:#121d30;border-radius:12px;padding:14px}.agent{padding:8px;border:1px solid #344966;border-radius:8px;margin-top:7px}.shared{padding:8px;border:1px dashed #4d6589;border-radius:8px;margin-top:7px}@media(max-width:760px){.wrap{grid-template-columns:1fr}}</style><b>Collective Topology Runtime</b><div class="wrap"><div class="card"><h3>Agents</h3>${agents.map(a=>`<div class="agent">${a.id}<br><small>${(a.specialization||[]).join(", ")}</small></div>`).join("")}</div><div class="card"><h3>Shared Topology</h3>${shared.map(s=>`<div class="shared">${s.id}<br><small>${s.kind} · ${(s.score||0).toFixed(2)}</small></div>`).join("")}</div></div>`;
 }
}
customElements.define("topospace-collective-topology",TopoSpaceCollectiveTopology);
window.TopoSpaceCollectiveTopologySDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-collective-topology");h.replaceChildren(e);e.setData(data);return e;}};
