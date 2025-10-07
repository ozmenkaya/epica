import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Organization, Membership
from core.models import Customer, Supplier


@pytest.mark.django_db
def test_customer_portal_access(client):
    U = get_user_model()
    u = U.objects.create_user(username="cust", password="p")
    org = Organization.objects.create(name="OrgP")
    c = Customer.objects.create(organization=org, name="Cust1", user=u)

    client.login(username="cust", password="p")
    res = client.get(reverse("customer_portal"))
    assert res.status_code == 200
    assert "Cust1" in res.content.decode()


@pytest.mark.django_db
def test_supplier_portal_access(client):
    U = get_user_model()
    u = U.objects.create_user(username="supp", password="p")
    org = Organization.objects.create(name="OrgP2")
    s = Supplier.objects.create(organization=org, name="Supp1", user=u)

    client.login(username="supp", password="p")
    res = client.get(reverse("supplier_portal"))
    assert res.status_code == 200
    assert "Supp1" in res.content.decode()


@pytest.mark.django_db
def test_other_user_cannot_access_portals(client):
    U = get_user_model()
    other = U.objects.create_user(username="o", password="p")
    org = Organization.objects.create(name="OrgX")
    Customer.objects.create(organization=org, name="C", user=None)
    Supplier.objects.create(organization=org, name="S", user=None)

    client.login(username="o", password="p")
    assert client.get(reverse("customer_portal")).status_code in (302, 403)
    assert client.get(reverse("supplier_portal")).status_code in (302, 403)
