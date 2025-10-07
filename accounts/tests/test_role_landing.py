import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Organization, Membership, Role


@pytest.mark.django_db
def test_owner_redirects_to_dashboard(client):
    u = User.objects.create_user(username="u", password="p")
    org = Organization.objects.create(name="Org", owner=u)
    Membership.objects.create(user=u, organization=org, role=Membership.Role.OWNER)
    client.login(username="u", password="p")
    client.get(reverse("org_switch", args=[org.slug]))
    resp = client.get(reverse("role_landing"))
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/dashboard/")


@pytest.mark.django_db
def test_custom_role_key_mapping(client):
    u = User.objects.create_user(username="u2", password="p")
    org = Organization.objects.create(name="Org2", owner=u)
    r = Role.objects.create(key="viewer", name="Viewer")
    Membership.objects.create(user=u, organization=org, role=Membership.Role.MEMBER, role_fk=r)
    client.login(username="u2", password="p")
    client.get(reverse("org_switch", args=[org.slug]))
    resp = client.get(reverse("role_landing"))
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
