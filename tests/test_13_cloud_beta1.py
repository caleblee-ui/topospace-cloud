
import os
from cloud21.bootstrap import build_service
from cloud21.http_provider import OpenAICompatibleHTTPProvider

def test_provider_url_contract():
    p=OpenAICompatibleHTTPProvider("https://example.com/v1","x")
    assert p.base_url=="https://example.com/v1"

def test_bootstrap_mock(monkeypatch):
    monkeypatch.setenv("TOPOSPACE_API_KEY","sk-test")
    monkeypatch.setenv("ALLOW_MOCK_PROVIDER","true")
    monkeypatch.delenv("PRIMARY_PROVIDER_BASE_URL",raising=False)
    monkeypatch.delenv("PRIMARY_PROVIDER_API_KEY",raising=False)
    s=build_service()
    assert s.provider_router is not None

def test_bootstrap_requires_public_key(monkeypatch):
    monkeypatch.delenv("TOPOSPACE_API_KEY",raising=False)
    try:build_service();assert False
    except RuntimeError as e:assert "TOPOSPACE_API_KEY" in str(e)

def test_replit_files_exist():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    assert (root/".replit").exists() and (root/"requirements.txt").exists() and (root/"main.py").exists()
