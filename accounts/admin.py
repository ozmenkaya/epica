from django.contrib import admin
from .models import Organization, Membership, Role


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "owner", "email_host", "created_at")
	search_fields = ("name",)
	fieldsets = (
		('Genel Bilgiler', {
			'fields': ('name', 'slug', 'owner')
		}),
		('Email Ayarları', {
			'fields': (
				'email_host', 
				'email_port', 
				'email_use_tls', 
				'email_use_ssl',
				'email_host_user', 
				'email_host_password',
				'email_from_address',
			),
			'description': 'Organizasyona özel SMTP ayarları. Boş bırakırsanız sistem varsayılan ayarları kullanır.',
		}),
	)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "organization", "role", "role_fk", "created_at")
	list_filter = ("role", "role_fk")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ("id", "key", "name", "created_at")
	search_fields = ("key", "name")
