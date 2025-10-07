import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Organization, Membership
from core.models import Customer, Supplier


@pytest.mark.django_db
def setup_org_user(role=Membership.Role.MEMBER):
    U = get_user_model()
    user = U.objects.create_user(username=f"u_{role}", password="p")
    org = Organization.objects.create(name=f"Org_{role}")
    Membership.objects.create(user=user, organization=org, role=role)
    return user, org


@pytest.mark.django_db
def test_customer_search_and_filter(client):
    user, org = setup_org_user(Membership.Role.MEMBER)
    Customer.objects.create(organization=org, name="Alpha", email="a@x.com")
    Customer.objects.create(organization=org, name="Beta", email="")
    client.login(username=f"u_{Membership.Role.MEMBER}", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()

    res = client.get(reverse("customers_list"), {"q": "alp"})
    assert "Alpha" in res.content.decode()
    assert "Beta" not in res.content.decode()

    res = client.get(reverse("customers_list"), {"has_email": "1"})
    html = res.content.decode()
    assert "Alpha" in html and "Beta" not in html


@pytest.mark.django_db
def test_customer_edit_delete_permissions(client):
    admin_user, org = setup_org_user(Membership.Role.ADMIN)
    member_user, _ = setup_org_user(Membership.Role.MEMBER)
    # move member to same org
    Membership.objects.filter(user=member_user).update(organization=org)

    obj = Customer.objects.create(organization=org, name="Zeta")

    # member cannot edit
    client.login(username=f"u_{Membership.Role.MEMBER}", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()
    res = client.post(reverse("customers_edit", args=[obj.id]), {"name": "Changed"})
    assert res.status_code == 403

    # admin can edit
    client.logout()
    client.login(username=f"u_{Membership.Role.ADMIN}", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()
    res = client.post(reverse("customers_edit", args=[obj.id]), {"name": "Changed"})
    assert res.status_code == 302
    obj.refresh_from_db()
    assert obj.name == "Changed"

    # admin can delete
    res = client.post(reverse("customers_delete", args=[obj.id]))
    assert res.status_code == 302
    assert not Customer.objects.filter(id=obj.id).exists()


@pytest.mark.django_db
def test_supplier_search_and_filter(client):
    user, org = setup_org_user(Membership.Role.MEMBER)
    Supplier.objects.create(organization=org, name="Gamma", email="g@x.com")
    Supplier.objects.create(organization=org, name="Delta", email="")
    client.login(username=f"u_{Membership.Role.MEMBER}", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()

    res = client.get(reverse("suppliers_list"), {"q": "gam"})
    assert "Gamma" in res.content.decode()
    assert "Delta" not in res.content.decode()

    res = client.get(reverse("suppliers_list"), {"has_email": "1"})
    html = res.content.decode()
    assert "Gamma" in html and "Delta" not in html


@pytest.mark.django_db
def test_supplier_edit_delete_permissions(client):
    admin_user, org = setup_org_user(Membership.Role.ADMIN)
    member_user, _ = setup_org_user(Membership.Role.MEMBER)
    Membership.objects.filter(user=member_user).update(organization=org)
    obj = Supplier.objects.create(organization=org, name="Omega")

    # member cannot edit
    client.login(username=f"u_{Membership.Role.MEMBER}", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()
    res = client.post(reverse("suppliers_edit", args=[obj.id]), {"name": "Changed"})
    assert res.status_code == 403

    # admin can edit
    client.logout()
    client.login(username=f"u_{Membership.Role.ADMIN}", password="p")
    session = client.session
    session["current_org"] = org.slug
    session.save()
    res = client.post(reverse("suppliers_edit", args=[obj.id]), {"name": "Changed"})
    assert res.status_code == 302
    obj.refresh_from_db()
    assert obj.name == "Changed"

    # admin can delete
    res = client.post(reverse("suppliers_delete", args=[obj.id]))
    assert res.status_code == 302
    assert not Supplier.objects.filter(id=obj.id).exists()
