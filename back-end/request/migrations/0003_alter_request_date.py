# Generated by Django 5.1.3 on 2024-12-22 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0002_alter_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
