
class TopoSpaceAdminConsole extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={};}
 connectedCallback(){this.render();}
 setData(d){this.data=d||{};this.render();}
 render(){
  const d=this.data,sla=d.sla||{},usage=d.usage||{},top=d.topology||{nodes:[],edges:[]};
  const esc=x=>String(x??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  this.shadowRoot.innerHTML=`<style>
 :host{display:block;font-family:Inter,system-ui;background:#080e19;color:#edf3ff;min-height:760px}
 .shell{display:grid;grid-template-columns:230px 1fr;min-height:760px}.nav{padding:22px;border-right:1px solid #26334a}.main{padding:22px}
 .brand{font-size:20px;font-weight:800;margin-bottom:26px}.nav div{padding:9px 0;color:#9caac0}.nav .on{color:white;font-weight:700}
 .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card{background:#111b2d;border:1px solid #263751;border-radius:14px;padding:15px}
 .big{font-size:24px;font-weight:800;margin-top:8px}.layout{display:grid;grid-template-columns:1.5fr 1fr;gap:12px;margin-top:12px}
 svg{width:100%;height:390px}.edge{stroke:#536b8f;stroke-opacity:.45}.label{fill:#dce8fb;font-size:10px}
 table{width:100%;border-collapse:collapse;font-size:12px}td,th{padding:8px;border-bottom:1px solid #263751;text-align:left}
 @media(max-width:900px){.shell{grid-template-columns:1fr}.nav{display:none}.grid{grid-template-columns:repeat(2,1fr)}.layout{grid-template-columns:1fr}}
 </style><div class="shell"><aside class="nav"><div class="brand">TopoSpace</div><div class="on">Overview</div><div>Topology</div><div>Torus Memory</div><div>Tenants</div><div>Usage</div><div>Runtime</div><div>Licenses</div></aside>
 <main class="main"><h2>Operations Console</h2><div class="grid">
 <div class="card">Requests<div class="big">${esc(usage.requests||0)}</div></div>
 <div class="card">p95 latency<div class="big">${Number(sla.p95_ms||0).toFixed(3)} ms</div></div>
 <div class="card">Context tokens<div class="big">${esc(usage.context_tokens||0)}</div></div>
 <div class="card">Topology nodes<div class="big">${top.nodes.length}</div></div></div>
 <div class="layout"><section class="card"><b>Live Topology</b><svg viewBox="0 0 760 390"><g id="graph"></g></svg></section>
 <section class="card"><b>Recent Optimizations</b><table><thead><tr><th>Task</th><th>Latency</th><th>Tokens</th></tr></thead><tbody>
 ${(d.events||[]).slice(-12).reverse().map(e=>`<tr><td>${esc(e.objective||e.type)}</td><td>${Number(e.latency_ms||0).toFixed(3)}</td><td>${esc(e.context_tokens||0)}</td></tr>`).join("")}
 </tbody></table></section></div></main></div>`;
  this.draw(top);
 }
 draw(top){
  const g=this.shadowRoot.getElementById("graph"),nodes=top.nodes||[],edges=top.edges||[],pos={},cx=380,cy=195;
  nodes.forEach((n,i)=>{const a=2*Math.PI*i/Math.max(1,nodes.length);const r=n.kind==="task"?90:155;pos[n.id]={x:cx+Math.cos(a)*r,y:cy+Math.sin(a)*r};});
  edges.forEach(e=>{if(!pos[e.source]||!pos[e.target])return;const l=document.createElementNS("http://www.w3.org/2000/svg","line");
   l.setAttribute("x1",pos[e.source].x);l.setAttribute("y1",pos[e.source].y);l.setAttribute("x2",pos[e.target].x);l.setAttribute("y2",pos[e.target].y);l.setAttribute("class","edge");g.appendChild(l);});
  nodes.forEach(n=>{const p=pos[n.id],c=document.createElementNS("http://www.w3.org/2000/svg","circle");c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);
   c.setAttribute("r",n.kind==="task"?13:9);c.setAttribute("fill","#172842");c.setAttribute("stroke","#8fa9d2");c.setAttribute("stroke-width","2");g.appendChild(c);
   const t=document.createElementNS("http://www.w3.org/2000/svg","text");t.setAttribute("x",p.x+13);t.setAttribute("y",p.y+4);t.setAttribute("class","label");t.textContent=n.label||n.id;g.appendChild(t);});
 }
}
customElements.define("topospace-admin-console",TopoSpaceAdminConsole);
window.TopoSpaceAdminConsoleSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-admin-console");h.replaceChildren(e);e.setData(data);return e;}};
