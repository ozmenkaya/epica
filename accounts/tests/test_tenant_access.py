import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Organization, Membership


@pytest.mark.django_db
def test_member_can_access_dashboard(client):
    user = User.objects.create_user(username="u1", password="p")
    org = Organization.objects.create(name="Org A", owner=user)
    Membership.objects.create(user=user, organization=org, role=Membership.Role.MEMBER)
    client.login(username="u1", password="p")
    # select org via switch
    client.get(reverse("org_switch", args=[org.slug]))
    resp = client.get(reverse("dashboard"))
    assert resp.status_code == 200
    assert b"Org A" in resp.content


@pytest.mark.django_db
def test_non_member_forbidden(client):
    user = User.objects.create_user(username="u2", password="p")
    other = User.objects.create_user(username="u3", password="p")
    org = Organization.objects.create(name="Org B", owner=other)
    Membership.objects.create(user=other, organization=org, role=Membership.Role.OWNER)
    # user2 login
    client.login(username="u2", password="p")
    # try switch to org without membership
    client.get(reverse("org_switch", args=[org.slug]))
    resp = client.get(reverse("dashboard"))
    assert resp.status_code in (302, 403)