
class TopoSpaceTrustPanel extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data;
  this.shadowRoot.innerHTML=`<style>
 :host{display:block;background:#0a1322;color:#eef4ff;border:1px solid #2b3c59;border-radius:14px;padding:16px;font-family:Inter,system-ui}
 .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.c{background:#121d30;border-radius:10px;padding:12px}.v{font-size:20px;font-weight:800;margin-top:5px}
 @media(max-width:700px){.grid{grid-template-columns:1fr 1fr}}</style>
 <b>Enterprise Trust Layer</b><div class="grid">
 <div class="c">mTLS<div class="v">${d.mtls?"Enabled":"Disabled"}</div></div>
 <div class="c">Attestation<div class="v">${d.attested?"Verified":"Missing"}</div></div>
 <div class="c">Integrity<div class="v">${d.integrity?"Verified":"Changed"}</div></div>
 <div class="c">SBOM files<div class="v">${d.sbom_count||0}</div></div></div>`;
 }
}
customElements.define("topospace-trust-panel",TopoSpaceTrustPanel);
window.TopoSpaceTrustPanelSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-trust-panel");h.replaceChildren(e);e.setData(data);return e;}};
