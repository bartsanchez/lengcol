from django.db import migrations


def update_site_domain_and_name(apps, schema_editor):
    site_model = apps.get_model("sites", "Site")

    domain_name = "lenguajecoloquial.com"
    site_model.objects.update_or_create(
        id=1,
        defaults={"domain": domain_name, "name": domain_name},
    )


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("definitions", "0010_definition_tags"),
    ]

    operations = [migrations.RunPython(update_site_domain_and_name)]
