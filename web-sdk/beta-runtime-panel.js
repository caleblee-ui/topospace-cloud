
class TopoSpaceBetaRuntimePanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render()} setData(d){this.data=d||{};this.render()}
 render(){const d=this.data;this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:Inter,system-ui}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.c{background:#121d30;padding:13px;border-radius:10px}.v{font-size:20px;font-weight:800;margin-top:5px}</style><b>TopoSpace 1.1 Beta Runtime</b><div class="grid"><div class="c">Mode<div class="v">Remote SDK</div></div><div class="c">Tenant isolation<div class="v">${d.tenant?"PASS":"CHECK"}</div></div><div class="c">Runtime API<div class="v">${d.api?"PASS":"CHECK"}</div></div><div class="c">TorusDB path<div class="v">${d.torus?"READY":"CHECK"}</div></div></div>`}}
customElements.define("topospace-beta-runtime-panel",TopoSpaceBetaRuntimePanel);
window.TopoSpaceBetaRuntimePanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-beta-runtime-panel");h.replaceChildren(e);e.setData(data);return e;}};
