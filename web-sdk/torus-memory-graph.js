
class TorusMemoryGraph extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={memories:[],edges:[]};}
 connectedCallback(){this.render();}
 setData(data){this.data=data||{memories:[],edges:[]};this.render();}
 render(){
  const memories=this.data.memories||[], edges=this.data.edges||[];
  this.shadowRoot.innerHTML=`<style>
  :host{display:block;background:#08101d;color:#eef4ff;border-radius:16px;min-height:620px;font-family:Inter,system-ui}
  .wrap{display:grid;grid-template-columns:1fr 330px;min-height:620px}.stage{position:relative}.side{border-left:1px solid #26354f;padding:16px}
  svg{width:100%;height:620px}.edge{stroke:#506580;stroke-opacity:.5}.node{cursor:pointer}.label{fill:#edf3ff;font-size:12px}
  .card{background:#121c30;padding:10px;border-radius:10px;margin:8px 0}.metric{display:flex;justify-content:space-between;padding:4px 0}
  @media(max-width:800px){.wrap{grid-template-columns:1fr}.side{border-left:0;border-top:1px solid #26354f}}
  </style><div class="wrap"><div class="stage"><svg viewBox="0 0 980 620"><g id="g"></g></svg></div>
  <aside class="side"><b>TorusDB × TopoSpace Memory</b><div class="card"><div class="metric"><span>Candidate memories</span><b>${this.data.candidate_count??memories.length}</b></div>
  <div class="metric"><span>Selected memories</span><b>${memories.length}</b></div><div class="metric"><span>Context tokens</span><b>${this.data.context_tokens??0}</b></div></div>
  <div id="inspect" class="card">Select a memory node</div></aside></div>`;
  const g=this.shadowRoot.getElementById("g"),cx=470,cy=300,N=Math.max(1,memories.length),R=Math.min(230,120+N*12),pos={task:{x:cx,y:cy}};
  const state={id:"task",label:this.data.query||"Current task",score:1,type:"state"};
  const all=[state,...memories];
  memories.forEach((m,i)=>{const a=2*Math.PI*i/N-Math.PI/2;pos[m.id]={x:cx+Math.cos(a)*R,y:cy+Math.sin(a)*R};});
  (edges.length?edges:memories.map(m=>({source:"task",target:m.id,affinity:m.score||m.utility||.5}))).forEach(e=>{
    const a=pos[e.source],b=pos[e.target];if(!a||!b)return;const l=document.createElementNS("http://www.w3.org/2000/svg","line");
    l.setAttribute("x1",a.x);l.setAttribute("y1",a.y);l.setAttribute("x2",b.x);l.setAttribute("y2",b.y);l.setAttribute("class","edge");l.setAttribute("stroke-width",1+3*(e.affinity||.3));g.appendChild(l);
  });
  all.forEach(n=>{const p=pos[n.id]||pos.task,grp=document.createElementNS("http://www.w3.org/2000/svg","g");grp.setAttribute("class","node");
    const c=document.createElementNS("http://www.w3.org/2000/svg","circle");c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);c.setAttribute("r",n.type==="state"?20:11+14*(n.score||n.utility||.4));c.setAttribute("fill",n.type==="state"?"#243b64":"#162641");c.setAttribute("stroke","#8ba7d8");c.setAttribute("stroke-width",n.type==="state"?"3":"2");grp.appendChild(c);
    const t=document.createElementNS("http://www.w3.org/2000/svg","text");t.setAttribute("x",p.x+17);t.setAttribute("y",p.y+4);t.setAttribute("class","label");t.textContent=n.label||n.id;grp.appendChild(t);
    grp.onclick=()=>this.inspect(n);g.appendChild(grp);
  });
 }
 inspect(n){const el=this.shadowRoot.getElementById("inspect");el.innerHTML=`<b>${n.label||n.id}</b>`+
  ["score","distance","importance","drift","tokens"].filter(k=>n[k]!==undefined).map(k=>`<div class="metric"><span>${k}</span><b>${typeof n[k]==="number"?n[k].toFixed?.(3)??n[k]:n[k]}</b></div>`).join("")+
  (n.ciphertext?`<div class="metric"><span>protected</span><b>ciphertext</b></div>`:"");
 }
}
customElements.define("torus-memory-graph",TorusMemoryGraph);
window.TorusMemoryGraphSDK={mount(sel,data){const host=document.querySelector(sel),el=document.createElement("torus-memory-graph");host.replaceChildren(el);el.setData(data);return el;}};
