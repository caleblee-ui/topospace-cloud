
class TopoSpaceAutopilotPanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data.decision||{},s=this.data.signals||{},reasons=d.reason||[];
  this.shadowRoot.innerHTML=`<style>
 :host{display:block;background:#0b1423;color:#eef4ff;border:1px solid #293b58;border-radius:14px;padding:16px;font-family:Inter,system-ui}
 .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.m{background:#121d30;border-radius:10px;padding:12px}.v{font-size:21px;font-weight:800;margin-top:5px}
 .reason{display:inline-block;margin:4px 5px 0 0;padding:5px 8px;border:1px solid #405574;border-radius:999px;color:#afc1da;font-size:12px}
 @media(max-width:700px){.grid{grid-template-columns:1fr 1fr}}</style>
 <b>Topology Autopilot</b><div class="grid">
 <div class="m">ε<div class="v">${Number(d.epsilon||0).toFixed(3)}</div></div>
 <div class="m">Lp exponent<div class="v">${Number(d.p||0).toFixed(2)}</div></div>
 <div class="m">Token budget<div class="v">${d.max_context_tokens||0}</div></div>
 <div class="m">Memory depth<div class="v">${d.memory_recall_limit||0}</div></div>
 <div class="m">Tool radius<div class="v">${Number(d.tool_radius||0).toFixed(3)}</div></div>
 <div class="m">Exploration<div class="v">${Number(d.exploration||0).toFixed(2)}</div></div>
 </div><div style="margin-top:10px">${reasons.map(r=>`<span class="reason">${r}</span>`).join("")}</div>`;
 }
}
customElements.define("topospace-autopilot-panel",TopoSpaceAutopilotPanel);
window.TopoSpaceAutopilotPanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-autopilot-panel");h.replaceChildren(e);e.setData(data);return e;}};
