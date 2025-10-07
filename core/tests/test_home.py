import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_status(client):
    resp = client.get(reverse("home"))
    assert resp.status_code == 200
    assert b"Epica SaaS" in resp.content
