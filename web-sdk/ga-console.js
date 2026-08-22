
class TopoSpaceGAConsole extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data,items=[["API v1",d.api],["TorusDB HTTP",d.torus],["Install",d.install],["Trust",d.trust],["Release Manifest",d.manifest],["Docker",d.docker]];
  this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2c3d5a;border-radius:16px;padding:18px;font-family:Inter,system-ui}.head{display:flex;justify-content:space-between;align-items:center}.ga{padding:6px 10px;border:1px solid #6786b6;border-radius:999px;font-weight:700}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:15px}.c{background:#121d30;padding:14px;border-radius:11px}.v{font-size:20px;font-weight:800;margin-top:6px}@media(max-width:720px){.grid{grid-template-columns:1fr 1fr}}</style><div class="head"><b>TopoSpace 1.0</b><span class="ga">GA</span></div><div class="grid">${items.map(x=>`<div class="c">${x[0]}<div class="v">${x[1]?"PASS":"CHECK"}</div></div>`).join("")}</div>`;
 }
}
customElements.define("topospace-ga-console",TopoSpaceGAConsole);
window.TopoSpaceGAConsoleSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-ga-console");h.replaceChildren(e);e.setData(data);return e;}};
