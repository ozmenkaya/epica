from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .permissions import backoffice_only
from .models import Organization, Membership


def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect("portal_home")
		messages.error(request, "Giriş başarısız")
	else:
		form = AuthenticationForm(request)
	return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
	logout(request)
	return redirect("role_landing")


def signup_view(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("portal_home")
		messages.error(request, "Kayıt başarısız")
	else:
		form = UserCreationForm()
	return render(request, "accounts/signup.html", {"form": form})


@backoffice_only
def org_list(request):
	orgs = Organization.objects.filter(memberships__user=request.user).distinct()
	current = getattr(request, "tenant", None)
	return render(request, "accounts/org_list.html", {"orgs": orgs, "current": current})


@backoffice_only
def org_create(request):
	if request.method == "POST":
		name = request.POST.get("name", "").strip()
		if name:
			org = Organization.objects.create(name=name, owner=request.user)
			Membership.objects.create(user=request.user, organization=org, role=Membership.Role.OWNER)
			request.session["current_org"] = org.slug
			return redirect("role_landing")
		messages.error(request, "İsim gerekli")
	return render(request, "accounts/org_create.html")


@backoffice_only
def org_switch(request, slug: str):
	org = Organization.objects.filter(slug=slug, memberships__user=request.user).first()
	if not org:
		messages.error(request, "Bu organizasyona erişiminiz yok")
		return redirect("org_list")
	request.session["current_org"] = org.slug
	return redirect("role_landing")
