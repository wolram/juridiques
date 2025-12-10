import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_list_agents():
    resp = client.get('/agents')
    assert resp.status_code == 200
    data = resp.json()
    assert 'pesquisa' in data


def test_redator_run_mock():
    payload = {"input": "Gerar rascunho de contestação"}
    resp = client.post('/agents/redator/run', json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert 'title' in data or 'sections' in data
