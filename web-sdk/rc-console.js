
class TopoSpaceRCConsole extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data,rows=[["Contract",d.contract],["Upgrade",d.upgrade],["TorusDB E2E",d.torus],["Soak",d.soak],["Fault tolerance",d.faults],["Install",d.install],["Trust",d.trust]];
  this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#eef4ff;border:1px solid #2b3c59;border-radius:16px;padding:18px;font-family:Inter,system-ui}.head{display:flex;justify-content:space-between}.badge{padding:6px 10px;border:1px solid #4b648b;border-radius:999px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}.c{background:#121d30;border-radius:10px;padding:13px}.v{font-size:19px;font-weight:800;margin-top:5px}@media(max-width:760px){.grid{grid-template-columns:1fr 1fr}}</style><div class="head"><b>TopoSpace 1.0 Release Candidate</b><span class="badge">${d.version||"rc"}</span></div><div class="grid">${rows.map(r=>`<div class="c">${r[0]}<div class="v">${r[1]?"PASS":"CHECK"}</div></div>`).join("")}</div>`;
 }
}
customElements.define("topospace-rc-console",TopoSpaceRCConsole);
window.TopoSpaceRCConsoleSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-rc-console");h.replaceChildren(e);e.setData(data);return e;}};
