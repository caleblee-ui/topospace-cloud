
class TopoSpaceGA11Console extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render()} setData(d){this.data=d||{};this.render()}
 render(){
  const d=this.data,rows=[
   ["Generalized Geometry",d.geometry],["Joint Optimizer",d.joint],["Online Learning",d.online],
   ["Runtime Server",d.server],["TorusDB Path",d.torus],["Trust/Governance",d.trust]
  ];
  this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:system-ui}.g{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.c{background:#121d30;padding:14px;border-radius:10px}.v{font-size:20px;font-weight:800}.badge{border:1px solid #4d6489;border-radius:999px;padding:5px 10px}</style><div style="display:flex;justify-content:space-between"><b>TopoSpace 1.1</b><span class="badge">GA</span></div><div class="g">${rows.map(x=>`<div class="c">${x[0]}<div class="v">${x[1]?"PASS":"CHECK"}</div></div>`).join("")}</div>`;
 }}
customElements.define("topospace-ga11-console",TopoSpaceGA11Console);
window.TopoSpaceGA11ConsoleSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-ga11-console");h.replaceChildren(e);e.setData(data);return e;}};
