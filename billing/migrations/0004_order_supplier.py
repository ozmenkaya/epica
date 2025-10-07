from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0003_order_currency"),
        ("core", "0014_alter_categoryformfield_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="supplier",
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name="orders", to="core.supplier"),
        ),
    ]
