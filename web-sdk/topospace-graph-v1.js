
class TopoSpaceGraphV1 extends HTMLElement{
 constructor(){
  super();this.attachShadow({mode:"open"});this.data={nodes:[],edges:[]};this.frames=[];this.frameIndex=-1;
  this.scale=1;this.pan={x:0,y:0};this.positions={};this.drag=null;
 }
 connectedCallback(){this.renderShell();this.draw();}
 setGraph(data){this.data=data||{nodes:[],edges:[]};this.computePositions();this.draw();}
 pushFrame(frame){this.frames.push(frame);this.frameIndex=this.frames.length-1;this.setGraph(frame.payload||frame);this.updateTimeline();}
 setHistory(frames){this.frames=frames||[];this.frameIndex=this.frames.length-1;if(this.frameIndex>=0)this.setGraph(this.frames[this.frameIndex].payload||this.frames[this.frameIndex]);this.updateTimeline();}
 renderShell(){
  this.shadowRoot.innerHTML=`<style>
  :host{display:block;min-height:620px;background:#08101d;color:#eef4ff;border-radius:16px;overflow:hidden;font-family:Inter,system-ui}
  .wrap{display:grid;grid-template-columns:minmax(0,1fr) 320px;min-height:620px}.stage{position:relative;overflow:hidden}.side{border-left:1px solid #26354f;padding:16px;overflow:auto}
  svg{width:100%;height:100%;min-height:620px;touch-action:none}.edge{stroke:#536682;stroke-opacity:.45}.label{fill:#eef3ff;font-size:12px}.node{cursor:grab}
  .card{background:#121c30;padding:10px;border-radius:9px;margin:8px 0}.metric{display:flex;justify-content:space-between;padding:4px 0}.timeline{display:flex;gap:4px;flex-wrap:wrap}.tick{width:22px;height:22px;border-radius:5px;border:1px solid #41516d;background:#17233a;color:#dce6fa;cursor:pointer}
  button{background:#17233a;color:#eef4ff;border:1px solid #41516d;border-radius:7px;padding:6px 9px;cursor:pointer}
  @media(max-width:800px){.wrap{grid-template-columns:1fr}.side{border-left:0;border-top:1px solid #26354f}}
  </style><div class="wrap"><div class="stage"><svg viewBox="0 0 1000 620"><g id="viewport"></g></svg></div><aside class="side">
  <b>TopoSpace Graph v1</b>
  <div class="card"><div class="metric"><span>Zoom</span><b id="zoom">1.00×</b></div><button id="reset">Reset view</button></div>
  <div class="card"><b>Time travel</b><div class="timeline" id="timeline"></div></div>
  <div class="card" id="inspector">Select a node</div>
  </aside></div>`;
  const svg=this.shadowRoot.querySelector("svg");
  svg.addEventListener("wheel",e=>{e.preventDefault();this.scale=Math.max(.3,Math.min(3,this.scale*(e.deltaY<0?1.1:.9)));this.applyTransform();},{passive:false});
  let panning=null;
  svg.addEventListener("pointerdown",e=>{if(e.target===svg){panning={x:e.clientX,y:e.clientY,px:this.pan.x,py:this.pan.y};svg.setPointerCapture(e.pointerId)}});
  svg.addEventListener("pointermove",e=>{if(panning){this.pan.x=panning.px+(e.clientX-panning.x);this.pan.y=panning.py+(e.clientY-panning.y);this.applyTransform();}});
  svg.addEventListener("pointerup",()=>panning=null);
  this.shadowRoot.getElementById("reset").onclick=()=>{this.scale=1;this.pan={x:0,y:0};this.applyTransform();};
 }
 computePositions(){
  const nodes=this.data.nodes||[]; const cx=500,cy=300,rad=Math.min(230,120+nodes.length*10);
  nodes.forEach((n,i)=>{if(!this.positions[n.id]){const a=2*Math.PI*i/Math.max(nodes.length,1)-Math.PI/2;this.positions[n.id]={x:cx+Math.cos(a)*rad,y:cy+Math.sin(a)*rad};}});
 }
 applyTransform(){const g=this.shadowRoot.getElementById("viewport");if(g)g.setAttribute("transform",`translate(${this.pan.x} ${this.pan.y}) scale(${this.scale})`);const z=this.shadowRoot.getElementById("zoom");if(z)z.textContent=this.scale.toFixed(2)+"×";}
 draw(){
  const g=this.shadowRoot&&this.shadowRoot.getElementById("viewport"); if(!g)return; g.innerHTML="";
  const nodes=this.data.nodes||[], edges=this.data.edges||[];this.computePositions();
  edges.forEach(e=>{const a=this.positions[e.source],b=this.positions[e.target];if(!a||!b)return;const l=document.createElementNS("http://www.w3.org/2000/svg","line");
   l.setAttribute("x1",a.x);l.setAttribute("y1",a.y);l.setAttribute("x2",b.x);l.setAttribute("y2",b.y);l.setAttribute("class","edge");l.setAttribute("stroke-width",1+3*(e.affinity||0));g.appendChild(l);});
  nodes.forEach(n=>{const p=this.positions[n.id],grp=document.createElementNS("http://www.w3.org/2000/svg","g");grp.setAttribute("class","node");
   const c=document.createElementNS("http://www.w3.org/2000/svg","circle");c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);c.setAttribute("r",10+16*(n.score||0));c.setAttribute("fill","#162641");c.setAttribute("stroke","#8ba7d8");c.setAttribute("stroke-width","2");grp.appendChild(c);
   const t=document.createElementNS("http://www.w3.org/2000/svg","text");t.setAttribute("x",p.x+16);t.setAttribute("y",p.y+4);t.setAttribute("class","label");t.textContent=n.label||n.id;grp.appendChild(t);
   grp.addEventListener("pointerdown",e=>{e.stopPropagation();this.drag={id:n.id,ox:e.clientX,oy:e.clientY,x:p.x,y:p.y};grp.setPointerCapture(e.pointerId)});
   grp.addEventListener("pointermove",e=>{if(this.drag&&this.drag.id===n.id){this.positions[n.id]={x:this.drag.x+(e.clientX-this.drag.ox)/this.scale,y:this.drag.y+(e.clientY-this.drag.oy)/this.scale};this.draw();}});
   grp.addEventListener("pointerup",()=>this.drag=null);grp.addEventListener("click",()=>this.inspect(n));g.appendChild(grp);});
  this.applyTransform();
 }
 inspect(n){
  const c=n.components||{};this.shadowRoot.getElementById("inspector").innerHTML=`<b>${n.label||n.id}</b><div class="metric"><span>score</span><b>${Number(n.score||0).toFixed(3)}</b></div>`+
  Object.entries(c).map(([k,v])=>`<div class="metric"><span>${k}</span><span>${Number(v).toFixed(3)}</span></div>`).join("");
  this.dispatchEvent(new CustomEvent("node-select",{detail:n,bubbles:true,composed:true}));
 }
 updateTimeline(){
  const el=this.shadowRoot&&this.shadowRoot.getElementById("timeline");if(!el)return;el.innerHTML="";
  this.frames.forEach((f,i)=>{const b=document.createElement("button");b.className="tick";b.textContent=i+1;b.title=f.event||`Frame ${i+1}`;b.onclick=()=>{this.frameIndex=i;this.setGraph(f.payload||f)};el.appendChild(b);});
 }
 connectSSE(url){
  const es=new EventSource(url);
  es.addEventListener("topology",e=>{try{this.pushFrame(JSON.parse(e.data))}catch(_){}});
  es.onmessage=e=>{try{this.pushFrame(JSON.parse(e.data))}catch(_){}};
  return es;
 }
 clusterByType(){
  const groups={};(this.data.nodes||[]).forEach(n=>(groups[n.type||"context"]??=[]).push(n));
  const keys=Object.keys(groups),cx=500,cy=300,R=190;
  keys.forEach((k,gi)=>{const a=2*Math.PI*gi/Math.max(keys.length,1)-Math.PI/2,cc={x:cx+Math.cos(a)*R,y:cy+Math.sin(a)*R};
    groups[k].forEach((n,i)=>{const aa=2*Math.PI*i/Math.max(groups[k].length,1);this.positions[n.id]={x:cc.x+Math.cos(aa)*55,y:cc.y+Math.sin(aa)*55};});
  });this.draw();
 }
}
customElements.define("topospace-graph-v1",TopoSpaceGraphV1);
window.TopoSpaceGraphV1SDK={mount(selector,data){const host=document.querySelector(selector),el=document.createElement("topospace-graph-v1");host.replaceChildren(el);el.setGraph(data);return el;}};
