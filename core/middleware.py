from typing import Optional
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from accounts.models import Organization, Membership


class TenantMiddleware(MiddlewareMixin):
    """Resolve current tenant from ?org=<slug> or session."""

    def process_request(self, request: HttpRequest):
        slug = request.GET.get("org") or request.session.get("current_org")
        tenant: Optional[Organization] = None
        if slug:
            tenant = Organization.objects.filter(slug=slug).first()
            if tenant:
                request.session["current_org"] = tenant.slug
        request.tenant = tenant

    # Optionally, you can enforce auth per-tenant here
