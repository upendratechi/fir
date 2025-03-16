from django.db import migrations, models
from django.utils import timezone

def set_defaults(apps, schema_editor):
    PSNEntry = apps.get_model('psnapp', 'PSNEntry')
    for entry in PSNEntry.objects.all():
        if not entry.engineer_name:
            entry.engineer_name = 'Unknown'
        if not entry.issue:
            entry.issue = 'Unknown'
        if not entry.psn:
            entry.psn = 'Unknown'
        if not entry.unique_id:
            today = timezone.now()
            date_str = today.strftime('%d%m%y')
            last_entry = PSNEntry.objects.filter(unique_id__startswith=date_str).order_by('unique_id').last()
            if last_entry:
                last_serial = int(last_entry.unique_id[-3:])
                new_serial = last_serial + 1
            else:
                new_serial = 1
            entry.unique_id = f"{date_str}{new_serial:03d}"
        entry.save()

class Migration(migrations.Migration):

    dependencies = [
        ('psnapp', '0022_auto_20250304_0010'),  # Replace with the last migration
    ]

    operations = [
        migrations.AddField(
            model_name='psnentry',
            name='unique_id',
            field=models.CharField(max_length=9, unique=True, editable=False, default=''),
        ),
        migrations.RunPython(set_defaults),
    ]