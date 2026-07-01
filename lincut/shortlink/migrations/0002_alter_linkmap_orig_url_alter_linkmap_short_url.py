import shortlink.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortlink", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="linkmap",
            name="orig_url",
            field=models.CharField(
                unique=True, validators=[shortlink.models.custom_url_validator]
            ),
        ),
        migrations.AlterField(
            model_name="linkmap",
            name="short_url",
            field=models.CharField(
                unique=True, validators=[shortlink.models.custom_url_validator]
            ),
        ),
    ]
