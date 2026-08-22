
class TopoSpaceLearningPanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data;
  this.shadowRoot.innerHTML=`<style>
 :host{display:block;background:#0b1423;color:#eef4ff;border:1px solid #2a3b59;border-radius:14px;padding:16px;font-family:Inter,system-ui}
 .row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.card{background:#121d30;border-radius:10px;padding:12px}.v{font-size:21px;font-weight:800;margin-top:5px}
 @media(max-width:700px){.row{grid-template-columns:1fr 1fr}}</style>
 <b>Self-Optimizing Autopilot</b><div class="row">
 <div class="card">Profile<div class="v">${d.profile||"—"}</div></div>
 <div class="card">Reward<div class="v">${Number(d.reward||0).toFixed(3)}</div></div>
 <div class="card">Feasible<div class="v">${d.feasible===false?"No":"Yes"}</div></div>
 <div class="card">Observations<div class="v">${d.observations||0}</div></div></div>`;
 }
}
customElements.define("topospace-learning-panel",TopoSpaceLearningPanel);
window.TopoSpaceLearningPanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-learning-panel");h.replaceChildren(e);e.setData(data);return e;}};
