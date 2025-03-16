from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('psnapp', '0021_auto_20250304_0009'),  # Replace with the last migration
    ]

    operations = [
        migrations.AddField(
            model_name='psnentry',
            name='engineer_name',
            field=models.CharField(max_length=255, null=False, default='Unknown'),
        ),
        migrations.AddField(
            model_name='psnentry',
            name='issue',
            field=models.TextField(null=False, default='Unknown'),
        ),
        migrations.AddField(
            model_name='psnentry',
            name='psn',
            field=models.CharField(max_length=50, null=False, default='Unknown'),
        ),
    ]
