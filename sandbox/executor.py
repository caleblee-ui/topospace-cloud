
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import subprocess, tempfile, shutil, os, time

@dataclass
class ExecutionResult:
    returncode: int
    stdout: str
    stderr: str
    elapsed_ms: float
    timed_out: bool = False

class PatchSandbox:
    """Filesystem-copy sandbox for safe agent patch/test cycles.

    It isolates repository mutations in a temporary directory. This is not a
    kernel/container security boundary; production deployments should replace
    it with containers/VMs.
    """
    def __init__(self, repo: str|Path):
        self.repo = Path(repo)

    def __enter__(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="topospace-sandbox-"))
        self.copy = self.tmp/"repo"
        shutil.copytree(self.repo, self.copy, dirs_exist_ok=True)
        return self

    def run(self, command, timeout=60):
        start=time.perf_counter()
        try:
            p=subprocess.run(command, cwd=self.copy, shell=isinstance(command,str),
                             capture_output=True, text=True, timeout=timeout)
            return ExecutionResult(p.returncode,p.stdout,p.stderr,(time.perf_counter()-start)*1000,False)
        except subprocess.TimeoutExpired as e:
            return ExecutionResult(124,e.stdout or "",e.stderr or "",(time.perf_counter()-start)*1000,True)

    def __exit__(self, exc_type, exc, tb):
        shutil.rmtree(self.tmp, ignore_errors=True)
