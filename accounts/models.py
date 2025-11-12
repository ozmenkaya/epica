from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Role(models.Model):
	"""Custom tenant roles definable in admin (e.g., editor, viewer)."""
	key = models.SlugField(max_length=50, unique=True)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return f"{self.name} ({self.key})"


class Organization(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_organizations")
	created_at = models.DateTimeField(auto_now_add=True)
	
	# Email Settings
	email_host = models.CharField(max_length=255, blank=True, help_text="SMTP sunucu adresi (örn: smtp.gmail.com)")
	email_port = models.IntegerField(null=True, blank=True, help_text="SMTP port (örn: 587 veya 465)")
	email_use_tls = models.BooleanField(default=True, help_text="TLS kullan (port 587 için)")
	email_use_ssl = models.BooleanField(default=False, help_text="SSL kullan (port 465 için)")
	email_host_user = models.CharField(max_length=255, blank=True, help_text="SMTP kullanıcı adı / email")
	email_host_password = models.CharField(max_length=255, blank=True, help_text="SMTP şifre / App Password")
	email_from_address = models.EmailField(blank=True, help_text="Gönderen email adresi")

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			base = slugify(self.name) or "org"
			candidate = base
			i = 1
			while Organization.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
				i += 1
				candidate = f"{base}-{i}"
			self.slug = candidate
		return super().save(*args, **kwargs)


class Membership(models.Model):
	class Role(models.TextChoices):
		OWNER = "owner", "Owner"
		ADMIN = "admin", "Admin"
		MEMBER = "member", "Member"

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
	role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
	role_fk = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='memberships')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("user", "organization")

	def __str__(self) -> str:
		return f"{self.user} @ {self.organization} ({self.role})"

# Create your models here.
