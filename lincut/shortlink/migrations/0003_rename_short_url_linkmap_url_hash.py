from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shortlink", "0002_alter_linkmap_orig_url_alter_linkmap_short_url"),
    ]

    operations = [
        migrations.RenameField(
            model_name="linkmap",
            old_name="short_url",
            new_name="url_hash",
        ),
    ]
