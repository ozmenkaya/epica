from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_quotecomment"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="desired_quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
