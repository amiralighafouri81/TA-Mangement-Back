# Generated by Django 5.1.3 on 2024-12-22 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_head_ta'),
        ('request', '0003_alter_request_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='condition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='head_TA',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='request.request'),
        ),
    ]