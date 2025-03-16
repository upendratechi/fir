# Generated by Django 5.1.6 on 2025-02-25 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("psnapp", "0005_psnentry_manager_approval_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="psnentry",
            name="date_of_complaint",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="date_of_delivery_to_customer",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="delivery_date",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="device_activity_completion",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="fitted_at_customer_vehicle",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="location_to_delivery_date",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="repair_priority_date",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="repaired",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="shipped_date",
        ),
        migrations.AlterField(
            model_name="psnentry",
            name="engineer_name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="psnentry",
            name="issue",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="psnentry",
            name="manager_approval_status",
            field=models.CharField(
                choices=[
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                    ("Pending", "Pending"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="psnentry",
            name="psn",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="psnentry",
            name="resolved_or_not",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")], max_length=10
            ),
        ),
    ]
