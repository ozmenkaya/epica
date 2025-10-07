from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_supplier"),
        ("accounts", "0003_role_membership_role_fk"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="customer_profile", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="supplier",
            name="user",
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="supplier_profile", to=settings.AUTH_USER_MODEL),
        ),
    ]
