
class TopoSpaceConsensusTopology extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={ranking:[]};}
 connectedCallback(){this.render()} setData(d){this.data=d||{};this.render()}
 render(){const d=this.data,r=d.ranking||[];this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:Inter,system-ui}.row{display:grid;grid-template-columns:1.5fr 1fr 1fr 3fr;gap:8px;padding:10px;margin-top:7px;background:#121d30;border-radius:9px}.win{font-size:22px;font-weight:800}</style><b>Topological Multi-Agent Consensus</b><div class="win">${d.winner||"Exploration required"}</div>${r.map(x=>`<div class="row"><span>${x.candidate_id}</span><span>${Number(x.score).toFixed(3)}</span><span>${x.support} agents</span><span>${(x.agents||[]).join(", ")}</span></div>`).join("")}`}}
customElements.define("topospace-consensus-topology",TopoSpaceConsensusTopology);
window.TopoSpaceConsensusTopologySDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-consensus-topology");h.replaceChildren(e);e.setData(data);return e;}};
