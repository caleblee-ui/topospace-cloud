
class TopoSpaceMiddlewareFlow extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.events=[];}
 connectedCallback(){this.render();}
 setEvents(events){this.events=events||[];this.render();}
 render(){
  this.shadowRoot.innerHTML=`<style>
  :host{display:block;background:#08101d;color:#edf3ff;border-radius:16px;font-family:Inter,system-ui;padding:18px}
  .flow{display:grid;grid-template-columns:repeat(6,minmax(120px,1fr));gap:10px;overflow:auto}
  .step{background:#121c30;border:1px solid #2d3e5b;border-radius:12px;padding:14px;min-height:90px}
  .active{border-color:#8aa7d7}.phase{font-weight:700}.meta{color:#9dacbf;font-size:12px;margin-top:6px}
  @media(max-width:900px){.flow{grid-template-columns:repeat(3,1fr)}}
  </style><div class="flow" id="flow"></div>`;
  const flow=this.shadowRoot.getElementById("flow");
  const phases=["memory_recall","before_inference","model","before_tool","after_tool","state_update"];
  phases.forEach(p=>{
    const latest=[...this.events].reverse().find(e=>e.phase===p);
    const d=document.createElement("div");d.className="step "+(latest?"active":"");
    d.innerHTML=`<div class="phase">${p}</div><div class="meta">${latest?JSON.stringify(latest.payload).slice(0,180):"waiting"}</div>`;
    flow.appendChild(d);
  });
 }
}
customElements.define("topospace-middleware-flow",TopoSpaceMiddlewareFlow);
window.TopoSpaceMiddlewareFlowSDK={mount(sel,events){const host=document.querySelector(sel),el=document.createElement("topospace-middleware-flow");host.replaceChildren(el);el.setEvents(events);return el;}};
