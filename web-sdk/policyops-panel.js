
class TopoSpacePolicyOpsPanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data;
  this.shadowRoot.innerHTML=`<style>
  :host{display:block;background:#0a1322;color:#eef4ff;border:1px solid #2b3c59;border-radius:14px;padding:16px;font-family:Inter,system-ui}
  .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.c{background:#121d30;border-radius:10px;padding:12px}.v{font-size:20px;font-weight:800;margin-top:5px}
  @media(max-width:700px){.grid{grid-template-columns:1fr 1fr}}</style>
  <b>Policy Operations</b><div class="grid">
  <div class="c">Champion<div class="v">${d.champion||"—"}</div></div>
  <div class="c">Challenger<div class="v">${d.challenger||"—"}</div></div>
  <div class="c">Shadow better<div class="v">${Number(100*(d.shadow_better_rate||0)).toFixed(1)}%</div></div>
  <div class="c">Concept drift<div class="v">${d.drift?"Detected":"Stable"}</div></div></div>`;
 }
}
customElements.define("topospace-policyops-panel",TopoSpacePolicyOpsPanel);
window.TopoSpacePolicyOpsPanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-policyops-panel");h.replaceChildren(e);e.setData(data);return e;}};
