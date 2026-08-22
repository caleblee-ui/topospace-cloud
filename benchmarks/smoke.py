import subprocess, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
for script, expected in [
    (root/'examples'/'coding_agent.py', 'auth.py'),
    (root/'examples'/'agent_runtime.py', 'CONTEXT'),
    (root/'benchmarks'/'cosine_vs_topospace.py', 'topospace'),
    (root/'benchmarks'/'repository_benchmark.py', 'repository_files'),
    (root/'tests'/'test_v03.py', 'PASS'),
]:
    r=subprocess.run([sys.executable,str(script)],capture_output=True,text=True)
    print(r.stdout)
    if r.stderr: print(r.stderr)
    assert r.returncode==0, (script,r.stderr)
    assert expected in r.stdout
print('TopoSpace v0.3 smoke benchmark: PASS')
