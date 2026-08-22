
from pathlib import Path
import sys, ast, json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from index.embeddings import HashEmbeddingProvider
from index.ann import ANNIndex

def scan(repo):
    rows=[]
    for p in Path(repo).rglob("*.py"):
        if any(x.startswith(".") for x in p.parts): continue
        try: text=p.read_text(errors="ignore")
        except Exception: continue
        symbols=[]
        try:
            symbols=[n.name for n in ast.walk(ast.parse(text)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
        except Exception: pass
        rows.append({"path":str(p.relative_to(repo)),"text":text[:16000],"symbols":symbols})
    return rows

def run(repo,query,k=10):
    rows=scan(repo); emb=HashEmbeddingProvider(); idx=ANNIndex(128)
    vecs={r["path"]:emb.embed(r["text"]+" "+" ".join(r["symbols"])) for r in rows};idx.build(vecs.items())
    semantic=idx.query(emb.embed(query),k)
    q=set(query.lower().split())
    hybrid=[]
    semantic_map=dict(idx.query(emb.embed(query),max(1,len(rows))))
    for r in rows:
        structural=sum(1 for s in r["symbols"] if any(x in s.lower() for x in q))
        path_score=sum(1 for x in q if x in r["path"].lower())
        hybrid.append((r["path"],semantic_map.get(r["path"],0)+.15*structural+.10*path_score))
    hybrid.sort(key=lambda x:x[1],reverse=True)
    result={"files":len(rows),"backend":idx.backend,"semantic":semantic,"hybrid":hybrid[:k]}
    print(json.dumps(result,indent=2))
    return result

if __name__=="__main__":
    if len(sys.argv)<3: raise SystemExit("usage: public_repo_v1.py REPO QUERY")
    run(sys.argv[1],sys.argv[2])
