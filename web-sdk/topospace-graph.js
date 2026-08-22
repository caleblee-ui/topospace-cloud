
class TopoSpaceGraph extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={nodes:[],edges:[]};this._epsilon=1;}
 connectedCallback(){this.render();}
 setGraph(data){this.data=data||{nodes:[],edges:[]};this.render();}
 set epsilon(v){this._epsilon=Number(v);this.render();}
 get epsilon(){return this._epsilon;}
 render(){
  this.shadowRoot.innerHTML=`<style>
  :host{display:block;min-height:560px;background:#09101d;color:#eef3ff;border-radius:16px;overflow:hidden;font-family:Inter,system-ui}
  .wrap{display:grid;grid-template-columns:minmax(0,1fr) 320px;min-height:560px}.stage{position:relative}.side{border-left:1px solid #26354f;padding:16px}
  svg{width:100%;height:100%;min-height:560px}.edge{stroke:#536682;stroke-opacity:.55}.label{fill:#eef3ff;font-size:12px}.node{cursor:pointer}
  .card{background:#121c30;padding:11px;border-radius:9px;margin:9px 0}.metric{display:flex;justify-content:space-between;gap:12px;padding:4px 0}
  input{width:100%}@media(max-width:760px){.wrap{grid-template-columns:1fr}.side{border-left:0;border-top:1px solid #26354f}}
  </style><div class="wrap"><div class="stage"><svg viewBox="0 0 900 560"></svg></div><aside class="side">
  <b>TopoSpace Graph</b><div class="card"><div class="metric"><span>Context threshold</span><b id="eps">${this._epsilon.toFixed(2)}</b></div>
  <input id="slider" type="range" min="0" max="1" step=".01" value="${this._epsilon}"></div>
  <div id="inspector" class="card">Select a node</div></aside></div>`;
  this.shadowRoot.getElementById("slider").oninput=e=>{this._epsilon=+e.target.value;this.shadowRoot.getElementById("eps").textContent=this._epsilon.toFixed(2);this.draw();};this.draw();
 }
 draw(){
  const svg=this.shadowRoot.querySelector("svg");svg.innerHTML="";
  const all=this.data.nodes||[]; const maxScore=Math.max(...all.map(n=>n.score||0),1e-9);
  const nodes=all.filter(n=>((n.score||0)/maxScore)>=1-this._epsilon || n.type==="state");
  const ids=new Set(nodes.map(n=>n.id));const edges=(this.data.edges||[]).filter(e=>ids.has(e.source)&&ids.has(e.target));
  const cx=445,cy=275,N=Math.max(nodes.length,1),rad=Math.min(210,110+N*12),pos={};
  nodes.forEach((n,i)=>{const a=2*Math.PI*i/N-Math.PI/2;pos[n.id]={x:cx+Math.cos(a)*rad,y:cy+Math.sin(a)*rad};});
  edges.forEach(e=>{const a=pos[e.source],b=pos[e.target];if(!a||!b)return;const l=document.createElementNS("http://www.w3.org/2000/svg","line");
   [["x1",a.x],["y1",a.y],["x2",b.x],["y2",b.y],["class","edge"],["stroke-width",1+3*(e.affinity||0)]].forEach(([k,v])=>l.setAttribute(k,v));svg.appendChild(l);});
  nodes.forEach(n=>{const p=pos[n.id],g=document.createElementNS("http://www.w3.org/2000/svg","g");g.setAttribute("class","node");
   const c=document.createElementNS("http://www.w3.org/2000/svg","circle");c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);c.setAttribute("r",10+15*((n.score||0)/maxScore));c.setAttribute("fill","#17253f");c.setAttribute("stroke","#8da8da");c.setAttribute("stroke-width","2");g.appendChild(c);
   const t=document.createElementNS("http://www.w3.org/2000/svg","text");t.setAttribute("x",p.x+16);t.setAttribute("y",p.y+4);t.setAttribute("class","label");t.textContent=n.label||n.id;g.appendChild(t);
   g.onclick=()=>this.inspect(n);svg.appendChild(g);});
 }
 inspect(n){const c=n.components||{};this.shadowRoot.getElementById("inspector").innerHTML=`<b>${n.label||n.id}</b>
 <div class="metric"><span>hybrid score</span><b>${Number(n.score||0).toFixed(3)}</b></div>
 <div class="metric"><span>topological support</span><b>${Number(n.topological_support||0).toFixed(3)}</b></div>`+
 Object.entries(c).map(([k,v])=>`<div class="metric"><span>${k}</span><span>${Number(v).toFixed(3)}</span></div>`).join("");
 this.dispatchEvent(new CustomEvent("node-select",{detail:n,bubbles:true,composed:true}));}
}
customElements.define("topospace-graph",TopoSpaceGraph);
window.TopoSpaceGraphSDK={mount(selector,data){const host=document.querySelector(selector),el=document.createElement("topospace-graph");host.replaceChildren(el);el.setGraph(data);return el;}};
