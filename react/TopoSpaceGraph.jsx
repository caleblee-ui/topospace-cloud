
import React, {useEffect, useRef} from "react";
import "../web-sdk/topospace-graph-v1.js";

export default function TopoSpaceGraph({data, history, onNodeSelect, className}) {
  const ref=useRef(null);
  useEffect(()=>{ if(ref.current && data) ref.current.setGraph(data); },[data]);
  useEffect(()=>{ if(ref.current && history) ref.current.setHistory(history); },[history]);
  useEffect(()=>{
    const el=ref.current; if(!el || !onNodeSelect) return;
    const fn=e=>onNodeSelect(e.detail); el.addEventListener("node-select",fn);
    return ()=>el.removeEventListener("node-select",fn);
  },[onNodeSelect]);
  return <topospace-graph-v1 ref={ref} class={className||""}></topospace-graph-v1>;
}
