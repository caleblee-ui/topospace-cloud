
export class TopoSpaceLiveClient {
  constructor(graph, baseURL, workspace){
    this.graph=graph;this.baseURL=baseURL.replace(/\/$/,"");this.workspace=workspace;this.seq=0;this.timer=null;
  }
  async loadLatest(){
    const r=await fetch(`${this.baseURL}/workspaces/${encodeURIComponent(this.workspace)}/graph/latest`);
    const x=await r.json();this.seq=x.seq||0;this.graph.setGraph(x.payload||{nodes:[],edges:[]});return x;
  }
  async loadHistory(limit=100){
    const r=await fetch(`${this.baseURL}/workspaces/${encodeURIComponent(this.workspace)}/graph/history?limit=${limit}`);
    const x=await r.json();this.graph.setHistory?.(x.slice().reverse());return x;
  }
  connect(){
    const poll=async()=>{
      try{
        const r=await fetch(`${this.baseURL}/workspaces/${encodeURIComponent(this.workspace)}/events?since=${this.seq}`);
        const text=await r.text();
        for(const block of text.split("\n\n")){
          const line=block.split("\n").find(x=>x.startsWith("data: "));
          if(!line)continue;
          const frame=JSON.parse(line.slice(6));this.seq=Math.max(this.seq,frame.seq||0);
          if(this.graph.pushFrame)this.graph.pushFrame(frame);else this.graph.setGraph(frame.payload);
        }
      }catch(e){this.graph.dispatchEvent(new CustomEvent("live-error",{detail:e}));}
      this.timer=setTimeout(poll,350);
    };poll();return this;
  }
  close(){if(this.timer)clearTimeout(this.timer);this.timer=null;}
}
