from pathlib import Path
import tempfile, shutil, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coding.agent import CodingAgent,semantic_selector,topological_selector

def fixture(root):
    root=Path(root); (root/'app').mkdir(); (root/'tests').mkdir()
    (root/'app/__init__.py').write_text('')
    (root/'app/auth.py').write_text('''def verify_token(token, expected):\n    return token == expected  # INSECURE_TOKEN_COMPARE\n''')
    (root/'app/auth_helpers.py').write_text('''def normalize_user(x): return x.strip().lower()\n''')
    (root/'app/layout.py').write_text('''# token styles authentication banner oauth words as semantic decoys\ndef render(): return "oauth token authentication"\n''')
    for i in range(12):
        (root/f'app/decoy_{i}.py').write_text(f'# oauth authentication token security session\ndef decoy_{i}(): return {i}\n')
    (root/'tests/test_auth.py').write_text('''from app.auth import verify_token\ndef test_verify_token():\n    assert verify_token("abc","abc")\n    assert not verify_token("abc","abd")\n''')
    (root/'tests/test_security.py').write_text('''from pathlib import Path\ndef test_constant_time_patch_present():\n    text=Path("app/auth.py").read_text()\n    assert "compare_digest" in text\n''')
    (root/'pytest.ini').write_text('[pytest]\n')

def one(selector):
    td=tempfile.mkdtemp(prefix='topospace-e2e-'); fixture(td)
    try:
        m,obs=CodingAgent(td,selector).run('Fix authentication token comparison security vulnerability')
        return m.__dict__,obs
    finally: shutil.rmtree(td)

def main():
    result={'baseline':one(semantic_selector(8)),'topospace':one(topological_selector(8))}
    print(json.dumps(result,indent=2))
    out=Path(__file__).with_name('coding_agent_e2e_result.json');out.write_text(json.dumps(result,indent=2))
    studio=Path(__file__).resolve().parents[1]/'studio'/'data'/'coding_agent_trace.json';studio.parent.mkdir(parents=True,exist_ok=True);studio.write_text(json.dumps({'task':'Fix authentication token comparison security vulnerability','result':result},indent=2))
if __name__=='__main__':main()
