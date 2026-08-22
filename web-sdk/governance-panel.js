
class TopoSpaceGovernancePanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data;
  this.shadowRoot.innerHTML=`<style>
  :host{display:block;background:#0a1322;color:#eef4ff;border:1px solid #2b3c59;border-radius:14px;padding:16px;font-family:Inter,system-ui}
  .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.c{background:#121d30;border-radius:10px;padding:12px}.v{font-size:20px;font-weight:800;margin-top:5px}
  @media(max-width:700px){.grid{grid-template-columns:1fr 1fr}}</style>
  <b>Policy Governance</b><div class="grid">
  <div class="c">Approval<div class="v">${d.approval||"Pending"}</div></div>
  <div class="c">Regions<div class="v">${d.regions||0}</div></div>
  <div class="c">Lineage<div class="v">${d.lineage||0}</div></div>
  <div class="c">DR status<div class="v">${d.dr||"Ready"}</div></div></div>`;
 }
}
customElements.define("topospace-governance-panel",TopoSpaceGovernancePanel);
window.TopoSpaceGovernancePanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-governance-panel");h.replaceChildren(e);e.setData(data);return e;}};
