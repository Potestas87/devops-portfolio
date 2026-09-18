from main import app


def test_index():
    res = app.test_client().get("/")
    assert res.status_code == 200
    assert res.get_json()["service"] == "api"


def test_healthz():
    assert app.test_client().get("/healthz").get_json() == {"status": "ok"}


def test_fail_returns_500():
    assert app.test_client().get("/fail").status_code == 500


def test_metrics_exposed():
    client = app.test_client()
    client.get("/")
    body = client.get("/metrics").get_data(as_text=True)
    assert "http_requests_total" in body
