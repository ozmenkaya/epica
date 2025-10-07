from django.urls import reverse


def test_webhook_ok(client):
    url = reverse("stripe_webhook")
    resp = client.post(url, data=b"{}", content_type="application/json")
    assert resp.status_code == 200
    assert resp.content == b"ok"
