from django.db import migrations, models

def set_default_unique_number(apps, schema_editor):
    PSNEntry = apps.get_model('psnapp', 'PSNEntry')
    for entry in PSNEntry.objects.all():
        if entry.unique_number is None:
            entry.unique_number = 10000 + entry.id  # Set a default unique number
            entry.save()

class Migration(migrations.Migration):

    dependencies = [
        ('psnapp', '0016_auto_set_default_unique_number'),
    ]

    operations = [
        migrations.RunPython(set_default_unique_number),
    ]