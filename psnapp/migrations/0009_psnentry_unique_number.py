# Generated by Django 5.1.6 on 2025-02-26 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("psnapp", "0008_psnentry_is_processed"),
    ]

    operations = [
        migrations.AddField(
            model_name="psnentry",
            name="unique_number",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
