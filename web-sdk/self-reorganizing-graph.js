
class TopoSpaceSelfReorgGraph extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={nodes:[],edges:[]};}
 connectedCallback(){this.render()} setData(d){this.data=d||{nodes:[],edges:[]};this.render()}
 render(){
  const d=this.data,nodes=d.nodes||[],edges=(d.edges||[]).filter(e=>e.active!==false),W=940,H=540,cx=W/2,cy=H/2;
  const ring={task:0,agent:150,tool:205,memory:250,context:190},pos={};
  const groups={};nodes.forEach(n=>(groups[n.kind]??=[]).push(n));
  Object.entries(groups).forEach(([kind,arr])=>arr.forEach((n,i)=>{if(kind==="task"){pos[n.id]=[cx,cy];return;}const r=ring[kind]||220,a=2*Math.PI*i/Math.max(1,arr.length)-Math.PI/2;pos[n.id]=[cx+r*Math.cos(a),cy+r*Math.sin(a)]}));
  const lines=edges.map(e=>{const a=pos[e.source],b=pos[e.target];if(!a||!b)return "";const w=Math.max(.5,4*(e.weight||.2));return `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="currentColor" stroke-width="${w}" opacity="${.15+.55*(e.weight||.2)}"/><text x="${(a[0]+b[0])/2}" y="${(a[1]+b[1])/2}" fill="currentColor" opacity=".55" font-size="9">${e.relation}</text>`}).join("");
  const circles=nodes.map(n=>{const p=pos[n.id],r=10+16*(n.score||.2);return `<g><circle cx="${p[0]}" cy="${p[1]}" r="${n.kind==="task"?30:r}" fill="none" stroke="currentColor" stroke-width="2"/><text x="${p[0]}" y="${p[1]+3}" fill="currentColor" text-anchor="middle" font-size="10">${n.id}</text></g>`}).join("");
  this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#dce9ff;border:1px solid #2d3f5e;border-radius:16px;padding:16px;font-family:Inter,system-ui}.top{display:flex;justify-content:space-between;margin-bottom:8px}svg{width:100%;height:auto}</style><div class="top"><b>Self-Reorganizing Agent Topology</b><span>step ${d.step||0} · graph v${d.version||0} · p=${Number(d.p||2).toFixed(2)} · ε=${Number(d.epsilon||0).toFixed(3)}</span></div><svg viewBox="0 0 ${W} ${H}">${lines}${circles}</svg>`;
 }
}
customElements.define("topospace-self-reorg-graph",TopoSpaceSelfReorgGraph);
window.TopoSpaceSelfReorgGraphSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-self-reorg-graph");h.replaceChildren(e);e.setData(data);return e;}};
