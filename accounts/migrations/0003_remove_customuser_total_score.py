# Generated by Django 5.0 on 2024-06-15 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_customuser_total_score"),
    ]

    operations = [
        migrations.RemoveField(model_name="customuser", name="total_score",),
    ]