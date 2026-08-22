
class TopoSpaceRuntimeSDKPanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render()} setData(d){this.data=d||{};this.render()}
 render(){const d=this.data,h=d.hooks||[];this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#edf3ff;border:1px solid #2d3f5e;border-radius:16px;padding:18px;font-family:Inter,system-ui}.flow{display:flex;gap:8px;flex-wrap:wrap}.h{background:#121d30;border:1px solid #344966;border-radius:9px;padding:9px 11px}.k{font-size:22px;font-weight:800}</style><b>TopoSpace Runtime SDK</b><div class="k">${d.framework||"Framework-agnostic middleware"}</div><div class="flow">${h.map(x=>`<div class="h">${x}</div>`).join("")}</div>`}}
customElements.define("topospace-runtime-sdk-panel",TopoSpaceRuntimeSDKPanel);
window.TopoSpaceRuntimeSDKPanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-runtime-sdk-panel");h.replaceChildren(e);e.setData(data);return e;}};
