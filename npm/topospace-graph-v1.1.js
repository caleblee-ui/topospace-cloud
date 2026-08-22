
class TopoSpaceGraphV11 extends HTMLElement {
  constructor(){
    super();
    this.attachShadow({mode:"open"});
    this.data={nodes:[],edges:[]};
    this.positions={};
    this.scale=1;
    this.pan={x:0,y:0};
    this.edgeTypes=new Set();
    this.epsilon=1;
    this.animation=null;
  }
  connectedCallback(){this.renderShell();this.layoutForce(80);this.draw();}
  setGraph(data){
    this.data=data||{nodes:[],edges:[]};
    this.edgeTypes=new Set((this.data.edges||[]).map(e=>e.type||"topological"));
    this.layoutForce(90);
    this.refreshControls();
    this.draw();
  }
  renderShell(){
    this.shadowRoot.innerHTML=`<style>
      :host{display:block;min-height:660px;background:#08101d;color:#eef4ff;border-radius:16px;overflow:hidden;font-family:Inter,system-ui}
      .wrap{display:grid;grid-template-columns:minmax(0,1fr) 340px;min-height:660px}
      .stage{position:relative;overflow:hidden}.side{border-left:1px solid #26354f;padding:16px;overflow:auto}
      svg{width:100%;height:100%;min-height:660px;touch-action:none}
      .edge{stroke:#5a6d8a;stroke-opacity:.42}.ring{fill:none;stroke:#6d84aa;stroke-dasharray:6 8;stroke-opacity:.35}
      .label{fill:#eef3ff;font-size:12px}.node{cursor:grab}
      .card{background:#121c30;padding:10px;border-radius:10px;margin:8px 0}.metric{display:flex;justify-content:space-between;padding:4px 0}
      .filters{display:flex;flex-wrap:wrap;gap:6px}.chip{padding:5px 8px;border:1px solid #41516d;border-radius:999px;background:#17233a;color:#eaf1ff;cursor:pointer}
      .chip.off{opacity:.35}button{background:#17233a;color:#eef4ff;border:1px solid #41516d;border-radius:7px;padding:6px 9px;cursor:pointer}
      input{width:100%}@media(max-width:820px){.wrap{grid-template-columns:1fr}.side{border-left:0;border-top:1px solid #26354f}}
    </style>
    <div class="wrap">
      <div class="stage"><svg viewBox="0 0 1000 660"><g id="viewport"></g></svg></div>
      <aside class="side">
        <b>TopoSpace Graph v1.1</b>
        <div class="card">
          <div class="metric"><span>ε filtration</span><b id="eps">${this.epsilon.toFixed(2)}</b></div>
          <input id="epsilon" type="range" min="0" max="1" step=".01" value="${this.epsilon}">
          <div style="margin-top:8px"><button id="animate">Animate filtration</button> <button id="reset">Reset</button></div>
        </div>
        <div class="card"><b>Edge types</b><div id="filters" class="filters"></div></div>
        <div class="card"><button id="force">Re-layout</button> <button id="cluster">Cluster by type</button></div>
        <div id="inspector" class="card">Select a node</div>
      </aside>
    </div>`;
    this.shadowRoot.getElementById("epsilon").oninput=e=>{
      this.epsilon=+e.target.value;
      this.shadowRoot.getElementById("eps").textContent=this.epsilon.toFixed(2);
      this.draw();
    };
    this.shadowRoot.getElementById("animate").onclick=()=>this.animateFiltration();
    this.shadowRoot.getElementById("reset").onclick=()=>{this.scale=1;this.pan={x:0,y:0};this.epsilon=1;this.shadowRoot.getElementById("epsilon").value=1;this.shadowRoot.getElementById("eps").textContent="1.00";this.layoutForce(70);this.draw();};
    this.shadowRoot.getElementById("force").onclick=()=>{this.layoutForce(120);this.draw();};
    this.shadowRoot.getElementById("cluster").onclick=()=>{this.clusterByType();this.draw();};
    const svg=this.shadowRoot.querySelector("svg");
    svg.addEventListener("wheel",e=>{e.preventDefault();this.scale=Math.max(.25,Math.min(4,this.scale*(e.deltaY<0?1.1:.9)));this.applyTransform();},{passive:false});
    let panning=null;
    svg.addEventListener("pointerdown",e=>{if(e.target===svg){panning={x:e.clientX,y:e.clientY,px:this.pan.x,py:this.pan.y};}});
    svg.addEventListener("pointermove",e=>{if(panning){this.pan.x=panning.px+(e.clientX-panning.x);this.pan.y=panning.py+(e.clientY-panning.y);this.applyTransform();}});
    svg.addEventListener("pointerup",()=>panning=null);
  }
  refreshControls(){
    if(!this.shadowRoot.querySelector("#filters")) return;
    const filters=this.shadowRoot.getElementById("filters");filters.innerHTML="";
    [...new Set((this.data.edges||[]).map(e=>e.type||"topological"))].forEach(type=>{
      const b=document.createElement("button");b.className="chip";b.textContent=type;
      b.onclick=()=>{if(this.edgeTypes.has(type)){this.edgeTypes.delete(type);b.classList.add("off")}else{this.edgeTypes.add(type);b.classList.remove("off")}this.draw();};
      filters.appendChild(b);
    });
  }
  activeNodes(){
    const max=Math.max(...(this.data.nodes||[]).map(n=>n.score||0),1e-9);
    return (this.data.nodes||[]).filter(n=>n.type==="state" || ((n.score||0)/max) >= 1-this.epsilon);
  }
  layoutForce(iterations=80){
    const nodes=this.data.nodes||[],edges=this.data.edges||[];
    const W=1000,H=660;
    nodes.forEach((n,i)=>{
      if(!this.positions[n.id]){const a=2*Math.PI*i/Math.max(1,nodes.length);this.positions[n.id]={x:W/2+Math.cos(a)*220,y:H/2+Math.sin(a)*220};}
    });
    for(let k=0;k<iterations;k++){
      const force={};nodes.forEach(n=>force[n.id]={x:0,y:0});
      for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){
        const a=this.positions[nodes[i].id],b=this.positions[nodes[j].id],dx=a.x-b.x,dy=a.y-b.y,d2=Math.max(100,dx*dx+dy*dy),d=Math.sqrt(d2),rep=6000/d2;
        force[nodes[i].id].x+=rep*dx/d;force[nodes[i].id].y+=rep*dy/d;force[nodes[j].id].x-=rep*dx/d;force[nodes[j].id].y-=rep*dy/d;
      }
      edges.forEach(e=>{
        const a=this.positions[e.source],b=this.positions[e.target];if(!a||!b)return;
        const dx=b.x-a.x,dy=b.y-a.y,d=Math.max(1,Math.sqrt(dx*dx+dy*dy)),target=120+120*(e.distance||0),spring=.004*(d-target);
        force[e.source].x+=spring*dx/d;force[e.source].y+=spring*dy/d;force[e.target].x-=spring*dx/d;force[e.target].y-=spring*dy/d;
      });
      nodes.forEach(n=>{const p=this.positions[n.id],f=force[n.id];p.x=Math.max(50,Math.min(W-50,p.x+f.x));p.y=Math.max(50,Math.min(H-50,p.y+f.y));});
    }
  }
  clusterByType(){
    const groups={};(this.data.nodes||[]).forEach(n=>(groups[n.type||"context"]??=[]).push(n));
    const keys=Object.keys(groups),cx=500,cy=330,R=210;
    keys.forEach((k,gi)=>{const a=2*Math.PI*gi/Math.max(1,keys.length),cc={x:cx+Math.cos(a)*R,y:cy+Math.sin(a)*R};
      groups[k].forEach((n,i)=>{const aa=2*Math.PI*i/Math.max(1,groups[k].length);this.positions[n.id]={x:cc.x+Math.cos(aa)*60,y:cc.y+Math.sin(aa)*60};});
    });
  }
  animateFiltration(){
    if(this.animation) clearInterval(this.animation);
    this.epsilon=0;
    this.shadowRoot.getElementById("epsilon").value=0;
    this.animation=setInterval(()=>{
      this.epsilon=Math.min(1,this.epsilon+.025);
      this.shadowRoot.getElementById("epsilon").value=this.epsilon;
      this.shadowRoot.getElementById("eps").textContent=this.epsilon.toFixed(2);
      this.draw();
      if(this.epsilon>=1){clearInterval(this.animation);this.animation=null;}
    },80);
  }
  applyTransform(){const g=this.shadowRoot.getElementById("viewport");if(g)g.setAttribute("transform",`translate(${this.pan.x} ${this.pan.y}) scale(${this.scale})`);}
  draw(){
    const g=this.shadowRoot&&this.shadowRoot.getElementById("viewport");if(!g)return;g.innerHTML="";
    const nodes=this.activeNodes(), ids=new Set(nodes.map(n=>n.id));
    const edges=(this.data.edges||[]).filter(e=>ids.has(e.source)&&ids.has(e.target)&&this.edgeTypes.has(e.type||"topological")&&((e.distance??0)<=this.epsilon));
    const state=nodes.find(n=>n.type==="state");
    if(state){
      const p=this.positions[state.id];
      [90,170,250].forEach(r=>{const c=document.createElementNS("http://www.w3.org/2000/svg","circle");c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);c.setAttribute("r",r);c.setAttribute("class","ring");g.appendChild(c);});
    }
    edges.forEach(e=>{const a=this.positions[e.source],b=this.positions[e.target];if(!a||!b)return;const l=document.createElementNS("http://www.w3.org/2000/svg","line");
      l.setAttribute("x1",a.x);l.setAttribute("y1",a.y);l.setAttribute("x2",b.x);l.setAttribute("y2",b.y);l.setAttribute("class","edge");l.setAttribute("stroke-width",1+3*(e.affinity||0));g.appendChild(l);});
    const max=Math.max(...nodes.map(n=>n.score||0),1e-9);
    nodes.forEach(n=>{const p=this.positions[n.id],grp=document.createElementNS("http://www.w3.org/2000/svg","g");grp.setAttribute("class","node");
      const c=document.createElementNS("http://www.w3.org/2000/svg","circle");c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);c.setAttribute("r",11+16*((n.score||0)/max));c.setAttribute("fill","#162641");c.setAttribute("stroke","#8ba7d8");c.setAttribute("stroke-width",n.type==="state"?"3":"2");grp.appendChild(c);
      const t=document.createElementNS("http://www.w3.org/2000/svg","text");t.setAttribute("x",p.x+17);t.setAttribute("y",p.y+4);t.setAttribute("class","label");t.textContent=n.label||n.id;grp.appendChild(t);
      let drag=null;grp.addEventListener("pointerdown",e=>{e.stopPropagation();drag={x:e.clientX,y:e.clientY,px:p.x,py:p.y};grp.setPointerCapture(e.pointerId)});
      grp.addEventListener("pointermove",e=>{if(drag){this.positions[n.id]={x:drag.px+(e.clientX-drag.x)/this.scale,y:drag.py+(e.clientY-drag.y)/this.scale};this.draw();}});
      grp.addEventListener("pointerup",()=>drag=null);grp.onclick=()=>this.inspect(n);g.appendChild(grp);});
    this.applyTransform();
  }
  inspect(n){const c=n.components||{};this.shadowRoot.getElementById("inspector").innerHTML=`<b>${n.label||n.id}</b><div class="metric"><span>score</span><b>${Number(n.score||0).toFixed(3)}</b></div>`+Object.entries(c).map(([k,v])=>`<div class="metric"><span>${k}</span><span>${Number(v).toFixed(3)}</span></div>`).join("");}
}
customElements.define("topospace-graph-v1-1",TopoSpaceGraphV11);
window.TopoSpaceGraphV11SDK={mount(selector,data){const host=document.querySelector(selector),el=document.createElement("topospace-graph-v1-1");host.replaceChildren(el);el.setGraph(data);return el;}};
