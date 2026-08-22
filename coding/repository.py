from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import ast, hashlib
from typing import Dict, List, Set

@dataclass
class CodeRecord:
    path: str
    language: str
    content: str
    symbols: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    digest: str = ""

class RepositoryIngestor:
    """Converts a repository into normalized code records for TopoSpace."""
    def __init__(self, max_bytes: int = 256_000): self.max_bytes=max_bytes

    def ingest(self, root: str | Path) -> List[CodeRecord]:
        root=Path(root); out=[]
        for p in sorted(root.rglob('*')):
            if not p.is_file() or any(x in {'.git','.venv','node_modules','__pycache__'} for x in p.parts): continue
            if p.suffix not in {'.py','.ts','.tsx','.js','.jsx','.md','.json','.toml','.yaml','.yml'}: continue
            try:
                raw=p.read_bytes()
                if len(raw)>self.max_bytes: continue
                text=raw.decode('utf-8',errors='ignore')
            except OSError: continue
            symbols=[]; imports=[]
            if p.suffix=='.py':
                try:
                    tree=ast.parse(text)
                    for n in ast.walk(tree):
                        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)): symbols.append(n.name)
                        elif isinstance(n,ast.Import): imports.extend(a.name for a in n.names)
                        elif isinstance(n,ast.ImportFrom) and n.module: imports.append(n.module)
                except SyntaxError: pass
            out.append(CodeRecord(str(p.relative_to(root)),p.suffix.lstrip('.'),text,symbols,imports,hashlib.sha256(raw).hexdigest()))
        return out

class CodeGraph:
    """Small structural graph used as one component of composite relevance."""
    def __init__(self, records: List[CodeRecord]):
        self.records={r.path:r for r in records}; self.edges: Dict[str,Set[str]]={r.path:set() for r in records}
        module_to_path={p[:-3].replace('/','.') : p for p in self.records if p.endswith('.py')}
        for r in records:
            if not r.path.endswith('.py'): continue
            for imp in r.imports:
                candidates=[imp, imp.rsplit('.',1)[0] if '.' in imp else imp]
                for c in candidates:
                    if c in module_to_path:
                        dst=module_to_path[c]; self.edges[r.path].add(dst); self.edges[dst].add(r.path)

    def distance(self,a: str,b: str,max_depth: int=4) -> float:
        if a==b:return 0.0
        if a not in self.edges or b not in self.edges:return 1.0
        frontier={a}; seen={a}
        for depth in range(1,max_depth+1):
            nxt=set()
            for n in frontier:nxt.update(self.edges[n])
            if b in nxt:return depth/max_depth
            nxt-=seen; seen|=nxt; frontier=nxt
            if not frontier:break
        return 1.0
