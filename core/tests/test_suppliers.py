import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Organization, Membership
from core.models import Supplier


@pytest.mark.django_db
def test_member_can_list_suppliers(client):
    U = get_user_model()
    user = U.objects.create_user(username="u1", password="p")
    org = Organization.objects.create(name="OrgA", owner=user)
    Membership.objects.create(user=user, organization=org, role=Membership.Role.MEMBER)
    client.login(username="u1", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()

    url = reverse("suppliers_list")
    res = client.get(url)
    assert res.status_code == 200


@pytest.mark.django_db
def test_admin_can_create_supplier(client):
    U = get_user_model()
    user = U.objects.create_user(username="adminu", password="p")
    org = Organization.objects.create(name="OrgB", owner=user)
    Membership.objects.create(user=user, organization=org, role=Membership.Role.ADMIN)
    client.login(username="adminu", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()

    url = reverse("suppliers_create")
    res = client.post(url, {"name": "Acme", "email": "a@c.me", "phone": "", "notes": ""})
    assert res.status_code == 302
    assert Supplier.objects.filter(organization=org, name="Acme").exists()


@pytest.mark.django_db
def test_member_cannot_create_supplier(client):
    U = get_user_model()
    user = U.objects.create_user(username="m1", password="p")
    org = Organization.objects.create(name="OrgC", owner=user)
    Membership.objects.create(user=user, organization=org, role=Membership.Role.MEMBER)
    client.login(username="m1", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()

    url = reverse("suppliers_create")
    res = client.post(url, {"name": "Blocked"})
    assert res.status_code == 403


@pytest.mark.django_db
def test_org_isolation_on_suppliers_list(client):
    U = get_user_model()
    user1 = U.objects.create_user(username="u1", password="p")
    user2 = U.objects.create_user(username="u2", password="p")
    org1 = Organization.objects.create(name="Org1", owner=user1)
    org2 = Organization.objects.create(name="Org2", owner=user2)
    Membership.objects.create(user=user1, organization=org1, role=Membership.Role.MEMBER)
    Membership.objects.create(user=user2, organization=org2, role=Membership.Role.MEMBER)

    Supplier.objects.create(organization=org1, name="S1")
    Supplier.objects.create(organization=org2, name="S2")

    client.login(username="u1", password="p")
    session = client.session
    session["current_org"] = org1.slug
    session.save()

    res = client.get(reverse("suppliers_list"))
    assert res.status_code == 200
    html = res.content.decode()
    assert "S1" in html and "S2" not in html
