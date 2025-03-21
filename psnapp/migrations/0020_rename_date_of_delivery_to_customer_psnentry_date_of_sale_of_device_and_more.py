# Generated by Django 5.1.6 on 2025-03-03 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("psnapp", "019_auto_set_default_unique_number"),
    ]

    operations = [
        migrations.RenameField(
            model_name="psnentry",
            old_name="date_of_delivery_to_customer",
            new_name="date_of_sale_of_device",
        ),
        migrations.RenameField(
            model_name="psnentry",
            old_name="delivery_date",
            new_name="issue_raised_by_customer",
        ),
        migrations.RenameField(
            model_name="psnentry",
            old_name="repair_priority_date",
            new_name="vehicle_sale_date",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="action",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="device_activity_completion",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="engineer_email",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="engineer_name",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="fitted_at_customer_vehicle",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="grn_no",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="hod_approval_status",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="is_processed",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="issue",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="location_to_delivery_date",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="manager_approval_status",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="psn",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="repaired",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="request_id",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="reused_for_field",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="shipped_date",
        ),
        migrations.RemoveField(
            model_name="psnentry",
            name="unique_number",
        ),
        migrations.AddField(
            model_name="psnentry",
            name="active_profile",
            field=models.CharField(
                choices=[("Airtel", "Airtel"), ("BSNL", "BSNL"), ("Dual", "Dual")],
                default="Airtel",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="c_trigger_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="commercial_expiry_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="complaint_raised_by",
            field=models.CharField(
                choices=[
                    ("Dealer", "Dealer"),
                    ("Customer", "Customer"),
                    ("AL Field", "AL Field"),
                    ("AL Service", "AL Service"),
                    ("I-Alert", "I-Alert"),
                ],
                default="Dealer",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="complaint_raised_name",
            field=models.CharField(default="Unknown", max_length=100),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="complaint_raised_through",
            field=models.CharField(
                choices=[
                    ("I-Alert", "I-Alert"),
                    ("Mail", "Mail"),
                    ("Telephone", "Telephone"),
                ],
                default="I-Alert",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="configuration",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="contact_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="device_iccid",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="device_imei",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="device_model",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="device_psn",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="device_sent_to",
            field=models.CharField(
                choices=[
                    ("Goa", "Goa"),
                    ("Hyderabad", "Hyderabad"),
                    ("Chennai", "Chennai"),
                    ("Others", "Others"),
                ],
                default="Goa",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="engineer_recommendation",
            field=models.CharField(
                choices=[
                    ("Repair", "Repair"),
                    ("Replace", "Replace"),
                    ("Monitor", "Monitor"),
                ],
                default="Repair",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="external_modification",
            field=models.CharField(
                choices=[
                    ("Air horn", "Air horn"),
                    ("Cabin", "Cabin"),
                    ("Alt-Device", "Alt-Device"),
                    ("Dashboard Modification", "Dashboard Modification"),
                ],
                default="Air horn",
                max_length=25,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="firmware",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="first_communication_on_darby",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="hod_remarks",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="issue_analysis",
            field=models.CharField(
                choices=[
                    ("Disk Image", "Disk Image"),
                    ("Sim-Reg issue", "Sim-Reg issue"),
                    ("Sim Expire", "Sim Expire"),
                    ("VIC Issue", "VIC Issue"),
                    ("CAN Issue", "CAN Issue"),
                    ("SW-Issue", "SW-Issue"),
                    ("GPS status", "GPS status"),
                    ("Others", "Others"),
                ],
                default="Disk Image",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="issue_description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="issue_identified",
            field=models.CharField(
                choices=[
                    ("100%V Packet", "100%V Packet"),
                    ("Partial V Packet", "Partial V Packet"),
                    ("Latency", "Latency"),
                    ("Data loss", "Data loss"),
                ],
                default="100%V Packet",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="kilometers_hours",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="last_communication_on_darby",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="main_battery_voltage",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="manager_remarks",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="s_trigger_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="service_engineer_name",
            field=models.CharField(
                choices=[
                    ("Anil", "Anil"),
                    ("Siva", "Siva"),
                    ("Swamy", "Swamy"),
                    ("Rishwanth", "Rishwanth"),
                    ("Gayadhar", "Gayadhar"),
                    ("Arun Maity", "Arun Maity"),
                ],
                default="Anil",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="telco_status",
            field=models.CharField(
                choices=[("Bootstrap", "Bootstrap"), ("Commercial", "Commercial")],
                default="Bootstrap",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="vehicle_running_location",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="vehicle_support_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="vehicle_type",
            field=models.CharField(
                choices=[
                    ("Tipper", "Tipper"),
                    ("E-com", "E-com"),
                    ("Boss", "Boss"),
                    ("Haulage", "Haulage"),
                ],
                default="Tipper",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="vehicle_usage",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="psnentry",
            name="vin_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
