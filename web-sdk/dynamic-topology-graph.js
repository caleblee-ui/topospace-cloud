
class TopoSpaceDynamicGraph extends HTMLElement{
 constructor(){super();this.attachShadow({mode:"open"});this.data={nodes:[],edges:[]};}
 connectedCallback(){this.render()} setData(d){this.data=d||{nodes:[],edges:[]};this.render()}
 render(){
  const nodes=this.data.nodes||[],edges=this.data.edges||[],W=900,H=520,cx=W/2,cy=H/2,r=190;
  const pos={};nodes.forEach((n,i)=>{const a=(Math.PI*2*i/Math.max(1,nodes.length))-Math.PI/2;pos[n.id]=[cx+r*Math.cos(a),cy+r*Math.sin(a)]});
  const lines=edges.map(e=>{const a=pos[e.source],b=pos[e.target];if(!a||!b)return "";return `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="currentColor" opacity=".22"/><text x="${(a[0]+b[0])/2}" y="${(a[1]+b[1])/2}" fill="currentColor" opacity=".55" font-size="10">${e.relation}</text>`}).join("");
  const circles=nodes.map(n=>{const p=pos[n.id];return `<g><circle cx="${p[0]}" cy="${p[1]}" r="${n.kind==="task"?28:22}" fill="none" stroke="currentColor" stroke-width="${n.state==="active"?3:1.5}"/><text x="${p[0]}" y="${p[1]-2}" text-anchor="middle" fill="currentColor" font-size="11">${n.id}</text><text x="${p[0]}" y="${p[1]+12}" text-anchor="middle" fill="currentColor" opacity=".6" font-size="9">${n.kind}</text></g>`}).join("");
  this.shadowRoot.innerHTML=`<style>:host{display:block;background:#08111f;color:#dce9ff;border:1px solid #2d3f5e;border-radius:16px;padding:16px;font-family:Inter,system-ui}.meta{display:flex;justify-content:space-between;margin-bottom:8px}svg{width:100%;height:auto}</style><div class="meta"><b>Dynamic Agent Topology</b><span>v${this.data.version||0} · ${nodes.length} nodes · ${edges.length} edges</span></div><svg viewBox="0 0 ${W} ${H}">${lines}${circles}</svg>`;
 }
}
customElements.define("topospace-dynamic-graph",TopoSpaceDynamicGraph);
window.TopoSpaceDynamicGraphSDK={mount(sel,data){const h=document.querySelector(sel),e=document.createElement("topospace-dynamic-graph");h.replaceChildren(e);e.setData(data);return e;}};
