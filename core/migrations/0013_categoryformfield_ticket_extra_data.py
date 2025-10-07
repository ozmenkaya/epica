from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_ticket_desired_quantity"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryFormField",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=100)),
                ("name", models.SlugField(max_length=100, help_text="Veri anahtarı (otomatik üretilebilir)")),
                ("field_type", models.CharField(choices=[("text", "Metin"), ("select", "Seçim (Dropdown)")], default="text", max_length=10)),
                ("options", models.TextField(blank=True, help_text="Select için seçenekleri satır satır yazın")),
                ("required", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
                ("help_text", models.CharField(max_length=200, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="category_form_fields", to="accounts.organization")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="form_fields", to="core.category")),
            ],
            options={
                "ordering": ["category", "order", "id"],
                "unique_together": {("category", "name")},
            },
        ),
        migrations.AddField(
            model_name="ticket",
            name="extra_data",
            field=models.JSONField(default=dict, blank=True),
        ),
    ]
