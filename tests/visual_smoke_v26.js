
class FakeElement {
  constructor(tag="x"){this.tag=tag;this.children=[];this.attrs={};this._innerHTML="";this.onclick=null;}
  setAttribute(k,v){this.attrs[k]=String(v);}
  appendChild(x){this.children.push(x);return x;}
  replaceChildren(...xs){this.children=[...xs];}
  set innerHTML(v){this._innerHTML=String(v);}
  get innerHTML(){return this._innerHTML;}
}
class FakeShadow extends FakeElement {
  constructor(){super("shadow");this.ids={g:new FakeElement("g"),inspect:new FakeElement("inspect")};}
  set innerHTML(v){this._innerHTML=String(v);}
  getElementById(id){return this.ids[id] || (this.ids[id]=new FakeElement(id));}
}
global.HTMLElement=class {
  attachShadow(){this.shadowRoot=new FakeShadow();return this.shadowRoot;}
};
global.document={createElementNS:(ns,tag)=>new FakeElement(tag),querySelector:()=>new FakeElement("host")};
const registry={};
global.customElements={define:(name,klass)=>{registry[name]=klass;}};
global.window={};

require("../web-sdk/torus-memory-graph.js");
const K=registry["torus-memory-graph"];
if(!K) throw new Error("component not registered");
const el=new K();
el.setData({
  query:"OAuth bug",
  candidate_count:4,
  context_tokens:1200,
  memories:[
    {id:"m1",label:"Decision",score:.9,distance:.1,importance:.8,drift:.05,tokens:500},
    {id:"m2",label:"Test",score:.8,distance:.2,importance:.7,drift:.07,tokens:400}
  ]
});
const g=el.shadowRoot.getElementById("g");
if(g.children.length < 5) throw new Error("expected rendered SVG children, got "+g.children.length);
el.inspect({id:"m1",label:"Decision",score:.9,distance:.1,importance:.8,drift:.05,tokens:500,ciphertext:"ENC"});
const inspect=el.shadowRoot.getElementById("inspect").innerHTML;
if(!inspect.includes("Decision") || !inspect.includes("protected")) throw new Error("inspector did not render");
console.log("visual DOM smoke PASS", g.children.length);
