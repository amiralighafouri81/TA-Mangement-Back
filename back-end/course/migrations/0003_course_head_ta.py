# Generated by Django 5.1.3 on 2024-12-22 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_condition'),
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='head_TA',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='request.request'),
        ),
    ]
