from django.contrib import admin
from .models import Organization, Membership, Role


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "owner", "created_at")
	search_fields = ("name",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "organization", "role", "role_fk", "created_at")
	list_filter = ("role", "role_fk")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ("id", "key", "name", "created_at")
	search_fields = ("key", "name")
