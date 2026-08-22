
export type OptimizeRequest = {
  objective: string;
  context: Array<Record<string, unknown>>;
  agents?: Array<Record<string, unknown>>;
  required_capabilities?: string[];
  uncertainty?: number;
  drift?: number;
  previous_success?: boolean;
  cost_pressure?: number;
  complexity?: number;
};
export class TopoSpaceClient {
  constructor(public baseURL="http://localhost:8787", public keyId?:string, public key?:string) {}
  async optimize(payload:OptimizeRequest){
    const headers:any={"content-type":"application/json"};
    if(this.keyId)headers["x-topospace-key-id"]=this.keyId;
    if(this.key)headers["x-topospace-key"]=this.key;
    const r=await fetch(this.baseURL.replace(/\/$/,"")+"/v1/optimize",{method:"POST",headers,body:JSON.stringify(payload)});
    if(!r.ok)throw new Error(`TopoSpace HTTP ${r.status}`);
    return await r.json();
  }
}
